# MCP Server Implementation Project

This project demonstrates how to build MCP (Model Context Protocol) servers using two different approaches: stdio and SSE, based on [MCP(Model Context Protocol)](https://blog.choonzang.com/it/ai/3318/).

## Project Structure

```
mcp-fundamental/
├── requirements.txt          # Python dependencies
├── stdio_server.py          # stdio-based MCP server
├── sse_server.py            # SSE-based MCP server
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Docker Compose configuration
└── README.md               # Project documentation
```

## Installation and Execution

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run stdio-based Server

```bash
python stdio_server.py
```

The stdio approach communicates through standard input/output and is used when integrating with MCP clients within the local system.

### 3. Run SSE-based Server

```bash
python sse_server.py
```

The SSE approach runs as a web-based service and provides the following endpoints:

- **SSE Stream**: `http://localhost:8000/sse`
- **Tools List**: `http://localhost:8000/tools`
- **Tool Call**: `http://localhost:8000/tools/call`
- **Resources List**: `http://localhost:8000/resources`
- **Resource Read**: `http://localhost:8000/resources/read`
- **Prompts List**: `http://localhost:8000/prompts`
- **Get Prompt**: `http://localhost:8000/prompts/get`

### 4. Run with Docker

```bash
# Run only SSE server
docker-compose up mcp-sse-server

# Run only stdio server
docker-compose up mcp-stdio-server

# Run all services
docker-compose up
```

## Available Features

### Tools

1. **calculator**: Performs mathematical calculations
   - Input: `{"expression": "2+2"}`
   - Output: `"Calculation result: 4"`

2. **echo**: Returns a message
   - Input: `{"message": "Hello World"}`
   - Output: `"Echo: Hello World"`

### Resources

1. **config.json**: Application configuration file
   - URI: `file://config.json`
   - MIME type: `application/json`

### Prompts

1. **code_review**: Code review prompt
   - Input: `{"code": "def hello(): print('Hello')"}`
   - Output: Structured prompt for code review

## Client Testing

### 1. Using Python Client

```bash
# Test stdio client
python stdio_client.py

# Test SSE client (SSE server must be running)
python sse_client.py

# Integrated test (all client tests)
python test_mcp.py

# Or use the convenient execution script
python run_tests.py              # All tests
python run_tests.py --stdio-only # stdio only
python run_tests.py --sse-only   # SSE only
```

### 2. API Usage Examples (curl)

```bash
# Use calculator tool
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "calculator", "arguments": {"expression": "2+2"}}'

# Use echo tool
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "echo", "arguments": {"message": "Hello MCP"}}'

# Read resource
curl "http://localhost:8000/resources/read?uri=file://config.json"

# Get prompt
curl -X POST http://localhost:8000/prompts/get \
  -H "Content-Type: application/json" \
  -d '{"name": "code_review", "arguments": {"code": "def hello(): print(\"Hello\")"}}'
```

## stdio vs SSE Comparison

| Aspect | stdio Method | SSE Method |
|--------|--------------|------------|
| **Communication** | Standard I/O | HTTP-based |
| **Environment** | Local system | Web service |
| **Complexity** | Simple | Complex |
| **Network Support** | None | Yes |
| **Real-time Streaming** | Limited | Supported |
| **Deployment** | Local execution | Web server deployment |

## Security Considerations

- The calculator tool uses the `eval()` function, so it's recommended to use a safer math parser in production environments.
- The SSE server is configured to allow CORS, so set appropriate CORS policies in production environments.

## References

- [Building MCP Server: Differences between stdio and SSE approaches](https://blog.choonzang.com/it/ai/3318/)
- [MCP Official Documentation](https://modelcontextprotocol.io/)