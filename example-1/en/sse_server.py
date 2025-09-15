# sse_server.py
import asyncio
import json
import math
from typing import Dict, Any
from mcp.server import Server
from mcp import types
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn


# Create server instance
server = Server("my-mcp-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """Return list of available tools."""
    return [
        types.Tool(
            name="calculator",
            description="Performs simple mathematical calculations",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate (e.g., 2+2)"
                    }
                },
                "required": ["expression"]
            }
        ),
        types.Tool(
            name="echo",
            description="Returns the input message as is",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to return"
                    }
                },
                "required": ["message"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    if name == "calculator":
        expression = arguments.get("expression", "")
        try:
            # Only allow limited functions for safe calculation
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return [types.TextContent(type="text", text=f"Calculation result: {result}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"Calculation error: {str(e)}")]
    
    elif name == "echo":
        message = arguments.get("message", "")
        return [types.TextContent(type="text", text=f"Echo: {message}")]
    
    else:
        raise ValueError(f"Unknown tool: {name}")


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """Return list of available resources."""
    return [
        types.Resource(
            uri="file://config.json",
            name="Configuration file",
            description="Application configuration file",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """Read and return a resource."""
    if uri == "file://config.json":
        return json.dumps({
            "version": "1.0",
            "debug": True,
            "max_connections": 100
        }, indent=2)
    else:
        raise ValueError(f"Unknown resource: {uri}")


@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """Return list of available prompts."""
    return [
        types.Prompt(
            name="code_review",
            description="Prompt for code review",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="Code to review",
                    required=True
                )
            ]
        )
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    """Return a prompt."""
    if name == "code_review":
        code = arguments["code"]
        return types.GetPromptResult(
            description="Code review prompt",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"Please review the following code:\n\n```\n{code}\n```"
                    )
                )
            ]
        )
    else:
        raise ValueError(f"Unknown prompt: {name}")


# SSE endpoint
async def sse_endpoint(request):
    """Server-Sent Events endpoint"""
    
    async def event_generator():
        # Initial connection message
        yield f"data: {json.dumps({'type': 'connected', 'message': 'MCP Server connected'})}\n\n"
        
        # Queue for receiving messages from client
        message_queue = asyncio.Queue()
        
        # Message processing task
        async def process_messages():
            while True:
                try:
                    # In actual implementation, client messages should be received via WebSocket or other methods
                    # Here we only provide a simple structure for demo purposes
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"Message processing error: {e}")
                    break
        
        # Start message processing
        task = asyncio.create_task(process_messages())
        
        try:
            while True:
                # Periodic status updates (in reality, respond to client messages)
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
                await asyncio.sleep(5)
        except Exception as e:
            print(f"SSE stream error: {e}")
        finally:
            task.cancel()
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


# API endpoints
async def list_tools_endpoint(request):
    """Return tool list"""
    tools = await server.list_tools()
    return JSONResponse(tools)


async def call_tool_endpoint(request):
    """Call a tool"""
    body = await request.json()
    name = body.get("name")
    arguments = body.get("arguments", {})
    
    try:
        result = await server.call_tool(name, arguments)
        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


async def list_resources_endpoint(request):
    """Return resource list"""
    resources = await server.list_resources()
    return JSONResponse(resources)


async def read_resource_endpoint(request):
    """Read a resource"""
    uri = request.query_params.get("uri")
    if not uri:
        return JSONResponse({"error": "URI is required"}, status_code=400)
    
    try:
        content = await server.read_resource(uri)
        return JSONResponse({"content": content})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


async def list_prompts_endpoint(request):
    """Return prompt list"""
    prompts = await server.list_prompts()
    return JSONResponse(prompts)


async def get_prompt_endpoint(request):
    """Get a prompt"""
    body = await request.json()
    name = body.get("name")
    arguments = body.get("arguments", {})
    
    try:
        result = await server.get_prompt(name, arguments)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


# Create Starlette application
app = Starlette(
    routes=[
        Route("/sse", sse_endpoint),
        Route("/tools", list_tools_endpoint, methods=["GET"]),
        Route("/tools/call", call_tool_endpoint, methods=["POST"]),
        Route("/resources", list_resources_endpoint, methods=["GET"]),
        Route("/resources/read", read_resource_endpoint, methods=["GET"]),
        Route("/prompts", list_prompts_endpoint, methods=["GET"]),
        Route("/prompts/get", get_prompt_endpoint, methods=["POST"]),
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    print("MCP Server (SSE) starting...")
    print("SSE endpoint: http://localhost:8000/sse")
    print("API endpoint: http://localhost:8000/tools")
    uvicorn.run(app, host="0.0.0.0", port=8000)
