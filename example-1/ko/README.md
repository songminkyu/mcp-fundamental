# MCP Server 구축 프로젝트

이 프로젝트는 [MCP(Model Context Protocol)](https://blog.choonzang.com/it/ai/3318/)을 사용하여 stdio와 SSE 두 가지 방식으로 MCP 서버를 구축하는 예제입니다.

## 프로젝트 구조

```
mcp-fundamental/
├── requirements.txt          # Python 의존성
├── stdio_server.py          # stdio 방식 MCP 서버
├── sse_server.py            # SSE 방식 MCP 서버
├── Dockerfile               # Docker 이미지 설정
├── docker-compose.yml       # Docker Compose 설정
└── README.md               # 프로젝트 설명서
```

## 설치 및 실행

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

### 2. stdio 방식 서버 실행

```bash
python stdio_server.py
```

stdio 방식은 표준 입출력을 통해 통신하며, 로컬 시스템 내에서 MCP 클라이언트와 연동할 때 사용됩니다.

### 3. SSE 방식 서버 실행

```bash
python sse_server.py
```

SSE 방식은 웹 기반 서비스로 실행되며, 다음 엔드포인트를 제공합니다:

- **SSE 스트림**: `http://localhost:8000/sse`
- **도구 목록**: `http://localhost:8000/tools`
- **도구 호출**: `http://localhost:8000/tools/call`
- **리소스 목록**: `http://localhost:8000/resources`
- **리소스 읽기**: `http://localhost:8000/resources/read`
- **프롬프트 목록**: `http://localhost:8000/prompts`
- **프롬프트 가져오기**: `http://localhost:8000/prompts/get`

### 4. Docker를 사용한 실행

```bash
# SSE 서버만 실행
docker-compose up mcp-sse-server

# stdio 서버만 실행
docker-compose up mcp-stdio-server

# 모든 서비스 실행
docker-compose up
```

## 제공되는 기능

### 도구 (Tools)

1. **calculator**: 수학 계산 수행
   - 입력: `{"expression": "2+2"}`
   - 출력: `"계산 결과: 4"`

2. **echo**: 메시지 반환
   - 입력: `{"message": "Hello World"}`
   - 출력: `"에코: Hello World"`

### 리소스 (Resources)

1. **config.json**: 애플리케이션 설정 파일
   - URI: `file://config.json`
   - MIME 타입: `application/json`

### 프롬프트 (Prompts)

1. **code_review**: 코드 리뷰 프롬프트
   - 입력: `{"code": "def hello(): print('Hello')"}`
   - 출력: 코드 리뷰를 위한 구조화된 프롬프트

## 클라이언트 테스트

### 1. Python 클라이언트 사용

```bash
# stdio 클라이언트 테스트
python stdio_client.py

# SSE 클라이언트 테스트 (SSE 서버가 실행 중이어야 함)
python sse_client.py

# 통합 테스트 (모든 클라이언트 테스트)
python test_mcp.py

# 또는 간편한 실행 스크립트 사용
python run_tests.py              # 모든 테스트
python run_tests.py --stdio-only # stdio만 테스트
python run_tests.py --sse-only   # SSE만 테스트
```

### 2. API 사용 예제 (curl)

```bash
# calculator 도구 사용
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "calculator", "arguments": {"expression": "2+2"}}'

# echo 도구 사용
curl -X POST http://localhost:8000/tools/call \
  -H "Content-Type: application/json" \
  -d '{"name": "echo", "arguments": {"message": "Hello MCP"}}'

# 리소스 읽기
curl "http://localhost:8000/resources/read?uri=file://config.json"

# 프롬프트 가져오기
curl -X POST http://localhost:8000/prompts/get \
  -H "Content-Type: application/json" \
  -d '{"name": "code_review", "arguments": {"code": "def hello(): print(\"Hello\")"}}'
```

## stdio vs SSE 비교

| 구분 | stdio 방식 | SSE 방식 |
|------|------------|----------|
| **통신 방식** | 표준 입출력 | HTTP 기반 |
| **사용 환경** | 로컬 시스템 | 웹 서비스 |
| **구현 복잡도** | 간단 | 복잡 |
| **네트워크 지원** | 없음 | 있음 |
| **실시간 스트리밍** | 제한적 | 지원 |
| **배포** | 로컬 실행 | 웹 서버 배포 |

## 보안 고려사항

- calculator 도구는 `eval()` 함수를 사용하므로 프로덕션 환경에서는 더 안전한 수학 파서를 사용하는 것을 권장합니다.
- SSE 서버는 CORS를 허용하도록 설정되어 있으므로, 프로덕션 환경에서는 적절한 CORS 정책을 설정하세요.

## 참고 자료

- [MCP Server 구축하기: stdio와 SSE 방식 차이점](https://blog.choonzang.com/it/ai/3318/)
- [MCP 공식 문서](https://modelcontextprotocol.io/)
