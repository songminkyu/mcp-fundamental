# sse_client.py
import asyncio
import aiohttp
import json
from typing import Dict, Any, List, Optional
import time


class MCPSseClient:
    """SSE 방식 MCP 클라이언트"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
        self.session = None
    
    async def connect(self):
        """HTTP 세션 생성"""
        try:
            self.session = aiohttp.ClientSession()
            print("✅ HTTP 세션이 생성되었습니다.")
            return True
        except Exception as e:
            print(f"❌ 세션 생성 실패: {e}")
            return False
    
    async def disconnect(self):
        """HTTP 세션 종료"""
        if self.session:
            await self.session.close()
            print("🔌 HTTP 세션이 종료되었습니다.")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 조회"""
        try:
            async with self.session.get(f"{self.base_url}/tools") as response:
                if response.status == 200:
                    tools = await response.json()
                    print(f"📋 사용 가능한 도구: {len(tools)}개")
                    for tool in tools:
                        print(f"  - {tool['name']}: {tool['description']}")
                    return tools
                else:
                    print(f"❌ 도구 목록 조회 실패: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ 도구 목록 조회 실패: {e}")
            return []
    
    async def call_tool(self, name: str, arguments: Dict[str, Any]) -> str:
        """도구 호출"""
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
                    print(f"🔧 도구 '{name}' 호출 결과:")
                    for content in result.get("result", []):
                        print(f"  {content.get('text', '')}")
                    return str(result)
                else:
                    error = await response.text()
                    print(f"❌ 도구 호출 실패: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ 도구 호출 실패: {e}")
            return ""
    
    async def list_resources(self) -> List[Dict[str, Any]]:
        """사용 가능한 리소스 목록 조회"""
        try:
            async with self.session.get(f"{self.base_url}/resources") as response:
                if response.status == 200:
                    resources = await response.json()
                    print(f"📁 사용 가능한 리소스: {len(resources)}개")
                    for resource in resources:
                        print(f"  - {resource['name']}: {resource['description']}")
                    return resources
                else:
                    print(f"❌ 리소스 목록 조회 실패: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ 리소스 목록 조회 실패: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """리소스 읽기"""
        try:
            params = {"uri": uri}
            async with self.session.get(
                f"{self.base_url}/resources/read",
                params=params
            ) as response:
                if response.status == 200:
                    result = await response.json()
                    content = result.get("content", "")
                    print(f"📖 리소스 '{uri}' 내용:")
                    print(f"  {content}")
                    return content
                else:
                    error = await response.text()
                    print(f"❌ 리소스 읽기 실패: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ 리소스 읽기 실패: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """사용 가능한 프롬프트 목록 조회"""
        try:
            async with self.session.get(f"{self.base_url}/prompts") as response:
                if response.status == 200:
                    prompts = await response.json()
                    print(f"💬 사용 가능한 프롬프트: {len(prompts)}개")
                    for prompt in prompts:
                        print(f"  - {prompt['name']}: {prompt['description']}")
                    return prompts
                else:
                    print(f"❌ 프롬프트 목록 조회 실패: HTTP {response.status}")
                    return []
        except Exception as e:
            print(f"❌ 프롬프트 목록 조회 실패: {e}")
            return []
    
    async def get_prompt(self, name: str, arguments: Dict[str, Any]) -> str:
        """프롬프트 가져오기"""
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
                    print(f"💭 프롬프트 '{name}' 내용:")
                    for message in result.get("messages", []):
                        content = message.get("content", {})
                        if isinstance(content, dict) and "text" in content:
                            print(f"  {content['text']}")
                    return str(result)
                else:
                    error = await response.text()
                    print(f"❌ 프롬프트 가져오기 실패: HTTP {response.status} - {error}")
                    return ""
        except Exception as e:
            print(f"❌ 프롬프트 가져오기 실패: {e}")
            return ""
    
    async def listen_sse(self, duration: int = 10):
        """SSE 스트림 수신 (지정된 시간 동안)"""
        try:
            print(f"📡 SSE 스트림 수신 시작 (최대 {duration}초)")
            async with self.session.get(f"{self.base_url}/sse") as response:
                if response.status == 200:
                    start_time = time.time()
                    async for line in response.content:
                        if time.time() - start_time > duration:
                            break
                        
                        line = line.decode('utf-8').strip()
                        if line.startswith('data: '):
                            data = line[6:]  # 'data: ' 제거
                            try:
                                event_data = json.loads(data)
                                print(f"📨 SSE 이벤트: {event_data}")
                            except json.JSONDecodeError:
                                print(f"📨 SSE 데이터: {data}")
                else:
                    print(f"❌ SSE 연결 실패: HTTP {response.status}")
        except Exception as e:
            print(f"❌ SSE 수신 실패: {e}")


async def test_sse_client():
    """SSE 클라이언트 테스트"""
    print("🚀 SSE MCP 클라이언트 테스트 시작")
    print("=" * 50)
    
    client = MCPSseClient()
    
    try:
        # 서버 연결
        if not await client.connect():
            return
        
        print("\n1️⃣ 도구 목록 조회")
        tools = await client.list_tools()
        
        print("\n2️⃣ 도구 호출 테스트")
        if tools:
            # calculator 도구 테스트
            await client.call_tool("calculator", {"expression": "2 + 3 * 4"})
            await client.call_tool("calculator", {"expression": "sqrt(16)"})
            
            # echo 도구 테스트
            await client.call_tool("echo", {"message": "Hello MCP SSE!"})
        
        print("\n3️⃣ 리소스 목록 조회")
        resources = await client.list_resources()
        
        print("\n4️⃣ 리소스 읽기 테스트")
        if resources:
            await client.read_resource("file://config.json")
        
        print("\n5️⃣ 프롬프트 목록 조회")
        prompts = await client.list_prompts()
        
        print("\n6️⃣ 프롬프트 가져오기 테스트")
        if prompts:
            await client.get_prompt("code_review", {
                "code": "def hello():\n    print('Hello, World!')"
            })
        
        print("\n7️⃣ SSE 스트림 테스트")
        await client.listen_sse(duration=5)
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_sse_client())
