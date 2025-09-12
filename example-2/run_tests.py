# run_tests.py
"""
FastMCP MCP 서버 테스트 실행 도구
Medium 글의 예제를 기반으로 구현
"""

import asyncio
import sys
import os
from test_mcp import MCPTester


def print_usage():
    """사용법 출력"""
    print("""
🧪 FastMCP MCP 서버 테스트 도구

Medium 글 기반 구현: https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb

사용법:
  python run_tests.py [옵션]

옵션:
  --stdio-only    STDIO 클라이언트만 테스트
  --sse-only      SSE 클라이언트만 테스트
  --help          이 도움말 표시

예시:
  python run_tests.py              # 모든 테스트 실행
  python run_tests.py --stdio-only # STDIO만 테스트
  python run_tests.py --sse-only   # SSE만 테스트

개별 실행:
  python stdio_server.py           # STDIO 서버 실행
  python sse_server.py             # SSE 서버 실행
  python stdio_client.py           # STDIO 클라이언트 테스트
  python sse_client.py             # SSE 클라이언트 테스트
""")


async def main():
    """메인 함수"""
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        return
    
    tester = MCPTester()
    
    if "--stdio-only" in args:
        print("📱 STDIO 클라이언트만 테스트합니다.")
        await tester.test_stdio_client()
    elif "--sse-only" in args:
        print("🌐 SSE 클라이언트만 테스트합니다.")
        if tester.start_sse_server():
            try:
                await tester.test_sse_client()
            finally:
                tester.stop_sse_server()
        else:
            print("❌ SSE 서버 시작 실패")
    else:
        print("🧪 모든 FastMCP 테스트를 실행합니다.")
        await tester.run_all_tests()


if __name__ == "__main__":
    asyncio.run(main())
