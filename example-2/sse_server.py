# sse_server.py
"""
FastMCP를 사용한 SSE 방식 MCP 서버
Medium 글의 예제를 기반으로 구현
"""

from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from mcp.server import Server
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import math
import json
from typing import Dict, Any, List

# MCP 서버 생성
mcp = FastMCP("SSE Example Server")

@mcp.tool()
def greet(name: str) -> str:
    """사용자 이름으로 인사"""
    return f"Hello, {name}! Welcome to the SSE server."

@mcp.tool()
def add(a: int, b: int) -> str:
    """두 숫자를 더하고 결과 반환"""
    return f"The sum of {a} and {b} is {a + b}."

@mcp.tool()
def multiply(a: float, b: float) -> str:
    """두 숫자를 곱하고 결과 반환"""
    result = a * b
    return f"The product of {a} and {b} is {result}"

@mcp.tool()
def calculate(expression: str) -> str:
    """수학 표현식을 계산합니다 (안전한 계산)"""
    try:
        # 안전한 계산을 위해 제한된 함수만 허용
        allowed_names = {
            k: v for k, v in math.__dict__.items() if not k.startswith("__")
        }
        allowed_names.update({"abs": abs, "round": round, "min": min, "max": max})
        
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"Calculation result: {result}"
    except Exception as e:
        return f"Calculation error: {str(e)}"

@mcp.tool()
def get_system_info() -> str:
    """시스템 정보를 반환합니다"""
    import platform
    import sys
    
    info = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "architecture": platform.architecture()[0],
        "processor": platform.processor()
    }
    
    return f"System Information:\n{json.dumps(info, indent=2)}"

@mcp.tool()
def echo(message: str) -> str:
    """입력된 메시지를 그대로 반환합니다"""
    return f"Echo: {message}"

@mcp.tool()
def get_server_status() -> str:
    """서버 상태를 반환합니다"""
    import time
    import psutil
    
    status = {
        "server_name": "SSE Example Server",
        "uptime": time.time(),
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "status": "running"
    }
    
    return f"Server Status:\n{json.dumps(status, indent=2)}"

@mcp.resource("config://settings")
def get_config() -> str:
    """설정 파일 리소스를 반환합니다"""
    config = {
        "server_name": "SSE Example Server",
        "version": "1.0.0",
        "features": ["tools", "resources", "prompts", "sse"],
        "max_connections": 1000,
        "debug_mode": True,
        "sse_endpoint": "/sse"
    }
    return json.dumps(config, indent=2)

@mcp.resource("file://readme")
def get_readme() -> str:
    """README 리소스를 반환합니다"""
    return """
# SSE MCP Server

이 서버는 FastMCP를 사용하여 구현된 SSE 방식의 MCP 서버입니다.

## 사용 가능한 도구
- greet: 사용자 인사
- add: 두 숫자 덧셈
- multiply: 두 숫자 곱셈
- calculate: 수학 표현식 계산
- get_system_info: 시스템 정보 조회
- echo: 메시지 반환
- get_server_status: 서버 상태 조회

## 사용 가능한 리소스
- config://settings: 서버 설정
- file://readme: 이 README 파일

## 사용 가능한 프롬프트
- code_review: 코드 리뷰 프롬프트
- explain_code: 코드 설명 프롬프트

## SSE 엔드포인트
- /sse: Server-Sent Events 스트림
- /messages/: 메시지 처리 엔드포인트
"""

@mcp.prompt("code_review")
def code_review_prompt(code: str, language: str = "python") -> str:
    """코드 리뷰를 위한 프롬프트를 생성합니다"""
    return f"""
다음 {language} 코드를 리뷰해주세요:

```{language}
{code}
```

다음 항목들을 확인해주세요:
1. 코드 스타일과 가독성
2. 잠재적인 버그나 오류
3. 성능 최적화 가능성
4. 보안 취약점
5. 개선 제안사항

각 항목에 대해 구체적인 피드백을 제공해주세요.
"""

@mcp.prompt("explain_code")
def explain_code_prompt(code: str, language: str = "python") -> str:
    """코드 설명을 위한 프롬프트를 생성합니다"""
    return f"""
다음 {language} 코드가 무엇을 하는지 자세히 설명해주세요:

```{language}
{code}
```

다음 내용을 포함해주세요:
1. 코드의 전체적인 목적
2. 각 부분의 역할과 기능
3. 사용된 알고리즘이나 패턴
4. 입력과 출력
5. 예시 사용법
"""

def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    """SSE를 통해 MCP 서버를 제공하는 Starlette 애플리케이션 생성"""
    sse = SseServerTransport("/messages/")

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
                request.scope,
                request.receive,
                request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    # CORS 미들웨어 추가
    app = Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/messages/", app=sse.handle_post_message),
        ],
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    return app

if __name__ == "__main__":
    # MCP 서버 인스턴스 가져오기
    mcp_server = mcp._mcp_server

    # SSE 지원 Starlette 앱 생성
    starlette_app = create_starlette_app(mcp_server, debug=True)

    port = 8080
    print(f"Starting MCP server with SSE transport on port {port}...")
    print(f"SSE endpoint available at: http://localhost:{port}/sse")
    print("Available tools: greet, add, multiply, calculate, get_system_info, echo, get_server_status")
    print("Available resources: config://settings, file://readme")
    print("Available prompts: code_review, explain_code")

    # uvicorn을 사용하여 서버 실행
    uvicorn.run(starlette_app, host="0.0.0.0", port=port)
