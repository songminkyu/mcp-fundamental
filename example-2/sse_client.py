# sse_client.py
"""
FastMCP를 사용한 SSE 방식 MCP 클라이언트
Medium 글의 예제를 기반으로 구현
"""

import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from typing import List, Dict, Any


class MCPSseClient:
    """SSE 방식 MCP 클라이언트"""
    
    def __init__(self, server_url: str = "http://localhost:8080/sse"):
        self.server_url = server_url
        self.session = None
    
    async def connect(self) -> bool:
        """MCP 서버에 연결"""
        try:
            print(f"🔌 SSE 서버에 연결 중: {self.server_url}")
            
            # SSE 전송을 통한 연결 생성
            self.streams = await sse_client(url=self.server_url).__aenter__()
            
            # 클라이언트 세션 생성
            self.session = ClientSession(*self.streams)
            await self.session.__aenter__()
            
            # 세션 초기화
            await self.session.initialize()
            
            print("✅ SSE 서버에 성공적으로 연결되었습니다.")
            return True
            
        except Exception as e:
            print(f"❌ SSE 서버 연결 실패: {e}")
            return False
    
    async def disconnect(self):
        """MCP 서버 연결 해제"""
        try:
            if self.session:
                await self.session.__aexit__(None, None, None)
            if hasattr(self, 'streams'):
                await self.streams.__aexit__(None, None, None)
            print("🔌 SSE 서버 연결이 해제되었습니다.")
        except Exception as e:
            print(f"⚠️ 연결 해제 중 오류: {e}")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 조회"""
        try:
            response = await self.session.list_tools()
            tools = [{"name": tool.name, "description": tool.description} for tool in response.tools]
            print(f"📋 사용 가능한 도구: {len(tools)}개")
            for tool in tools:
                print(f"  - {tool['name']}: {tool['description']}")
            return tools
        except Exception as e:
            print(f"❌ 도구 목록 조회 실패: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """도구 호출"""
        try:
            result = await self.session.call_tool(name, arguments)
            print(f"🔧 도구 '{name}' 호출 결과:")
            for content in result.content:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            return str(result.content)
        except Exception as e:
            print(f"❌ 도구 호출 실패: {e}")
            return ""
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """사용 가능한 리소스 목록 조회"""
        try:
            response = await self.session.list_resources()
            resources = [{"uri": res.uri, "name": res.name, "description": res.description} for res in response.resources]
            print(f"📁 사용 가능한 리소스: {len(resources)}개")
            for resource in resources:
                print(f"  - {resource['name']} ({resource['uri']}): {resource['description']}")
            return resources
        except Exception as e:
            print(f"❌ 리소스 목록 조회 실패: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """리소스 읽기"""
        try:
            result = await self.session.read_resource(uri)
            print(f"📖 리소스 '{uri}' 내용:")
            for content in result.contents:
                if hasattr(content, 'text'):
                    print(f"  {content.text}")
            return str(result.contents)
        except Exception as e:
            print(f"❌ 리소스 읽기 실패: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """사용 가능한 프롬프트 목록 조회"""
        try:
            response = await self.session.list_prompts()
            prompts = [{"name": prompt.name, "description": prompt.description} for prompt in response.prompts]
            print(f"💬 사용 가능한 프롬프트: {len(prompts)}개")
            for prompt in prompts:
                print(f"  - {prompt['name']}: {prompt['description']}")
            return prompts
        except Exception as e:
            print(f"❌ 프롬프트 목록 조회 실패: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        """프롬프트 가져오기"""
        try:
            result = await self.session.get_prompt(name, arguments)
            print(f"💭 프롬프트 '{name}' 내용:")
            for message in result.messages:
                if hasattr(message.content, 'text'):
                    print(f"  {message.content.text}")
            return str(result.messages)
        except Exception as e:
            print(f"❌ 프롬프트 가져오기 실패: {e}")
            return ""


async def test_sse_client():
    """SSE 클라이언트 테스트"""
    print("🚀 SSE MCP 클라이언트 테스트 시작")
    print("=" * 60)
    
    client = MCPSseClient()
    
    try:
        # 서버 연결
        if not await client.connect():
            print("⚠️ SSE 서버가 실행 중인지 확인해주세요. (python sse_server.py)")
            return
        
        print("\n1️⃣ 도구 목록 조회")
        tools = await client.list_tools()
        
        print("\n2️⃣ 도구 호출 테스트")
        if tools:
            # greet 도구 테스트
            await client.call_tool("greet", {"name": "Bob"})
            
            # add 도구 테스트
            await client.call_tool("add", {"a": 10, "b": 32})
            
            # multiply 도구 테스트
            await client.call_tool("multiply", {"a": 4.5, "b": 2.5})
            
            # calculate 도구 테스트
            await client.call_tool("calculate", {"expression": "pow(2, 3) + sqrt(25)"})
            
            # get_system_info 도구 테스트
            await client.call_tool("get_system_info", {})
            
            # get_server_status 도구 테스트
            await client.call_tool("get_server_status", {})
            
            # echo 도구 테스트
            await client.call_tool("echo", {"message": "Hello from SSE client!"})
        
        print("\n3️⃣ 리소스 목록 조회")
        resources = await client.list_resources()
        
        print("\n4️⃣ 리소스 읽기 테스트")
        if resources:
            await client.read_resource("config://settings")
            await client.read_resource("file://readme")
        
        print("\n5️⃣ 프롬프트 목록 조회")
        prompts = await client.list_prompts()
        
        print("\n6️⃣ 프롬프트 가져오기 테스트")
        if prompts:
            await client.get_prompt("code_review", {
                "code": "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[len(arr) // 2]\n    left = [x for x in arr if x < pivot]\n    middle = [x for x in arr if x == pivot]\n    right = [x for x in arr if x > pivot]\n    return quicksort(left) + middle + quicksort(right)",
                "language": "python"
            })
            
            await client.get_prompt("explain_code", {
                "code": "async def fetch_data(url):\n    async with aiohttp.ClientSession() as session:\n        async with session.get(url) as response:\n            return await response.json()",
                "language": "python"
            })
        
        print("\n✅ 모든 SSE 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_sse_client())
