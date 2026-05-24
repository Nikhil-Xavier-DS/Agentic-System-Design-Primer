from __future__ import annotations

from .base_provider import ChatRequest, ChatResponse, LLMProvider
from .config import LLMConfig


class AnthropicProvider(LLMProvider):
    name = "anthropic"

    def __init__(self, config: LLMConfig):
        self.config = config

    async def chat(self, request: ChatRequest) -> ChatResponse:
        try:
            from anthropic import AsyncAnthropic
        except ImportError as exc:
            raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
        client = AsyncAnthropic(api_key=self.config.anthropic_api_key)
        system = "\n".join(m.content for m in request.messages if m.role == "system")
        messages = [
            {"role": m.role, "content": m.content}
            for m in request.messages
            if m.role != "system"
        ]
        model = request.model or self.config.anthropic_model
        response = await client.messages.create(
            model=model,
            max_tokens=request.max_tokens or 1024,
            temperature=request.temperature,
            system=system or None,
            messages=messages,
        )
        text = "".join(block.text for block in response.content if block.type == "text")
        return ChatResponse(content=text, model=model, provider=self.name, raw=response)
