from __future__ import annotations

from .base_provider import ChatRequest, ChatResponse, LLMProvider
from .config import LLMConfig


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, config: LLMConfig):
        self.config = config

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
        client = AsyncOpenAI(api_key=self.config.openai_api_key)
        model = request.model or self.config.openai_model
        response = await client.chat.completions.create(
            model=model,
            messages=[message.__dict__ for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return ChatResponse(
            content=response.choices[0].message.content or "",
            model=model,
            provider=self.name,
            usage=response.usage.model_dump() if response.usage else {},
            raw=response,
        )


class OpenAICompatibleProvider(OpenAIProvider):
    name = "openai-compatible"

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            from openai import AsyncOpenAI
        except ImportError as exc:
            raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
        client = AsyncOpenAI(
            api_key=self.config.openai_compatible_api_key,
            base_url=self.config.openai_compatible_base_url,
        )
        model = request.model or self.config.openai_compatible_model or self.config.openai_model
        response = await client.chat.completions.create(
            model=model,
            messages=[message.__dict__ for message in request.messages],
            temperature=request.temperature,
            max_tokens=request.max_tokens,
        )
        return ChatResponse(
            content=response.choices[0].message.content or "",
            model=model,
            provider=self.name,
            usage=response.usage.model_dump() if response.usage else {},
            raw=response,
        )
