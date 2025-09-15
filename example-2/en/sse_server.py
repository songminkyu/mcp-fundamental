# sse_server.py
"""
SSE-based MCP server using FastMCP
Implemented based on Medium article examples
"""

from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import math
import json
from typing import Dict, Any, List

# Create MCP server
mcp = FastMCP("SSE Example Server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet with user name"""
    return f"Hello, {name}! Welcome to the SSE server."

@mcp.tool()
def add(a: int, b: int) -> str:
    """Add two numbers and return result"""
    return f"The sum of {a} and {b} is {a + b}."

@mcp.tool()
def multiply(a: float, b: float) -> str:
    """Multiply two numbers and return result"""
    result = a * b
    return f"The product of {a} and {b} is {result}"

@mcp.tool()
def calculate(expression: str) -> str:
    """Calculate mathematical expression (safe calculation)"""
    try:
        # Only allow limited functions for safe calculation
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

@mcp.tool()
def get_system_info() -> str:
    """Return system information"""
    import platform
    import sys
    
    info = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "architecture": platform.architecture()[0],
        "processor": platform.processor()
    }
    
    return f"System Information:\n{json.dumps(info, indent=2)}"

@mcp.tool()
def echo(message: str) -> str:
    """Return the input message as is"""
    return f"Echo: {message}"

@mcp.tool()
def get_server_status() -> str:
    """Return server status"""
    import time
    import psutil
    
    status = {
        "server_name": "SSE Example Server",
        "uptime": time.time(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "status": "running"
    }
    
    return f"Server Status:\n{json.dumps(status, indent=2)}"

@mcp.resource("config://settings")
def get_config() -> str:
    """Return configuration file resource"""
    config = {
        "server_name": "SSE Example Server",
        "version": "1.0.0",
        "features": ["tools", "resources", "prompts", "sse"],
        "max_connections": 1000,
        "debug_mode": True,
        "sse_endpoint": "/sse"
    }
    return json.dumps(config, indent=2)

@mcp.resource("file://readme")
def get_readme() -> str:
    """Return README resource"""
    return """
# SSE MCP Server

This server is an SSE-based MCP server implemented using FastMCP.

## Available Tools
- greet: User greeting
- add: Add two numbers
- multiply: Multiply two numbers
- calculate: Calculate mathematical expressions
- get_system_info: Get system information
- echo: Return message
- get_server_status: Get server status

## Available Resources
- config://settings: Server configuration
- file://readme: This README file

## Available Prompts
- code_review: Code review prompt
- explain_code: Code explanation prompt

## SSE Endpoints
- /sse: Server-Sent Events stream
- /messages/: Message processing endpoint
"""

@mcp.prompt("code_review")
def code_review_prompt(code: str, language: str = "python") -> str:
    """Generate prompt for code review"""
    return f"""
Please review the following {language} code:

```{language}
{code}
```

Please check the following items:
1. Code style and readability
2. Potential bugs or errors
3. Performance optimization possibilities
4. Security vulnerabilities
5. Improvement suggestions

Please provide specific feedback for each item.
"""

@mcp.prompt("explain_code")
def explain_code_prompt(code: str, language: str = "python") -> str:
    """Generate prompt for code explanation"""
    return f"""
Please explain in detail what the following {language} code does:

```{language}
{code}
```

Please include the following:
1. Overall purpose of the code
2. Role and function of each part
3. Algorithms or patterns used
4. Input and output
5. Example usage
"""

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """Create Starlette application that provides MCP server through SSE"""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # Add CORS middleware
    app = Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

if __name__ == "__main__":
    # Get MCP server instance
    mcp_server = mcp._mcp_server

    # Create SSE-enabled Starlette app
    starlette_app = create_starlette_app(mcp_server, debug=True)

    port = 8080
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    print("Available tools: greet, add, multiply, calculate, get_system_info, echo, get_server_status")
    print("Available resources: config://settings, file://readme")
    print("Available prompts: code_review, explain_code")

    # Run server using uvicorn
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
