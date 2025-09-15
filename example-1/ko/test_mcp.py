# test_mcp.py
import asyncio
import subprocess
import time
import signal
import sys
import os
from stdio_client import MCPStdioClient
from sse_client import MCPSseClient


class MCPTester:
    """MCP 서버 통합 테스트 클래스"""
    
    def __init__(self):
        self.sse_process = None
        self.stdio_client = None
        self.sse_client = None
    
    def start_sse_server(self):
        """SSE 서버 시작"""
        try:
            print("🚀 SSE 서버 시작 중...")
            self.sse_process = subprocess.Popen(
                [sys.executable, "sse_server.py"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # 서버가 시작될 때까지 잠시 대기
            time.sleep(3)
            
            # 서버가 실행 중인지 확인
            if self.sse_process.poll() is None:
                print("✅ SSE 서버가 성공적으로 시작되었습니다.")
                return True
            else:
                stdout, stderr = self.sse_process.communicate()
                print(f"❌ SSE 서버 시작 실패:")
                print(f"STDOUT: {stdout}")
                print(f"STDERR: {stderr}")
                return False
        except Exception as e:
            print(f"❌ SSE 서버 시작 중 오류: {e}")
            return False
    
    def stop_sse_server(self):
        """SSE 서버 중지"""
        if self.sse_process:
            try:
                print("🛑 SSE 서버 중지 중...")
                self.sse_process.terminate()
                self.sse_process.wait(timeout=5)
                print("✅ SSE 서버가 중지되었습니다.")
            except subprocess.TimeoutExpired:
                print("⚠️ 강제 종료 중...")
                self.sse_process.kill()
                self.sse_process.wait()
            except Exception as e:
                print(f"❌ SSE 서버 중지 중 오류: {e}")
    
    async def test_stdio_client(self):
        """stdio 클라이언트 테스트"""
        print("\n" + "="*60)
        print("📱 STDIO 클라이언트 테스트")
        print("="*60)
        
        try:
            server_command = [sys.executable, "stdio_server.py"]
            self.stdio_client = MCPStdioClient(server_command)
            
            # 연결 테스트
            if not await self.stdio_client.connect():
                return False
            
            # 도구 테스트
            print("\n🔧 도구 테스트")
            tools = await self.stdio_client.list_tools()
            if tools:
                await self.stdio_client.call_tool("calculator", {"expression": "10 + 5"})
                await self.stdio_client.call_tool("echo", {"message": "stdio 테스트"})
            
            # 리소스 테스트
            print("\n📁 리소스 테스트")
            resources = await self.stdio_client.list_resources()
            if resources:
                await self.stdio_client.read_resource("file://config.json")
            
            # 프롬프트 테스트
            print("\n💬 프롬프트 테스트")
            prompts = await self.stdio_client.list_prompts()
            if prompts:
                await self.stdio_client.get_prompt("code_review", {
                    "code": "def test():\n    return 'stdio test'"
                })
            
            await self.stdio_client.disconnect()
            print("✅ stdio 클라이언트 테스트 완료")
            return True
            
        except Exception as e:
            print(f"❌ stdio 클라이언트 테스트 실패: {e}")
            return False
    
    async def test_sse_client(self):
        """SSE 클라이언트 테스트"""
        print("\n" + "="*60)
        print("🌐 SSE 클라이언트 테스트")
        print("="*60)
        
        try:
            self.sse_client = MCPSseClient()
            
            # 연결 테스트
            if not await self.sse_client.connect():
                return False
            
            # 도구 테스트
            print("\n🔧 도구 테스트")
            tools = await self.sse_client.list_tools()
            if tools:
                await self.sse_client.call_tool("calculator", {"expression": "20 * 3"})
                await self.sse_client.call_tool("echo", {"message": "SSE 테스트"})
            
            # 리소스 테스트
            print("\n📁 리소스 테스트")
            resources = await self.sse_client.list_resources()
            if resources:
                await self.sse_client.read_resource("file://config.json")
            
            # 프롬프트 테스트
            print("\n💬 프롬프트 테스트")
            prompts = await self.sse_client.list_prompts()
            if prompts:
                await self.sse_client.get_prompt("code_review", {
                    "code": "def test():\n    return 'SSE test'"
                })
            
            # SSE 스트림 테스트
            print("\n📡 SSE 스트림 테스트")
            await self.sse_client.listen_sse(duration=3)
            
            await self.sse_client.disconnect()
            print("✅ SSE 클라이언트 테스트 완료")
            return True
            
        except Exception as e:
            print(f"❌ SSE 클라이언트 테스트 실패: {e}")
            return False
    
    async def run_all_tests(self):
        """모든 테스트 실행"""
        print("🧪 MCP 서버 통합 테스트 시작")
        print("="*60)
        
        results = {
            "stdio": False,
            "sse": False
        }
        
        try:
            # stdio 테스트 (서버 시작 불필요)
            results["stdio"] = await self.test_stdio_client()
            
            # SSE 서버 시작
            if not self.start_sse_server():
                print("❌ SSE 서버 시작 실패로 SSE 테스트를 건너뜁니다.")
                results["sse"] = False
            else:
                # SSE 테스트
                results["sse"] = await self.test_sse_client()
            
        except KeyboardInterrupt:
            print("\n⚠️ 사용자에 의해 테스트가 중단되었습니다.")
        except Exception as e:
            print(f"❌ 테스트 실행 중 오류: {e}")
        finally:
            # 정리
            self.stop_sse_server()
        
        # 결과 요약
        print("\n" + "="*60)
        print("📊 테스트 결과 요약")
        print("="*60)
        print(f"stdio 클라이언트: {'✅ 성공' if results['stdio'] else '❌ 실패'}")
        print(f"SSE 클라이언트: {'✅ 성공' if results['sse'] else '❌ 실패'}")
        
        total_tests = len(results)
        passed_tests = sum(1 for success in results.values() if success)
        
        print(f"\n전체 결과: {passed_tests}/{total_tests} 테스트 통과")
        
        if passed_tests == total_tests:
            print("🎉 모든 테스트가 성공적으로 완료되었습니다!")
        else:
            print("⚠️ 일부 테스트가 실패했습니다. 로그를 확인해주세요.")
        
        return results


def signal_handler(signum, frame):
    """시그널 핸들러 (Ctrl+C 처리)"""
    print("\n⚠️ 테스트가 중단되었습니다.")
    sys.exit(0)


async def main():
    """메인 함수"""
    # 시그널 핸들러 등록
    signal.signal(signal.SIGINT, signal_handler)
    
    tester = MCPTester()
    await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
