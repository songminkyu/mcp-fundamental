# sse_server.py
import asyncio
import json
import math
from typing import Dict, Any
from mcp.server import Server
from mcp import types
from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route
from starlette.middleware.cors import CORSMiddleware
import uvicorn


# 서버 인스턴스 생성
server = Server("my-mcp-server")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    """사용 가능한 도구 목록을 반환합니다."""
    return [
        types.Tool(
            name="calculator",
            description="간단한 수학 계산을 수행합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "계산할 수학 표현식 (예: 2+2)"
                    }
                },
                "required": ["expression"]
            }
        ),
        types.Tool(
            name="echo",
            description="입력된 메시지를 그대로 반환합니다",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "반환할 메시지"
                    }
                },
                "required": ["message"]
            }
        )
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """도구 호출을 처리합니다."""
    if name == "calculator":
        expression = arguments.get("expression", "")
        try:
            # 안전한 계산을 위해 제한된 함수만 허용
            allowed_names = {
                k: v for k, v in math.__dict__.items() if not k.startswith("__")
            }
            allowed_names.update({"abs": abs, "round": round})
            
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            return [types.TextContent(type="text", text=f"계산 결과: {result}")]
        except Exception as e:
            return [types.TextContent(type="text", text=f"계산 오류: {str(e)}")]
    
    elif name == "echo":
        message = arguments.get("message", "")
        return [types.TextContent(type="text", text=f"에코: {message}")]
    
    else:
        raise ValueError(f"알 수 없는 도구: {name}")


@server.list_resources()
async def list_resources() -> list[types.Resource]:
    """사용 가능한 리소스 목록을 반환합니다."""
    return [
        types.Resource(
            uri="file://config.json",
            name="설정 파일",
            description="애플리케이션 설정 파일",
            mimeType="application/json"
        )
    ]


@server.read_resource()
async def read_resource(uri: str) -> str:
    """리소스를 읽어 반환합니다."""
    if uri == "file://config.json":
        return json.dumps({
            "version": "1.0",
            "debug": True,
            "max_connections": 100
        }, indent=2)
    else:
        raise ValueError(f"알 수 없는 리소스: {uri}")


@server.list_prompts()
async def list_prompts() -> list[types.Prompt]:
    """사용 가능한 프롬프트 목록을 반환합니다."""
    return [
        types.Prompt(
            name="code_review",
            description="코드 리뷰를 위한 프롬프트",
            arguments=[
                types.PromptArgument(
                    name="code",
                    description="리뷰할 코드",
                    required=True
                )
            ]
        )
    ]


@server.get_prompt()
async def get_prompt(name: str, arguments: dict) -> types.GetPromptResult:
    """프롬프트를 반환합니다."""
    if name == "code_review":
        code = arguments["code"]
        return types.GetPromptResult(
            description="코드 리뷰 프롬프트",
            messages=[
                types.PromptMessage(
                    role="user",
                    content=types.TextContent(
                        type="text",
                        text=f"다음 코드를 리뷰해주세요:\n\n```\n{code}\n```"
                    )
                )
            ]
        )
    else:
        raise ValueError(f"알 수 없는 프롬프트: {name}")


# SSE 엔드포인트
async def sse_endpoint(request):
    """Server-Sent Events 엔드포인트"""
    
    async def event_generator():
        # 초기 연결 메시지
        yield f"data: {json.dumps({'type': 'connected', 'message': 'MCP Server connected'})}\n\n"
        
        # 클라이언트로부터 메시지를 받기 위한 큐
        message_queue = asyncio.Queue()
        
        # 메시지 처리 태스크
        async def process_messages():
            while True:
                try:
                    # 실제 구현에서는 WebSocket이나 다른 방식으로 클라이언트 메시지를 받아야 함
                    # 여기서는 데모를 위해 간단한 구조만 제공
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f"메시지 처리 오류: {e}")
                    break
        
        # 메시지 처리 시작
        task = asyncio.create_task(process_messages())
        
        try:
            while True:
                # 주기적으로 상태 업데이트 (실제로는 클라이언트 메시지에 응답)
                yield f"data: {json.dumps({'type': 'heartbeat', 'timestamp': asyncio.get_event_loop().time()})}\n\n"
                await asyncio.sleep(5)
        except Exception as e:
            print(f"SSE 스트림 오류: {e}")
        finally:
            task.cancel()
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Cache-Control"
        }
    )


# API 엔드포인트들
async def list_tools_endpoint(request):
    """도구 목록 반환"""
    tools = await server.list_tools()
    return JSONResponse(tools)


async def call_tool_endpoint(request):
    """도구 호출"""
    body = await request.json()
    name = body.get("name")
    arguments = body.get("arguments", {})
    
    try:
        result = await server.call_tool(name, arguments)
        return JSONResponse({"result": result})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


async def list_resources_endpoint(request):
    """리소스 목록 반환"""
    resources = await server.list_resources()
    return JSONResponse(resources)


async def read_resource_endpoint(request):
    """리소스 읽기"""
    uri = request.query_params.get("uri")
    if not uri:
        return JSONResponse({"error": "URI is required"}, status_code=400)
    
    try:
        content = await server.read_resource(uri)
        return JSONResponse({"content": content})
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


async def list_prompts_endpoint(request):
    """프롬프트 목록 반환"""
    prompts = await server.list_prompts()
    return JSONResponse(prompts)


async def get_prompt_endpoint(request):
    """프롬프트 가져오기"""
    body = await request.json()
    name = body.get("name")
    arguments = body.get("arguments", {})
    
    try:
        result = await server.get_prompt(name, arguments)
        return JSONResponse(result)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=400)


# Starlette 애플리케이션 생성
app = Starlette(
    routes=[
        Route("/sse", sse_endpoint),
        Route("/tools", list_tools_endpoint, methods=["GET"]),
        Route("/tools/call", call_tool_endpoint, methods=["POST"]),
        Route("/resources", list_resources_endpoint, methods=["GET"]),
        Route("/resources/read", read_resource_endpoint, methods=["GET"]),
        Route("/prompts", list_prompts_endpoint, methods=["GET"]),
        Route("/prompts/get", get_prompt_endpoint, methods=["POST"]),
    ]
)

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    print("MCP Server (SSE) 시작 중...")
    print("SSE 엔드포인트: http://localhost:8000/sse")
    print("API 엔드포인트: http://localhost:8000/tools")
    uvicorn.run(app, host="0.0.0.0", port=8000)
