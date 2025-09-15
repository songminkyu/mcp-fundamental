# MCP Fundamental Examples

This project is a collection of examples for learning the fundamental concepts and implementation methods of MCP (Model Context Protocol). It demonstrates how to implement MCP servers and clients through two different approaches.

## 📚 Project Structure

```
mcp-fundamental/
├── example-1/                  # Using basic MCP library
│   ├── ko/                     # Korean version
│   │   ├── stdio_server.py     # stdio method server
│   │   ├── sse_server.py       # SSE method server
│   │   ├── stdio_client.py     # stdio client
│   │   ├── sse_client.py       # SSE client
│   │   ├── test_mcp.py         # integrated tests
│   │   ├── run_tests.py        # test execution tool
│   │   └── README.md           # detailed documentation
│   └── en/                     # English version
│       └── [same files as ko/]
├── example-2/                  # Using FastMCP library
│   ├── ko/                     # Korean version
│   │   ├── stdio_server.py     # FastMCP stdio server
│   │   ├── sse_server.py       # FastMCP SSE server
│   │   ├── stdio_client.py     # stdio client
│   │   ├── sse_client.py       # SSE client
│   │   ├── test_mcp.py         # integrated tests
│   │   ├── run_tests.py        # test execution tool
│   │   └── README.md           # detailed documentation
│   └── en/                     # English version
│       └── [same files as ko/]
├── .gitignore              # Git ignore files
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
├── README.md               # This file (English)
└── README_ko.md            # Korean version
```

## 🎯 Learning Objectives

Through this project, you can learn:

1. **MCP Basic Concepts**: Understanding the core concepts of Model Context Protocol
2. **Two Implementation Approaches**: Comparison between basic MCP vs FastMCP
3. **Communication Methods**: Differences and use cases of STDIO vs SSE methods
4. **Actual Implementation**: Complete working server and client implementation
5. **Testing Methods**: Verification through automated testing

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone <repository-url>
cd mcp-fundamental
```

### 2. Choose Example

#### Example 1: Basic MCP Library
```bash
cd example-1/en  # or example-1/ko for Korean
pip install -r requirements.txt
python run_tests.py
```

#### Example 2: FastMCP Library
```bash
cd example-2/en  # or example-2/ko for Korean
pip install -r requirements.txt
python run_tests.py
```

## 📖 Example Features

### Example 1: Basic MCP Library

- **Library**: Standard MCP library
- **Complexity**: Medium (requires more configuration)
- **Learning Value**: Understanding internal workings of MCP
- **Suitable for**: When you want to deeply understand MCP details

**Key Features:**
- Manual server configuration
- Explicit tool/resource/prompt definitions
- Fine-grained control possible
- High educational value

### Example 2: FastMCP Library

- **Library**: FastMCP (modern MCP library)
- **Complexity**: Low (simple decorator usage)
- **Learning Value**: Rapid prototyping and modern development methods
- **Suitable for**: When you want to quickly build MCP servers

**Key Features:**
- Decorator-based simple syntax
- Automatic type inference
- Minimal code implementation
- Suitable for production environments

## 🔄 STDIO vs SSE Comparison

| Aspect | STDIO Method | SSE Method |
|--------|--------------|------------|
| **Communication** | Standard I/O | HTTP + Server-Sent Events |
| **Environment** | Local process | Web service |
| **Complexity** | Simple | Complex |
| **Network Support** | None | Yes |
| **Real-time Streaming** | Limited | Supported |
| **Scalability** | Limited | High |
| **Deployment** | Local execution | Web server deployment |
| **Use Cases** | Local tools, CLI | Web services, remote access |

## 🛠️ Available Features

### Tools
- **greet**: User greeting
- **add**: Add two numbers
- **multiply**: Multiply two numbers
- **calculate**: Calculate mathematical expressions
- **get_system_info**: Get system information
- **echo**: Return message
- **get_server_status**: Get server status (SSE only)

### Resources
- **config://settings**: Server configuration file
- **file://readme**: README resource

### Prompts
- **code_review**: Code review prompt
- **explain_code**: Code explanation prompt

## 🧪 Running Tests

### Individual Example Tests

```bash
# Example 1 tests
cd example-1/en  # or example-1/ko
python run_tests.py              # All tests
python run_tests.py --stdio-only # STDIO only
python run_tests.py --sse-only   # SSE only

