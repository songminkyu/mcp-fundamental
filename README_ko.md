# MCP Fundamental Examples

이 프로젝트는 MCP(Model Context Protocol)의 기본 개념과 구현 방법을 학습하기 위한 예제 모음입니다. 두 가지 다른 접근 방식을 통해 MCP 서버와 클라이언트를 구현하는 방법을 보여줍니다.

## 📚 프로젝트 구조

```
mcp-fundamental/
├── example-1/              # 기본 MCP 라이브러리 사용
│   ├── stdio_server.py     # stdio 방식 서버
│   ├── sse_server.py       # SSE 방식 서버
│   ├── stdio_client.py     # stdio 클라이언트
│   ├── sse_client.py       # SSE 클라이언트
│   ├── test_mcp.py         # 통합 테스트
│   ├── run_tests.py        # 테스트 실행 도구
│   ├── requirements.txt    # 의존성
│   ├── Dockerfile          # Docker 설정
│   ├── docker-compose.yml  # Docker Compose 설정
│   └── README.md           # 상세 문서
├── example-2/              # FastMCP 라이브러리 사용
│   ├── stdio_server.py     # FastMCP stdio 서버
│   ├── sse_server.py       # FastMCP SSE 서버
│   ├── stdio_client.py     # stdio 클라이언트
│   ├── sse_client.py       # SSE 클라이언트
│   ├── test_mcp.py         # 통합 테스트
│   ├── run_tests.py        # 테스트 실행 도구
│   ├── requirements.txt    # 의존성
│   └── README.md           # 상세 문서
├── .gitignore              # Git 무시 파일
└── README.md               # 이 파일
```

## 🎯 학습 목표

이 프로젝트를 통해 다음을 학습할 수 있습니다:

1. **MCP 기본 개념**: Model Context Protocol의 핵심 개념 이해
2. **두 가지 구현 방식**: 기본 MCP vs FastMCP 비교
3. **통신 방식**: STDIO vs SSE 방식의 차이점과 사용 사례
4. **실제 구현**: 완전히 작동하는 서버와 클라이언트 구현
5. **테스트 방법**: 자동화된 테스트를 통한 검증

## 🚀 빠른 시작

### 1. 저장소 클론

```bash
git clone <repository-url>
cd mcp-fundamental
```

### 2. 예제 선택

#### Example 1: 기본 MCP 라이브러리
```bash
cd example-1
pip install -r requirements.txt
python run_tests.py
```

#### Example 2: FastMCP 라이브러리
```bash
cd example-2
pip install -r requirements.txt
python run_tests.py
```

## 📖 예제별 특징

### Example 1: 기본 MCP 라이브러리

- **라이브러리**: 표준 MCP 라이브러리
- **복잡도**: 중간 (더 많은 설정 필요)
- **학습 가치**: MCP의 내부 동작 원리 이해
- **적합한 경우**: MCP의 세부 사항을 깊이 이해하고 싶은 경우

**주요 특징:**
- 수동으로 서버 설정
- 명시적인 도구/리소스/프롬프트 정의
- 세밀한 제어 가능
- 교육적 가치 높음

### Example 2: FastMCP 라이브러리

- **라이브러리**: FastMCP (현대적 MCP 라이브러리)
- **복잡도**: 낮음 (간단한 데코레이터 사용)
- **학습 가치**: 빠른 프로토타이핑과 현대적 개발 방법
- **적합한 경우**: 빠르게 MCP 서버를 구축하고 싶은 경우

**주요 특징:**
- 데코레이터 기반 간단한 문법
- 자동 타입 추론
- 최소한의 코드로 구현
- 프로덕션 환경에 적합

## 🔄 STDIO vs SSE 비교

