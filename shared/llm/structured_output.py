from __future__ import annotations

import json
from typing import TypeVar

from pydantic import BaseModel, ValidationError

from .base_provider import ChatMessage, ChatRequest
from .model_router import build_default_router


T = TypeVar("T", bound=BaseModel)


async def generate_structured(prompt: str, schema: type[T]) -> T:
    router = build_default_router()
    response = await router.chat(
        ChatRequest(
            messages=[
                ChatMessage(role="system", content="Return only valid JSON matching the requested schema."),
                ChatMessage(role="user", content=f"{prompt}\nSchema: {schema.model_json_schema()}"),
            ],
            temperature=0,
        )
    )
    try:
        return schema.model_validate_json(response.content)
    except ValidationError:
        return schema.model_validate(json.loads(response.content))
