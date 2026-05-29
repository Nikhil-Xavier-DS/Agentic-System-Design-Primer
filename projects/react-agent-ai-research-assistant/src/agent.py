from __future__ import annotations

import os
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from shared.llm import ChatMessage, ChatRequest, ModelRouter

from .memory import SQLiteResearchMemory
from .tools import LocalKnowledgeTool, ResearchTool, ToolResult, WebSearchTool


ROOT = Path(__file__).resolve().parents[3]
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass
class AgentStep:
    thought: str
    action: str
    action_input: str
    observation: str
    sources: list[str] = field(default_factory=list)


@dataclass
class AgentState:
    task: str
    steps: list[AgentStep] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)


class ResearchAssistantAgent:
    """A small but real ReAct-style research assistant.

    The agent performs explicit thought/action/observation steps before asking
    the configured model to synthesize an answer from gathered evidence.
    """

    pattern = "ReAct Agent"

    def __init__(
        self,
        router: ModelRouter,
        enable_web: bool | None = None,
        max_steps: int = 3,
        web_search_mode: str | None = None,
        memory: SQLiteResearchMemory | None = None,
    ):
        self.router = router
        self.web_search_mode = web_search_mode or ("off" if enable_web is False else "auto")
        if enable_web is True:
            self.web_search_mode = "auto"
        self.max_steps = max_steps
        self.memory = memory or SQLiteResearchMemory(memory_path_from_env())
        self.tools = self._build_tools()

    async def run(self, task: str) -> str:
        state = self.initialize(task)
        run_id = self.memory.create_run(
            task,
            {
                "pattern": self.pattern,
                "web_search_mode": self.web_search_mode,
                "memory_backend": "sqlite",
            },
        )
        state.artifacts["run_id"] = run_id
        prior_memories = self.memory.search_memories(task)
        if prior_memories:
            state.artifacts["prior_memories"] = [
                {"kind": memory.kind, "key": memory.key, "value": memory.value}
                for memory in prior_memories
            ]
        for query in self._build_research_queries(task)[: self.max_steps]:
            tool = await self._select_tool(task, query)
            thought = f"I need evidence about: {query}"
            result = tool.run(query)
            self.record_observation(state, thought, result)
            self.memory.save_step(
                run_id=run_id,
                step_number=len(state.steps),
                thought=thought,
                action=result.tool,
                action_input=result.query,
                observation=result.content,
                sources=result.sources,
            )

        final_answer = await self._synthesize(state)
        self.memory.save_final_answer(run_id, final_answer)
        self._write_reusable_memories(state, final_answer)
        trace = self._format_trace(state)
        memory_summary = self._format_memory_summary(state)
        return f"{memory_summary}\n\n{trace}\n\nFinal Answer\n{final_answer}"

    def initialize(self, task: str) -> AgentState:
        return AgentState(task=task, artifacts={"web_search_mode": self.web_search_mode})

    def record_observation(self, state: AgentState, thought: str, result: ToolResult) -> AgentState:
        step = AgentStep(
            thought=thought,
            action=result.tool,
            action_input=result.query,
            observation=result.content,
            sources=result.sources,
        )
        state.steps.append(step)
        state.observations.append(result.content)
        return state

    def _build_tools(self) -> dict[str, ResearchTool]:
        tools: dict[str, ResearchTool] = {
            LocalKnowledgeTool.name: LocalKnowledgeTool(PROJECT_ROOT / "data/local_knowledge.jsonl")
        }
        if self.web_search_mode != "off":
            tools[WebSearchTool.name] = WebSearchTool()
        return tools

    async def _select_tool(self, task: str, query: str) -> ResearchTool:
        if WebSearchTool.name not in self.tools:
            return self.tools[LocalKnowledgeTool.name]
        if self.web_search_mode == "always":
            return self.tools[WebSearchTool.name]

        decision = await self._ask_model_for_tool(task, query)
        if decision in self.tools:
            return self.tools[decision]
        if _looks_current_or_external(query):
            return self.tools[WebSearchTool.name]
        return self.tools[LocalKnowledgeTool.name]

    async def _ask_model_for_tool(self, task: str, query: str) -> str | None:
        try:
            response = await self.router.chat(
                ChatRequest(
                    messages=[
                        ChatMessage(
                            role="system",
                            content=(
                                "You are a ReAct tool router. Choose exactly one tool for the query. "
                                "Use web_search for current, recent, external, source-discovery, "
                                "benchmark, paper, GitHub, product, or news questions. Use "
                                "local_knowledge_search for stable architecture concepts already likely "
                                "covered by the local corpus. Return only JSON like "
                                '{"tool":"web_search","reason":"needs current external sources"}'
                            ),
                        ),
                        ChatMessage(
                            role="user",
                            content=(
                                f"Task: {task}\n"
                                f"Research query: {query}\n"
                                f"Available tools: {', '.join(self.tools)}"
                            ),
                        ),
                    ],
                    temperature=0,
                    max_tokens=120,
                )
            )
        except Exception:  # noqa: BLE001 - tool routing can fall back to deterministic policy
            return None
        try:
            payload = json.loads(_extract_json_object(response.content))
        except json.JSONDecodeError:
            return None
        tool = payload.get("tool")
        return tool if isinstance(tool, str) else None

    def _build_research_queries(self, task: str) -> list[str]:
        base = task.strip()
        return [
            base,
            f"{base} architecture tradeoffs",
            f"{base} production observability security failure modes",
        ]

    async def _synthesize(self, state: AgentState) -> str:
        memory_context = "\n".join(
            f"- {item['kind']}:{item['key']} => {item['value']}"
            for item in state.artifacts.get("prior_memories", [])
        )
        evidence = "\n\n".join(
            (
                f"Thought: {step.thought}\n"
                f"Action: {step.action}({step.action_input})\n"
                f"Observation: {step.observation}\n"
                f"Sources: {', '.join(step.sources) or 'none'}"
            )
            for step in state.steps
        )
        response = await self.router.chat(
            ChatRequest(
                messages=[
                    ChatMessage(
                        role="system",
                        content=(
                            "You are a production AI research assistant using the ReAct pattern. "
                            "Answer from the observations, separate facts from inferences, include "
                            "architecture tradeoffs, and cite source labels or URLs when available."
                        ),
                    ),
                    ChatMessage(
                        role="user",
                        content=(
                            f"Research task: {state.task}\n\n"
                            f"Relevant prior memory:\n{memory_context or 'none'}\n\n"
                            f"Evidence:\n{evidence}"
                        ),
                    ),
                ],
                temperature=0.2,
            )
        )
        return response.content

    def _write_reusable_memories(self, state: AgentState, final_answer: str) -> None:
        task_key = _memory_key(state.task)
        self.memory.remember(
            kind="research_summary",
            key=task_key,
            value=final_answer[:2000],
            source=f"research_run:{state.artifacts.get('run_id')}",
        )
        for step in state.steps:
            if step.sources:
                self.memory.remember(
                    kind="source_set",
                    key=_memory_key(step.action_input),
                    value=", ".join(step.sources[:10]),
                    source=f"research_run:{state.artifacts.get('run_id')}",
                )

    def _format_trace(self, state: AgentState) -> str:
        lines = ["ReAct Trace"]
        for index, step in enumerate(state.steps, start=1):
            lines.extend(
                [
                    f"\nStep {index}",
                    f"Thought: {step.thought}",
                    f"Action: {step.action}",
                    f"Action Input: {step.action_input}",
                    f"Observation: {step.observation}",
                    f"Sources: {', '.join(step.sources) or 'none'}",
                ]
            )
        return "\n".join(lines)

    def _format_memory_summary(self, state: AgentState) -> str:
        prior = state.artifacts.get("prior_memories", [])
        lines = [
            "Memory / Storage",
            f"Backend: sqlite",
            f"Database: {self.memory.database_path}",
            f"Run ID: {state.artifacts.get('run_id')}",
            f"Prior memories used: {len(prior)}",
        ]
        for item in prior[:3]:
            lines.append(f"- {item['kind']}:{item['key']}")
        return "\n".join(lines)