| 구분 | STDIO 방식 | SSE 방식 |
|------|------------|----------|
| **통신 방식** | 표준 입출력 | HTTP + Server-Sent Events |
| **사용 환경** | 로컬 프로세스 | 웹 서비스 |
| **구현 복잡도** | 간단 | 복잡 |
| **네트워크 지원** | 없음 | 있음 |
| **실시간 스트리밍** | 제한적 | 지원 |
| **확장성** | 제한적 | 높음 |
| **배포** | 로컬 실행 | 웹 서버 배포 |
| **사용 사례** | 로컬 도구, CLI | 웹 서비스, 원격 접근 |

## 🛠️ 제공되는 기능

### 도구 (Tools)
- **greet**: 사용자 인사
- **add**: 두 숫자 덧셈
- **multiply**: 두 숫자 곱셈
- **calculate**: 수학 표현식 계산
- **get_system_info**: 시스템 정보 조회
- **echo**: 메시지 반환
- **get_server_status**: 서버 상태 조회 (SSE 전용)

### 리소스 (Resources)
- **config://settings**: 서버 설정 파일
- **file://readme**: README 리소스

### 프롬프트 (Prompts)
- **code_review**: 코드 리뷰 프롬프트
- **explain_code**: 코드 설명 프롬프트

## 🧪 테스트 실행

### 개별 예제 테스트

```bash
# Example 1 테스트
cd example-1
python run_tests.py              # 모든 테스트
python run_tests.py --stdio-only # STDIO만
python run_tests.py --sse-only   # SSE만

# Example 2 테스트
cd example-2
python run_tests.py              # 모든 테스트
python run_tests.py --stdio-only # STDIO만
python run_tests.py --sse-only   # SSE만
```

### 개별 서버/클라이언트 실행

```bash
# 서버 실행
python stdio_server.py    # STDIO 서버
python sse_server.py      # SSE 서버

# 클라이언트 실행
python stdio_client.py    # STDIO 클라이언트
python sse_client.py      # SSE 클라이언트
```

## 🐳 Docker 사용

### Example 1 Docker 실행

```bash
cd example-1
docker-compose up mcp-sse-server    # SSE 서버만
docker-compose up mcp-stdio-server  # STDIO 서버만
docker-compose up                   # 모든 서비스
```

## 📚 학습 순서 권장

1. **기본 개념 이해**: MCP가 무엇인지, 왜 필요한지 이해
2. **Example 1 실행**: 기본 MCP 라이브러리로 구현된 예제 실행
3. **코드 분석**: Example 1의 서버/클라이언트 코드 분석
4. **Example 2 실행**: FastMCP로 구현된 예제 실행
5. **비교 분석**: 두 예제의 차이점과 장단점 비교
6. **자신만의 도구 추가**: 기존 예제에 새로운 도구 추가해보기

## 🔧 문제 해결

### 일반적인 문제

1. **의존성 설치 실패**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

2. **포트 충돌 (SSE 서버)**
   - 8080 포트가 사용 중인 경우 다른 포트 사용
   - `sse_server.py`에서 포트 번호 변경

3. **STDIO 클라이언트 연결 실패**
   - Python 경로 확인
   - 서버 스크립트 경로 확인

4. **SSE 클라이언트 연결 실패**
   - SSE 서버가 실행 중인지 확인
   - 방화벽 설정 확인

### 디버깅

```bash
# 상세한 로그와 함께 실행
python -u stdio_client.py
python -u sse_client.py
python -u test_mcp.py
```

## 📖 추가 자료

- [MCP 공식 문서](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/pydantic/fastmcp)
- [Medium: MCP Clients: Stdio vs SSE](https://medium.com/@vkrishnan9074/mcp-clients-stdio-vs-sse-a53843d9aabb)

## 🤝 기여

버그 리포트, 기능 제안, 또는 개선 사항이 있으시면 이슈로 등록해주세요.

## 📄 라이선스

이 프로젝트는 교육 목적으로 작성되었습니다.

---

**Happy Learning! 🎉**

MCP의 세계에 오신 것을 환영합니다. 이 예제들을 통해 MCP의 강력함과 유연성을 경험해보세요!