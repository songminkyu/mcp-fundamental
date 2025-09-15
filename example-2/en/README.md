# FastMCP MCP Server Example

This project implements MCP servers and clients using STDIO and SSE approaches with FastMCP, based on the examples from [Medium article](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb).

## 📚 References

- **Original Medium Article**: [MCP Clients: Stdio vs SSE](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)
- **FastMCP**: A library for modern and simple MCP server implementation

## 🏗️ Project Structure

```
example-2/
├── requirements.txt          # Python dependencies
├── stdio_server.py          # FastMCP STDIO server
├── sse_server.py            # FastMCP SSE server
├── stdio_client.py          # STDIO client
├── sse_client.py            # SSE client
├── test_mcp.py              # Integrated tests
├── run_tests.py             # Test execution tool
└── README.md                # This file
```

## 🚀 Installation and Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Individual Servers

#### STDIO Server
```bash
python stdio_server.py
```

#### SSE Server
```bash
python sse_server.py
```

### 3. Run Individual Client Tests

#### STDIO Client
```bash
python stdio_client.py
```

#### SSE Client (SSE server must be running)
```bash
python sse_client.py
```

### 4. Integrated Tests

```bash
# Run all tests
python test_mcp.py

# Or use the convenient execution script
python run_tests.py              # All tests
python run_tests.py --stdio-only # STDIO only
python run_tests.py --sse-only   # SSE only
```

## 🛠️ Available Features

### Tools

1. **greet**: Greet with user name
   - Input: `{"name": "Alice"}`
   - Output: `"Hello, Alice! Welcome to the STDIO/SSE server."`

2. **add**: Add two numbers
   - Input: `{"a": 5, "b": 7}`
   - Output: `"The sum of 5 and 7 is 12"`

3. **multiply**: Multiply two numbers
   - Input: `{"a": 3.5, "b": 2.0}`
   - Output: `"The product of 3.5 and 2.0 is 7.0"`

4. **calculate**: Calculate mathematical expressions
   - Input: `{"expression": "sqrt(16) + 2 * 3"}`
   - Output: `"Calculation result: 10.0"`

5. **get_system_info**: Get system information
   - Input: `{}`
   - Output: System information JSON

6. **echo**: Return a message
   - Input: `{"message": "Hello World"}`
   - Output: `"Echo: Hello World"`

7. **get_server_status**: Get server status (SSE only)
   - Input: `{}`
   - Output: Server status information JSON

### Resources

1. **config://settings**: Server configuration file
2. **file://readme**: README resource

### Prompts

1. **code_review**: Code review prompt
   - Input: `{"code": "def hello(): print('Hello')", "language": "python"}`
   - Output: Structured prompt for code review

2. **explain_code**: Code explanation prompt
   - Input: `{"code": "def fibonacci(n): ...", "language": "python"}`
   - Output: Structured prompt for code explanation

## 🔄 STDIO vs SSE Comparison

| Aspect | STDIO Method | SSE Method |
|--------|--------------|------------|
| **Communication** | Standard I/O | HTTP + Server-Sent Events |
| **Environment** | Local process | Web service |
| **Complexity** | Simple | Complex |
| **Network Support** | None | Yes |
| **Real-time Streaming** | Limited | Supported |
| **Scalability** | Limited | High |
| **Authentication** | None | Possible |
| **Deployment** | Local execution | Web server deployment |

## 🎯 FastMCP Advantages

1. **Simple Decorator Syntax**: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`
2. **Automatic Type Inference**: Automatic schema generation from function signatures
3. **Modern Python Syntax**: async/await, type hints support
4. **Rapid Development**: Implement MCP server with minimal code
5. **Flexible Transport**: Support for both STDIO and SSE

## 📝 Usage Examples

### STDIO Server and Client

```python
# Server (stdio_server.py)
from fastmcp import FastMCP

mcp = FastMCP("STDIO Example Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # Automatically uses STDIO

# Client (stdio_client.py)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["stdio_server.py"]
    )
    
    async with stdio_client(server_params) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool("greet", {"name": "Alice"})
            print(result.content)
```

### SSE Server and Client

```python
# Server (sse_server.py)
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
import uvicorn

mcp = FastMCP("SSE Example Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

def create_starlette_app(mcp_server):
    sse = SseServerTransport("/messages/")
    # ... SSE configuration
    return Starlette(routes=[...])

if __name__ == "__main__":
    app = create_starlette_app(mcp._mcp_server)
    uvicorn.run(app, host="0.0.0.0", port=8080)

# Client (sse_client.py)
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client(url="http://localhost:8080/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool("greet", {"name": "Bob"})
            print(result.content)
```

## 🔧 Troubleshooting

### Common Issues

1. **SSE Server Connection Failed**: Check if SSE server is running
2. **Port Conflict**: Use a different port if 8080 is already in use
3. **Dependency Error**: Re-run `pip install -r requirements.txt`

### Debugging

```bash
# Run with detailed logs
python -u stdio_client.py
python -u sse_client.py
```

## 📄 License

This project is written for educational purposes and is based on the examples from the original Medium article.

## 🤝 Contributing

Please register bug reports or feature suggestions as issues.

---

**Note**: This example implements the content from the [Medium article](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb) in Python code.