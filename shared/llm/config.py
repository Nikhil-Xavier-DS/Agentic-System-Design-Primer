from __future__ import annotations

import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - dotenv is optional at runtime
    load_dotenv = None


@dataclass(frozen=True)
class LLMConfig:
    model_provider: str = "mock"
    fallback_providers: tuple[str, ...] = ()
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"
    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-3-5-haiku-latest"
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    openai_compatible_base_url: str | None = None
    openai_compatible_api_key: str | None = None
    openai_compatible_model: str | None = None
    local_gguf_model_path: str | None = None
    request_timeout_seconds: float = 60.0

    @classmethod
    def from_env(cls) -> "LLMConfig":
        if load_dotenv is not None:
            load_dotenv()
        fallbacks = tuple(
            item.strip()
            for item in os.getenv("MODEL_FALLBACK_PROVIDERS", "").split(",")
            if item.strip()
        )
        return cls(
            model_provider=os.getenv("MODEL_PROVIDER", "mock"),
            fallback_providers=fallbacks,
            openai_api_key=os.getenv("OPENAI_API_KEY") or None,
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
            anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"),
            ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
            ollama_model=os.getenv("OLLAMA_MODEL", "llama3"),
            openai_compatible_base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL") or None,
            openai_compatible_api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY") or None,
            openai_compatible_model=os.getenv("OPENAI_COMPATIBLE_MODEL") or None,
            local_gguf_model_path=os.getenv("LOCAL_GGUF_MODEL_PATH") or None,
            request_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
        )
