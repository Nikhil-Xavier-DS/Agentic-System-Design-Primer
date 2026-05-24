from __future__ import annotations

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .base_provider import ChatRequest, ChatResponse, LLMProvider
from .config import LLMConfig


class OllamaProvider(LLMProvider):
    name = "ollama"

    def __init__(self, config: LLMConfig):
        self.config = config

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
    async def chat(self, request: ChatRequest) -> ChatResponse:
        model = request.model or self.config.ollama_model
        payload = {
            "model": model,
            "messages": [
                {"role": message.role, "content": message.content}
                for message in request.messages
            ],
            "stream": False,
            "options": {"temperature": request.temperature},
        }
        async with httpx.AsyncClient(timeout=self.config.request_timeout_seconds) as client:
            response = await client.post(f"{self.config.ollama_base_url}/api/chat", json=payload)
            response.raise_for_status()
            data = response.json()
        return ChatResponse(
            content=data.get("message", {}).get("content", ""),
            model=model,
            provider=self.name,
            usage={
                "prompt_eval_count": data.get("prompt_eval_count"),
                "eval_count": data.get("eval_count"),
            },
            raw=data,
        )

    async def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
        selected_model = model or self.config.ollama_model
        vectors: list[list[float]] = []
        async with httpx.AsyncClient(timeout=self.config.request_timeout_seconds) as client:
            for text in texts:
                response = await client.post(
                    f"{self.config.ollama_base_url}/api/embeddings",
                    json={"model": selected_model, "prompt": text},
                )
                response.raise_for_status()
                vectors.append(response.json()["embedding"])
        return vectors