# Example 2 tests
cd example-2/en  # or example-2/ko
python run_tests.py              # All tests
python run_tests.py --stdio-only # STDIO only
python run_tests.py --sse-only   # SSE only
```

### Individual Server/Client Execution

```bash
# Run server
python stdio_server.py    # STDIO server
python sse_server.py      # SSE server

# Run client
python stdio_client.py    # STDIO client
python sse_client.py      # SSE client
```

## 🐳 Using Docker

The project now supports multiple language and example combinations through Docker. You can run any combination of examples and languages.

### Available Services

| Service | Example | Language | Port | Description |
|---------|---------|----------|------|-------------|
| `mcp-sse-server-ex1-ko` | 1 | Korean | 8000 | Example 1 SSE server (Korean) |
| `mcp-stdio-server-ex1-ko` | 1 | Korean | - | Example 1 STDIO server (Korean) |
| `mcp-sse-server-ex1-en` | 1 | English | 8001 | Example 1 SSE server (English) |
| `mcp-stdio-server-ex1-en` | 1 | English | - | Example 1 STDIO server (English) |
| `mcp-sse-server-ex2-ko` | 2 | Korean | 8080 | Example 2 SSE server (Korean) |
| `mcp-stdio-server-ex2-ko` | 2 | Korean | - | Example 2 STDIO server (Korean) |
| `mcp-sse-server-ex2-en` | 2 | English | 8081 | Example 2 SSE server (English) |
| `mcp-stdio-server-ex2-en` | 2 | English | - | Example 2 STDIO server (English) |

**Note**: All services use the same root `requirements.txt` file for dependencies.

### Docker Commands

```bash
# Build the Docker image
docker-compose build

# Run specific services
docker-compose up mcp-sse-server-ex1-en          # Example 1 English SSE server
docker-compose up mcp-sse-server-ex2-ko          # Example 2 Korean SSE server
docker-compose up mcp-stdio-server-ex1-ko        # Example 1 Korean STDIO server

# Run all services
docker-compose up

# Run in background
docker-compose up -d

# Stop all services
docker-compose down
```

### Quick Start Examples

```bash
# Example 1 - English (Basic MCP)
docker-compose up mcp-sse-server-ex1-en
# Access at: http://localhost:8001

# Example 2 - Korean (FastMCP)
docker-compose up mcp-sse-server-ex2-ko
# Access at: http://localhost:8080

# Run both examples simultaneously
docker-compose up mcp-sse-server-ex1-en mcp-sse-server-ex2-ko
```

## 📚 Recommended Learning Order

1. **Understand Basic Concepts**: Understand what MCP is and why it's needed
2. **Run Example 1**: Execute examples implemented with basic MCP library
3. **Analyze Code**: Analyze server/client code in Example 1
4. **Run Example 2**: Execute examples implemented with FastMCP
5. **Compare Analysis**: Compare differences and pros/cons of both examples
6. **Add Your Own Tools**: Try adding new tools to existing examples

## 🔧 Troubleshooting

### Common Issues

1. **Dependency Installation Failure**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **Port Conflict (SSE Server)**
   - Use a different port if 8080 is in use
   - Change port number in `sse_server.py`

3. **STDIO Client Connection Failure**
   - Check Python path
   - Check server script path

4. **SSE Client Connection Failure**
   - Check if SSE server is running
   - Check firewall settings

### Debugging

```bash
# Run with detailed logs
python -u stdio_client.py
python -u sse_client.py
python -u test_mcp.py
```

## 📖 Additional Resources

- [MCP Official Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/pydantic/fastmcp)
- [Medium: MCP Clients: Stdio vs SSE](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)

## 🤝 Contributing

Please register bug reports, feature suggestions, or improvements as issues.

## 📄 License

This project is written for educational purposes.

---

**Happy Learning! 🎉**

Welcome to the world of MCP. Experience the power and flexibility of MCP through these examples!


