# test_mcp.py
"""
MCP server integrated test using FastMCP
Implemented based on Medium article examples
"""

import asyncio
import subprocess
import time
import signal
import sys
import os
from stdio_client import MCPStdioClient
from sse_client import MCPSseClient


class MCPTester:
    """MCP server integrated test class"""
    
    def __init__(self):
        self.sse_process = None
        self.stdio_client = None
        self.sse_client = None
    
    def start_sse_server(self):
        """Start SSE server"""
        try:
            print("🚀 Starting SSE server...")
            self.sse_process = subprocess.Popen(
                [sys.executable, "sse_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a moment for server to start
            time.sleep(3)
            
            # Check if server is running
            if self.sse_process.poll() is None:
                print("✅ SSE server started successfully.")
                return True
            else:
                stdout, stderr = self.sse_process.communicate()
                print(f"❌ SSE server start failed:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
        except Exception as e:
            print(f"❌ Error starting SSE server: {e}")
            return False
    
    def stop_sse_server(self):
        """Stop SSE server"""
        if self.sse_process:
            try:
                print("🛑 Stopping SSE server...")
                self.sse_process.terminate()
                self.sse_process.wait(timeout=5)
                print("✅ SSE server stopped.")
            except subprocess.TimeoutExpired:
                print("⚠️ Force killing...")
                self.sse_process.kill()
                self.sse_process.wait()
            except Exception as e:
                print(f"❌ Error stopping SSE server: {e}")
    
    async def test_stdio_client(self):
        """STDIO client test"""
        print("\n" + "="*60)
        print("📱 STDIO Client Test (FastMCP)")
        print("="*60)
        
        try:
            self.stdio_client = MCPStdioClient()
            
            # Connection test
            if not await self.stdio_client.connect():
                return False
            
            # Tool test
            print("\n🔧 Tool Test")
            tools = await self.stdio_client.list_tools()
            if tools:
                await self.stdio_client.call_tool("greet", {"name": "Alice"})
                await self.stdio_client.call_tool("add", {"a": 15, "b": 25})
                await self.stdio_client.call_tool("multiply", {"a": 3.14, "b": 2.0})
                await self.stdio_client.call_tool("calculate", {"expression": "sqrt(144) + 2**3"})
                await self.stdio_client.call_tool("echo", {"message": "STDIO FastMCP test"})
            
            # Resource test
            print("\n📁 Resource Test")
            resources = await self.stdio_client.list_resources()
            if resources:
                await self.stdio_client.read_resource("config://settings")
                await self.stdio_client.read_resource("file://readme")
            
            # Prompt test
            print("\n💬 Prompt Test")
            prompts = await self.stdio_client.list_prompts()
            if prompts:
                await self.stdio_client.get_prompt("code_review", {
                    "code": "def factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n-1)",
                    "language": "python"
                })
            
            await self.stdio_client.disconnect()
            print("✅ STDIO client test completed")
            return True
            
        except Exception as e:
            print(f"❌ STDIO client test failed: {e}")
            return False
    
    async def test_sse_client(self):
        """SSE client test"""
        print("\n" + "="*60)
        print("🌐 SSE Client Test (FastMCP)")
        print("="*60)
        
        try:
            self.sse_client = MCPSseClient()
            
            # Connection test
            if not await self.sse_client.connect():
                return False
            
            # Tool test
            print("\n🔧 Tool Test")
            tools = await self.sse_client.list_tools()
            if tools:
                await self.sse_client.call_tool("greet", {"name": "Bob"})
                await self.sse_client.call_tool("add", {"a": 100, "b": 200})
                await self.sse_client.call_tool("multiply", {"a": 7.5, "b": 4.0})
                await self.sse_client.call_tool("calculate", {"expression": "log(100) + sin(pi/2)"})
                await self.sse_client.call_tool("get_server_status", {})
                await self.sse_client.call_tool("echo", {"message": "SSE FastMCP test"})
            
            # Resource test
            print("\n📁 Resource Test")
            resources = await self.sse_client.list_resources()
            if resources:
                await self.sse_client.read_resource("config://settings")
                await self.sse_client.read_resource("file://readme")
            
            # Prompt test
            print("\n💬 Prompt Test")
            prompts = await self.sse_client.list_prompts()
            if prompts:
                await self.sse_client.get_prompt("code_review", {
                    "code": "class Node:\n    def __init__(self, data):\n        self.data = data\n        self.next = None\n\nclass LinkedList:\n    def __init__(self):\n        self.head = None",
                    "language": "python"
                })
            
            await self.sse_client.disconnect()
            print("✅ SSE client test completed")
            return True
            
        except Exception as e:
            print(f"❌ SSE client test failed: {e}")
            return False
    
    async def run_all_tests(self):
        """Run all tests"""
        print("🧪 FastMCP MCP Server Integrated Test Started")
        print("="*60)
        print("📚 Implementation based on Medium article examples")
        print("🔗 https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb")
        
        results = {
            "stdio": False,
            "sse": False
        }
        
        try:
            # STDIO test (no server startup needed)
            results["stdio"] = await self.test_stdio_client()
            
            # Start SSE server
            if not self.start_sse_server():
                print("❌ SSE server start failed, skipping SSE test.")
                results["sse"] = False
            else:
                # SSE test
                results["sse"] = await self.test_sse_client()
            
        except KeyboardInterrupt:
            print("\n⚠️ Test interrupted by user.")
        except Exception as e:
            print(f"❌ Error during test execution: {e}")
        finally:
            # Cleanup
            self.stop_sse_server()
        
        # Result summary
        print("\n" + "="*60)
        print("📊 Test Result Summary")
        print("="*60)
        print(f"STDIO Client (FastMCP): {'✅ Success' if results['stdio'] else '❌ Failed'}")
        print(f"SSE Client (FastMCP): {'✅ Success' if results['sse'] else '❌ Failed'}")
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        
        print(f"\nOverall result: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 All FastMCP tests completed successfully!")
            print("📖 Medium article examples are working correctly.")
        else:
            print("⚠️ Some tests failed. Please check the logs.")
        
        return results


def signal_handler(signum, frame):
    """Signal handler (Ctrl+C handling)"""
    print("\n⚠️ Test interrupted.")
    sys.exit(0)


async def main():
    """Main function"""
    # Register signal handler
    signal.signal(signal.SIGINT, signal_handler)
    
    tester = MCPTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
