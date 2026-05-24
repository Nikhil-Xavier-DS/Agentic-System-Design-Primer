from __future__ import annotations

import asyncio
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.main import run


async def main() -> None:
    start = time.perf_counter()
    await run("Benchmark the reference workflow.")
    elapsed = time.perf_counter() - start
    print({"latency_seconds": round(elapsed, 4)})


if __name__ == "__main__":
    asyncio.run(main())
