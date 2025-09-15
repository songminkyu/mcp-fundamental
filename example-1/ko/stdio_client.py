# stdio_client.py
import asyncio
import json
import subprocess
import sys
from typing import Dict, Any, List
from mcp.client import ClientSession
from mcp.client.stdio import stdio_client


class MCPStdioClient:
    """stdio 방식 MCP 클라이언트"""
    
    def __init__(self, server_command: List[str]):
        self.server_command = server_command
        self.session = None
    
    async def connect(self):
        """MCP 서버에 연결"""
        try:
            # stdio 클라이언트 생성
            self.session = await stdio_client(self.server_command)
            print("✅ MCP 서버에 연결되었습니다.")
            return True
        except Exception as e:
            print(f"❌ 연결 실패: {e}")
            return False
    
    async def disconnect(self):
        """MCP 서버 연결 해제"""
        if self.session:
            await self.session.close()
            print("🔌 MCP 서버 연결이 해제되었습니다.")
    
    async def list_tools(self) -> List[Dict[str, Any]]:
        """사용 가능한 도구 목록 조회"""
        try:
            tools = await self.session.list_tools()
            print(f"📋 사용 가능한 도구: {len(tools.tools)}개")
            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")
            return tools.tools
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
            resources = await self.session.list_resources()
            print(f"📁 사용 가능한 리소스: {len(resources.resources)}개")
            for resource in resources.resources:
                print(f"  - {resource.name}: {resource.description}")
            return resources.resources
        except Exception as e:
            print(f"❌ 리소스 목록 조회 실패: {e}")
            return []
    
    async def read_resource(self, uri: str) -> str:
        """리소스 읽기"""
        try:
            result = await self.session.read_resource(uri)
            print(f"📖 리소스 '{uri}' 내용:")
            print(f"  {result.contents[0].text}")
            return result.contents[0].text
        except Exception as e:
            print(f"❌ 리소스 읽기 실패: {e}")
            return ""
    
    async def list_prompts(self) -> List[Dict[str, Any]]:
        """사용 가능한 프롬프트 목록 조회"""
        try:
            prompts = await self.session.list_prompts()
            print(f"💬 사용 가능한 프롬프트: {len(prompts.prompts)}개")
            for prompt in prompts.prompts:
                print(f"  - {prompt.name}: {prompt.description}")
            return prompts.prompts
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


async def test_stdio_client():
    """stdio 클라이언트 테스트"""
    print("🚀 stdio MCP 클라이언트 테스트 시작")
    print("=" * 50)
    
    # stdio 서버 명령어 (stdio_server.py 실행)
    server_command = [sys.executable, "stdio_server.py"]
    
    client = MCPStdioClient(server_command)
    
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
            await client.call_tool("echo", {"message": "Hello MCP!"})
        
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
        
        print("\n✅ 모든 테스트가 완료되었습니다!")
        
    except Exception as e:
        print(f"❌ 테스트 중 오류 발생: {e}")
    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(test_stdio_client())
