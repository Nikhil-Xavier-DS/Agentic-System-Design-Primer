from __future__ import annotations

from collections.abc import Iterable

from .anthropic_provider import AnthropicProvider
from .base_provider import ChatRequest, ChatResponse, LLMProvider
from .config import LLMConfig
from .ollama_provider import OllamaProvider
from .openai_provider import OpenAICompatibleProvider, OpenAIProvider


class MockProvider(LLMProvider):
    name = "mock"

    async def chat(self, request: ChatRequest) -> ChatResponse:
        last = request.messages[-1].content if request.messages else ""
        return ChatResponse(
            content=f"[mock] Planned response for: {last}",
            model=request.model or "mock-model",
            provider=self.name,
            usage={"prompt_tokens": len(last.split()), "completion_tokens": 6},
        )

    async def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
        return [[float((hash(text) + i) % 997) / 997 for i in range(16)] for text in texts]


class ModelRouter:
    def __init__(self, providers: dict[str, LLMProvider], default_provider: str, fallbacks: Iterable[str] = ()):
        self.providers = providers
        self.default_provider = default_provider
        self.fallbacks = tuple(fallbacks)

    async def chat(self, request: ChatRequest, provider: str | None = None) -> ChatResponse:
        provider_chain = (provider or self.default_provider, *self.fallbacks, "mock")
        errors: list[str] = []
        for provider_name in provider_chain:
            selected = self.providers.get(provider_name)
            if selected is None:
                continue
            try:
                return await selected.chat(request)
            except Exception as exc:  # noqa: BLE001 - router must preserve fallback behavior
                errors.append(f"{provider_name}: {exc}")
        raise RuntimeError("All providers failed: " + " | ".join(errors))


def build_default_router(config: LLMConfig | None = None) -> ModelRouter:
    cfg = config or LLMConfig.from_env()
    providers: dict[str, LLMProvider] = {
        "mock": MockProvider(),
        "ollama": OllamaProvider(cfg),
        "openai": OpenAIProvider(cfg),
        "anthropic": AnthropicProvider(cfg),
        "openai-compatible": OpenAICompatibleProvider(cfg),
    }
    return ModelRouter(providers, cfg.model_provider, cfg.fallback_providers)
