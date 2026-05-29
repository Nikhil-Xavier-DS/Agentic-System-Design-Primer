from __future__ import annotations

import argparse
import asyncio
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = Path(__file__).resolve().parents[1]
for path in (ROOT, PROJECT_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from shared.llm import build_default_router
from src.agent import ResearchAssistantAgent, memory_path_from_env, web_search_mode_from_env
from src.memory import SQLiteResearchMemory


async def run(
    task: str,
    web_search_mode: str | None = None,
    max_steps: int = 3,
    memory_db: Path | None = None,
) -> str:
    router = build_default_router()
    agent = ResearchAssistantAgent(
        router=router,
        web_search_mode=web_search_mode or web_search_mode_from_env(),
        max_steps=max_steps,
        memory=SQLiteResearchMemory(memory_db or memory_path_from_env()),
    )
    return await agent.run(task)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the ReAct AI Research Assistant.")
    parser.add_argument("task", nargs="*", help="Research task to run.")
    parser.add_argument(
        "--no-web",
        action="store_true",
        help="Disable web search and use only local tools.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=3,
        help="Maximum ReAct tool steps before synthesis.",
    )
    parser.add_argument(
        "--memory-db",
        type=Path,
        default=None,
        help="Path to the SQLite research memory database.",
    )
    parser.add_argument(
        "--show-memory",
        action="store_true",
        help="Show recent research runs and exit.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    memory = SQLiteResearchMemory(args.memory_db or memory_path_from_env())
    if args.show_memory:
        for research_run in memory.recent_runs():
            print(research_run)
        return
    task = " ".join(args.task) or "Run a smoke test and explain the architecture."
    web_search_mode = "off" if args.no_web else None
    print(
        asyncio.run(
            run(
                task,
                web_search_mode=web_search_mode,
                max_steps=args.max_steps,
                memory_db=args.memory_db,
            )
        )
    )


if __name__ == "__main__":
    main()
