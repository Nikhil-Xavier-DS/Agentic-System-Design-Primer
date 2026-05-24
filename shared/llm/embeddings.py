from __future__ import annotations

from .model_router import build_default_router


async def embed_texts(texts: list[str], provider: str | None = None, model: str | None = None) -> list[list[float]]:
    router = build_default_router()
    selected = router.providers[provider or router.default_provider]
    return await selected.embed(texts, model=model)
