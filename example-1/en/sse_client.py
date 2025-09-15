# sse_client.py
import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
import time


class MCPSseClient:
    """SSE-based MCP client"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = None
    
    async def connect(self):
        """Create HTTP session"""
        try:
            self.session = aiohttp.ClientSession()
            print("✅ HTTP session created.")
            return True
        except Exception as e:
            print(f"❌ Session creation failed: {e}")
            return False
    
    async def disconnect(self):
        """Close HTTP session"""
        if self.session:
            await self.session.close()
            print("🔌 HTTP session closed.")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """Get list of available tools"""
        try:
            async with self.session.get(f"{self.base_url}/tools") as response:
                if response.status == 200:
                    tools = await response.json()
                    print(f"📋 Available tools: {len(tools)}")
                    for tool in tools:
                        print(f"  - {tool['name']}: {tool['description']}")
                    return tools
                else:
                    print(f"❌ Failed to get tool list: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Failed to get tool list: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """Call a tool"""
        try:
            payload = {
                "name": name,
                "arguments": arguments
            }
            async with self.session.post(
                f"{self.base_url}/tools/call",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"🔧 Tool '{name}' call result:")
                    for content in result.get("result", []):
                        print(f"  {content.get('text', '')}")
                    return str(result)
                else:
                    error = await response.text()
                    print(f"❌ Tool call failed: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ Tool call failed: {e}")
            return ""
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """Get list of available resources"""
        try:
            async with self.session.get(f"{self.base_url}/resources") as response:
                if response.status == 200:
                    resources = await response.json()
                    print(f"📁 Available resources: {len(resources)}")
                    for resource in resources:
                        print(f"  - {resource['name']}: {resource['description']}")
                    return resources
                else:
                    print(f"❌ Failed to get resource list: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Failed to get resource list: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """Read a resource"""
        try:
            params = {"uri": uri}
            async with self.session.get(
                f"{self.base_url}/resources/read",
                params=params
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result.get("content", "")
                    print(f"📖 Resource '{uri}' content:")
                    print(f"  {content}")
                    return content
                else:
                    error = await response.text()
                    print(f"❌ Failed to read resource: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ Failed to read resource: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """Get list of available prompts"""
        try:
            async with self.session.get(f"{self.base_url}/prompts") as response:
                if response.status == 200:
                    prompts = await response.json()
                    print(f"💬 Available prompts: {len(prompts)}")
                    for prompt in prompts:
                        print(f"  - {prompt['name']}: {prompt['description']}")
                    return prompts
                else:
                    print(f"❌ Failed to get prompt list: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ Failed to get prompt list: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        """Get a prompt"""
        try:
            payload = {
                "name": name,
                "arguments": arguments
            }
            async with self.session.post(
                f"{self.base_url}/prompts/get",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    print(f"💭 Prompt '{name}' content:")
                    for message in result.get("messages", []):
                        content = message.get("content", {})
                        if isinstance(content, dict) and "text" in content:
                            print(f"  {content['text']}")
                    return str(result)
                else:
                    error = await response.text()
                    print(f"❌ Failed to get prompt: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ Failed to get prompt: {e}")
            return ""
    
    async def listen_sse(self, duration: int = 10):
        """Listen to SSE stream (for specified duration)"""
        try:
            print(f"📡 SSE stream listening started (max {duration} seconds)")
            async with self.session.get(f"{self.base_url}/sse") as response:
                if response.status == 200:
                    start_time = time.time()
                    async for line in response.content:
                        if time.time() - start_time > duration:
                            break
                        
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = line[6:]  # Remove 'data: '
                            try:
                                event_data = json.loads(data)
                                print(f"📨 SSE event: {event_data}")
                            except json.JSONDecodeError:
                                print(f"📨 SSE data: {data}")
                else:
                    print(f"❌ SSE connection failed: HTTP {response.status}")
        except Exception as e:
            print(f"❌ SSE listening failed: {e}")


async def test_sse_client():
    """SSE client test"""
    print("🚀 SSE MCP client test started")
    print("=" * 50)
    
    client = MCPSseClient()
    
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
            await client.call_tool("echo", {"message": "Hello MCP SSE!"})
        
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
        
        print("\n7️⃣ SSE stream test")
        await client.listen_sse(duration=5)
        
        print("\n✅ All tests completed!")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_sse_client())
