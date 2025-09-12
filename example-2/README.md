# FastMCP MCP 서버 예제

이 프로젝트는 [Medium 글](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)의 예제를 기반으로 FastMCP를 사용하여 STDIO와 SSE 두 가지 방식의 MCP 서버와 클라이언트를 구현한 예제입니다.

## 📚 참고 자료

- **원본 Medium 글**: [MCP Clients: Stdio vs SSE](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)
- **FastMCP**: 현대적이고 간단한 MCP 서버 구현을 위한 라이브러리

## 🏗️ 프로젝트 구조

```
example-2/
├── requirements.txt          # Python 의존성
├── stdio_server.py          # FastMCP STDIO 서버
├── sse_server.py            # FastMCP SSE 서버
├── stdio_client.py          # STDIO 클라이언트
├── sse_client.py            # SSE 클라이언트
├── test_mcp.py              # 통합 테스트
├── run_tests.py             # 테스트 실행 도구
└── README.md                # 이 파일
```

## 🚀 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. 개별 서버 실행

#### STDIO 서버
```bash
python stdio_server.py
```

#### SSE 서버
```bash
python sse_server.py
```

### 3. 개별 클라이언트 테스트

#### STDIO 클라이언트
```bash
python stdio_client.py
```

#### SSE 클라이언트 (SSE 서버가 실행 중이어야 함)
```bash
python sse_client.py
```

### 4. 통합 테스트

```bash
# 모든 테스트 실행
python test_mcp.py

# 또는 간편한 실행 스크립트 사용
python run_tests.py              # 모든 테스트
python run_tests.py --stdio-only # STDIO만 테스트
python run_tests.py --sse-only   # SSE만 테스트
```

## 🛠️ 제공되는 기능

### 도구 (Tools)

1. **greet**: 사용자 이름으로 인사
   - 입력: `{"name": "Alice"}`
   - 출력: `"Hello, Alice! Welcome to the STDIO/SSE server."`

2. **add**: 두 숫자 덧셈
   - 입력: `{"a": 5, "b": 7}`
   - 출력: `"The sum of 5 and 7 is 12"`

3. **multiply**: 두 숫자 곱셈
   - 입력: `{"a": 3.5, "b": 2.0}`
   - 출력: `"The product of 3.5 and 2.0 is 7.0"`

4. **calculate**: 수학 표현식 계산
   - 입력: `{"expression": "sqrt(16) + 2 * 3"}`
   - 출력: `"Calculation result: 10.0"`

5. **get_system_info**: 시스템 정보 조회
   - 입력: `{}`
   - 출력: 시스템 정보 JSON

6. **echo**: 메시지 반환
   - 입력: `{"message": "Hello World"}`
   - 출력: `"Echo: Hello World"`

7. **get_server_status**: 서버 상태 조회 (SSE 전용)
   - 입력: `{}`
   - 출력: 서버 상태 정보 JSON

### 리소스 (Resources)

1. **config://settings**: 서버 설정 파일
2. **file://readme**: README 리소스

### 프롬프트 (Prompts)

1. **code_review**: 코드 리뷰 프롬프트
   - 입력: `{"code": "def hello(): print('Hello')", "language": "python"}`
   - 출력: 코드 리뷰를 위한 구조화된 프롬프트

2. **explain_code**: 코드 설명 프롬프트
   - 입력: `{"code": "def fibonacci(n): ...", "language": "python"}`
   - 출력: 코드 설명을 위한 구조화된 프롬프트

## 🔄 STDIO vs SSE 비교

| 구분 | STDIO 방식 | SSE 방식 |
|------|------------|----------|
| **통신 방식** | 표준 입출력 | HTTP + Server-Sent Events |
| **사용 환경** | 로컬 프로세스 | 웹 서비스 |
| **구현 복잡도** | 간단 | 복잡 |
| **네트워크 지원** | 없음 | 있음 |
| **실시간 스트리밍** | 제한적 | 지원 |
| **확장성** | 제한적 | 높음 |
| **인증** | 없음 | 가능 |
| **배포** | 로컬 실행 | 웹 서버 배포 |

## 🎯 FastMCP의 장점

1. **간단한 데코레이터 문법**: `@mcp.tool()`, `@mcp.resource()`, `@mcp.prompt()`
2. **자동 타입 추론**: 함수 시그니처에서 자동으로 스키마 생성
3. **현대적인 Python 문법**: async/await, 타입 힌트 지원
4. **빠른 개발**: 최소한의 코드로 MCP 서버 구현
5. **유연한 전송 방식**: STDIO와 SSE 모두 지원

## 📝 사용 예제

### STDIO 서버와 클라이언트

```python
# 서버 (stdio_server.py)
from fastmcp import FastMCP

mcp = FastMCP("STDIO Example Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()  # 자동으로 STDIO 사용

# 클라이언트 (stdio_client.py)
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["stdio_server.py"]
    )
    
    async with stdio_client(server_params) as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool("greet", {"name": "Alice"})
            print(result.content)
```

### SSE 서버와 클라이언트

```python
# 서버 (sse_server.py)
from fastmcp import FastMCP
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
import uvicorn

mcp = FastMCP("SSE Example Server")

@mcp.tool()
def greet(name: str) -> str:
    return f"Hello, {name}!"

def create_starlette_app(mcp_server):
    sse = SseServerTransport("/messages/")
    # ... SSE 설정
    return Starlette(routes=[...])

if __name__ == "__main__":
    app = create_starlette_app(mcp._mcp_server)
    uvicorn.run(app, host="0.0.0.0", port=8080)

# 클라이언트 (sse_client.py)
from mcp import ClientSession
from mcp.client.sse import sse_client

async def main():
    async with sse_client(url="http://localhost:8080/sse") as streams:
        async with ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool("greet", {"name": "Bob"})
            print(result.content)
```

## 🔧 문제 해결

### 일반적인 문제

1. **SSE 서버 연결 실패**: SSE 서버가 실행 중인지 확인
2. **포트 충돌**: 8080 포트가 사용 중인 경우 다른 포트 사용
3. **의존성 오류**: `pip install -r requirements.txt` 재실행

### 디버깅

```bash
# 상세한 로그와 함께 실행
python -u stdio_client.py
python -u sse_client.py
```

## 📄 라이선스

이 프로젝트는 교육 목적으로 작성되었으며, 원본 Medium 글의 예제를 기반으로 합니다.

## 🤝 기여

버그 리포트나 기능 제안은 이슈로 등록해주세요.

---

**참고**: 이 예제는 [Medium 글](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)의 내용을 Python 코드로 구현한 것입니다.
