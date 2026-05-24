from __future__ import annotations

import argparse
import asyncio
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from shared.llm import ChatMessage, ChatRequest, build_default_router


async def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default=None)
    parser.add_argument("--model", default=None)
    args = parser.parse_args()
    router = build_default_router()
    start = time.perf_counter()
    response = await router.chat(
        ChatRequest(
            messages=[ChatMessage(role="user", content="Return a concise benchmark response.")],
            model=args.model,
        ),
        provider=args.provider,
    )
    print({
        "provider": response.provider,
        "model": response.model,
        "latency_seconds": round(time.perf_counter() - start, 4),
        "usage": response.usage,
    })


if __name__ == "__main__":
    asyncio.run(main())
