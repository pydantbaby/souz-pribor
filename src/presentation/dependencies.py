from typing import Annotated, Protocol

from fastapi import Depends, Request


class AIClient(Protocol):
    async def request(self, message: str) -> str: ...


def get_ai_client(request: Request) -> AIClient:
    return request.app.state.ai_client  # type: ignore


AIClientDep = Annotated[AIClient, Depends(get_ai_client)]
