# run_tests.py
"""
FastMCP MCP server test execution tool
Implemented based on Medium article examples
"""

import asyncio
import sys
import os
from test_mcp import MCPTester


def print_usage():
    """Print usage"""
    print("""
🧪 FastMCP MCP Server Test Tool

Implementation based on Medium article: https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb

Usage:
  python run_tests.py [options]

Options:
  --stdio-only    Test only STDIO client
  --sse-only      Test only SSE client
  --help          Show this help

Examples:
  python run_tests.py              # Run all tests
  python run_tests.py --stdio-only # Test only STDIO
  python run_tests.py --sse-only   # Test only SSE

Individual execution:
  python stdio_server.py           # Run STDIO server
  python sse_server.py             # Run SSE server
  python stdio_client.py           # Test STDIO client
  python sse_client.py             # Test SSE client
""")


async def main():
    """Main function"""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        return
    
    tester = MCPTester()
    
    if "--stdio-only" in args:
        print("📱 Testing only STDIO client.")
        await tester.test_stdio_client()
    elif "--sse-only" in args:
        print("🌐 Testing only SSE client.")
        if tester.start_sse_server():
            try:
                await tester.test_sse_client()
            finally:
                tester.stop_sse_server()
        else:
            print("❌ SSE server start failed")
    else:
        print("🧪 Running all FastMCP tests.")
        await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
