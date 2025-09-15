# sse_client.py
"""
SSE-based MCP client using FastMCP
Implemented based on Medium article examples
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import List, Dict, Any


class MCPSseClient:
    """SSE-based MCP client"""
    
    def __init__(self, server_url: str = "http://localhost:8080/sse"):
        self.server_url = server_url
        self.session = None
    
    async def connect(self) -> bool:
        """Connect to MCP server"""
        try:
            print(f"🔌 Connecting to SSE server: {self.server_url}")
            
            # Create connection through SSE transport
            self.streams = await sse_client(url=self.server_url).__aenter__()
            
            # Create client session
            self.session = ClientSession(*self.streams)
            await self.session.__aenter__()
            
            # Initialize session
            await self.session.initialize()
            
            print("✅ Successfully connected to SSE server.")
            return True
            
        except Exception as e:
            print(f"❌ SSE server connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
            if hasattr(self, 'streams'):
                await self.streams.__aexit__(None, None, None)
            print("🔌 SSE server connection closed.")
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


async def test_sse_client():
    """SSE client test"""
    print("🚀 SSE MCP client test started")
    print("=" * 60)
    
    client = MCPSseClient()
    
    try:
        # Connect to server
        if not await client.connect():
            print("⚠️ Please check if SSE server is running. (python sse_server.py)")
            return
        
        print("\n1️⃣ Get tool list")
        tools = await client.list_tools()
        
        print("\n2️⃣ Tool call test")
        if tools:
            # Test greet tool
            await client.call_tool("greet", {"name": "Bob"})
            
            # Test add tool
            await client.call_tool("add", {"a": 10, "b": 32})
            
            # Test multiply tool
            await client.call_tool("multiply", {"a": 4.5, "b": 2.5})
            
            # Test calculate tool
            await client.call_tool("calculate", {"expression": "pow(2, 3) + sqrt(25)"})
            
            # Test get_system_info tool
            await client.call_tool("get_system_info", {})
            
            # Test get_server_status tool
            await client.call_tool("get_server_status", {})
            
            # Test echo tool
            await client.call_tool("echo", {"message": "Hello from SSE client!"})
        
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
                "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
                "language": "python"
            })
            
            await client.get_prompt("explain_code", {
                "code": "async def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.json()",
                "language": "python"
            })
        
        print("\n✅ All SSE tests completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_sse_client())