class ReferenceAgent(ResearchAssistantAgent):
    """Backward-compatible alias used by the generated smoke test."""

    def __init__(
        self,
        router: ModelRouter | None = None,
        enable_web: bool | None = None,
        max_steps: int = 3,
        web_search_mode: str | None = None,
        memory: SQLiteResearchMemory | None = None,
    ):
        if router is None:
            from shared.llm import build_default_router

            router = build_default_router()
        super().__init__(
            router=router,
            enable_web=enable_web,
            max_steps=max_steps,
            web_search_mode=web_search_mode,
            memory=memory,
        )


def web_search_mode_from_env() -> str:
    mode = os.getenv("WEB_SEARCH_MODE")
    if mode:
        return mode.lower()
    legacy = os.getenv("ENABLE_WEB_SEARCH")
    if legacy is None:
        return "auto"
    return "auto" if legacy.lower() in {"1", "true", "yes", "on"} else "off"


def memory_path_from_env() -> Path:
    configured = os.getenv("RESEARCH_MEMORY_DB")
    if configured:
        return Path(configured).expanduser()
    return PROJECT_ROOT / "storage/research_memory.sqlite3"


def _looks_current_or_external(query: str) -> bool:
    lowered = query.lower()
    return any(
        marker in lowered
        for marker in (
            "latest",
            "current",
            "today",
            "2025",
            "2026",
            "web",
            "news",
            "github",
            "paper",
            "benchmark",
        )
    )


def _extract_json_object(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        return text
    return text[start : end + 1]


def _memory_key(text: str) -> str:
    tokens = [
        token
        for token in "".join(ch.lower() if ch.isalnum() else " " for ch in text).split()
        if token
    ]
    return "-".join(tokens[:12]) or "untitled"
