# stdio_client.py
"""
STDIO-based MCP client using FastMCP
Implemented based on Medium article examples
"""

import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from typing import List, Dict, Any


class MCPStdioClient:
    """STDIO-based MCP client"""
    
    def __init__(self, server_script: str = "stdio_server.py"):
        self.server_script = server_script
        self.session = None
    
    async def connect(self) -> bool:
        """Connect to MCP server"""
        try:
            # Set server script path
            current_dir = os.path.dirname(os.path.abspath(__file__))
            server_path = os.path.join(current_dir, self.server_script)
            
            # Create server parameters
            server_params = StdioServerParameters(
                command="python",
                args=[server_path]
            )
            
            print(f"🔌 Connecting to STDIO server: {server_path}")
            
            # Create connection through stdio transport
            self.streams = await stdio_client(server_params).__aenter__()
            
            # Create client session
            self.session = ClientSession(*self.streams)
            await self.session.__aenter__()
            
            # Initialize session
            await self.session.initialize()
            
            print("✅ Successfully connected to STDIO server.")
            return True
            
        except Exception as e:
            print(f"❌ STDIO server connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
            if hasattr(self, 'streams'):
                await self.streams.__aexit__(None, None, None)
            print("🔌 STDIO server connection closed.")
        except Exception as e:
            print(f"⚠️ Error during disconnection: {e}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        try:
            response = await self.session.list_tools()
            tools = [{"name": tool.name, "description": tool.description} for tool in response.tools]
            print(f"📋 Available tools: {len(tools)}")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            return tools
        except Exception as e:
            print(f"❌ Failed to get tool list: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool"""
        try:
            result = await self.session.call_tool(name, arguments)
            print(f"🔧 Tool '{name}' call result:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            return str(result.content)
        except Exception as e:
            print(f"❌ Tool call failed: {e}")
            return ""
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Get list of available resources"""
        try:
            response = await self.session.list_resources()
            resources = [{"uri": res.uri, "name": res.name, "description": res.description} for res in response.resources]
            print(f"📁 Available resources: {len(resources)}")
            for resource in resources:
                print(f"  - {resource['name']} ({resource['uri']}): {resource['description']}")
            return resources
        except Exception as e:
            print(f"❌ Failed to get resource list: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        try:
            result = await self.session.read_resource(uri)
            print(f"📖 Resource '{uri}' content:")
            for content in result.contents:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            return str(result.contents)
        except Exception as e:
            print(f"❌ Failed to read resource: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """Get list of available prompts"""
        try:
            response = await self.session.list_prompts()
            prompts = [{"name": prompt.name, "description": prompt.description} for prompt in response.prompts]
            print(f"💬 Available prompts: {len(prompts)}")
            for prompt in prompts:
                print(f"  - {prompt['name']}: {prompt['description']}")
            return prompts
        except Exception as e:
            print(f"❌ Failed to get prompt list: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        """Get a prompt"""
        try:
            result = await self.session.get_prompt(name, arguments)
            print(f"💭 Prompt '{name}' content:")
            for message in result.messages:
                if hasattr(message.content, 'text'):
                    print(f"  {message.content.text}")
            return str(result.messages)
        except Exception as e:
            print(f"❌ Failed to get prompt: {e}")
            return ""


async def test_stdio_client():
    """STDIO client test"""
    print("🚀 STDIO MCP client test started")
    print("=" * 60)
    
    client = MCPStdioClient()
    
    try:
        # Connect to server
        if not await client.connect():
            return
        
        print("\n1️⃣ Get tool list")
        tools = await client.list_tools()
        
        print("\n2️⃣ Tool call test")
        if tools:
            # Test greet tool
            await client.call_tool("greet", {"name": "Alice"})
            
            # Test add tool
            await client.call_tool("add", {"a": 5, "b": 7})
            
            # Test multiply tool
            await client.call_tool("multiply", {"a": 3.5, "b": 2.0})
            
            # Test calculate tool
            await client.call_tool("calculate", {"expression": "sqrt(16) + 2 * 3"})
            
            # Test get_system_info tool
            await client.call_tool("get_system_info", {})
            
            # Test echo tool
            await client.call_tool("echo", {"message": "Hello from STDIO client!"})
        
        print("\n3️⃣ Get resource list")
        resources = await client.list_resources()
        
        print("\n4️⃣ Resource read test")
        if resources:
            await client.read_resource("config://settings")
            await client.read_resource("file://readme")
        
        print("\n5️⃣ Get prompt list")
        prompts = await client.list_prompts()
        
        print("\n6️⃣ Get prompt test")
        if prompts:
            await client.get_prompt("code_review", {
                "code": "def hello():\n    print('Hello, World!')",
                "language": "python"
            })
            
            await client.get_prompt("explain_code", {
                "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)",
                "language": "python"
            })
        
        print("\n✅ All STDIO tests completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_stdio_client())
