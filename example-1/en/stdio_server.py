# stdio_server.py
import asyncio
import sys
import json
import math
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


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


async def main():
    """Main function"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
