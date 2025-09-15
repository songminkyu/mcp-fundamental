# stdio_client.py
import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client


class MCPStdioClient:
    """STDIO-based MCP client"""
    
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
    
    async def connect(self):
        """Connect to MCP server"""
        try:
            # Create stdio client
            self.session = await stdio_client(self.server_command)
            print("✅ Connected to MCP server.")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def disconnect(self):
        """Disconnect from MCP server"""
        if self.session:
            await self.session.close()
            print("🔌 MCP server connection closed.")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        try:
            tools = await self.session.list_tools()
            print(f"📋 Available tools: {len(tools.tools)}")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            return tools.tools
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
            resources = await self.session.list_resources()
            print(f"📁 Available resources: {len(resources.resources)}")
            for resource in resources.resources:
                print(f"  - {resource.name}: {resource.description}")
            return resources.resources
        except Exception as e:
            print(f"❌ Failed to get resource list: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        try:
            result = await self.session.read_resource(uri)
            print(f"📖 Resource '{uri}' content:")
            print(f"  {result.contents[0].text}")
            return result.contents[0].text
        except Exception as e:
            print(f"❌ Failed to read resource: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """Get list of available prompts"""
        try:
            prompts = await self.session.list_prompts()
            print(f"💬 Available prompts: {len(prompts.prompts)}")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            return prompts.prompts
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
    print("=" * 50)
    
    # stdio server command (run stdio_server.py)
    server_command = [sys.executable, "stdio_server.py"]
    
    client = MCPStdioClient(server_command)
    
    try:
        # Connect to server
        if not await client.connect():
            return
        
        print("\n1️⃣ Get tool list")
        tools = await client.list_tools()
        
        print("\n2️⃣ Tool call test")
        if tools:
            # Test calculator tool
            await client.call_tool("calculator", {"expression": "2 + 3 * 4"})
            await client.call_tool("calculator", {"expression": "sqrt(16)"})
            
            # Test echo tool
            await client.call_tool("echo", {"message": "Hello MCP!"})
        
        print("\n3️⃣ Get resource list")
        resources = await client.list_resources()
        
        print("\n4️⃣ Resource read test")
        if resources:
            await client.read_resource("file://config.json")
        
        print("\n5️⃣ Get prompt list")
        prompts = await client.list_prompts()
        
        print("\n6️⃣ Get prompt test")
        if prompts:
            await client.get_prompt("code_review", {
                "code": "def hello():\n    print('Hello, World!')"
            })
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_stdio_client())
