from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.infrastructure.ai import OpenAIClient as AIClient
from src.presentation import router
from src.presentation.exceptions import setup_exception_handlers
from src.settings import Settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    s = Settings()
    app.state.ai_client = AIClient(
        s.ai_base_url, s.ai_model, s.ai_api_key, s.ai_system_prompt, s.ai_timeout
    )
    yield
    await app.state.ai_client.client.close()


app = FastAPI(lifespan=lifespan)

app.include_router(router)
setup_exception_handlers(app)
