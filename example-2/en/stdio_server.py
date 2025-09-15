# stdio_server.py
"""
STDIO-based MCP server using FastMCP
Implemented based on Medium article examples
"""

from fastmcp import FastMCP
import math
import json
from typing import Dict, Any, List

# Create MCP server
mcp = FastMCP("STDIO Example Server")

@mcp.tool()
def greet(name: str) -> str:
    """Greet with user name"""
    return f"Hello, {name}! Welcome to the STDIO server."

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

@mcp.resource("config://settings")
def get_config() -> str:
    """Return configuration file resource"""
    config = {
        "server_name": "STDIO Example Server",
        "version": "1.0.0",
        "features": ["tools", "resources", "prompts"],
        "max_connections": 100,
        "debug_mode": True
    }
    return json.dumps(config, indent=2)

@mcp.resource("file://readme")
def get_readme() -> str:
    """Return README resource"""
    return """
# STDIO MCP Server

This server is a STDIO-based MCP server implemented using FastMCP.

## Available Tools
- greet: User greeting
- add: Add two numbers
- multiply: Multiply two numbers
- calculate: Calculate mathematical expressions
- get_system_info: Get system information
- echo: Return message

## Available Resources
- config://settings: Server configuration
- file://readme: This README file
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

if __name__ == "__main__":
    print("Starting MCP server with STDIO transport...")
    print("Available tools: greet, add, multiply, calculate, get_system_info, echo")
    print("Available resources: config://settings, file://readme")
    print("Available prompts: code_review, explain_code")
    
    # run() method uses stdio by default
    mcp.run()
