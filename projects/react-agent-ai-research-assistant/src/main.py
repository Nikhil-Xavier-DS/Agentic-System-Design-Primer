from __future__ import annotations

import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.llm import ChatMessage, ChatRequest, build_default_router


SYSTEM_PROMPT = """You are running the AI Research Assistant reference implementation.
Use the ReAct Agent architecture. Be explicit about plan, state, tools, risks, and next action.
Keep the response concise but implementation-minded."""


async def run(task: str) -> str:
    router = build_default_router()
    response = await router.chat(
        ChatRequest(
            messages=[
                ChatMessage(role="system", content=SYSTEM_PROMPT),
                ChatMessage(role="user", content=task),
            ],
            temperature=0.2,
        )
    )
    return response.content


def main() -> None:
    task = " ".join(sys.argv[1:]) or "Run a smoke test and explain the architecture."
    print(asyncio.run(run(task)))


if __name__ == "__main__":
    main()
