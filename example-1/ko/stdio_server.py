# stdio_server.py
import asyncio
import sys
import json
import math
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp import types


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


async def main():
    """메인 함수"""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
