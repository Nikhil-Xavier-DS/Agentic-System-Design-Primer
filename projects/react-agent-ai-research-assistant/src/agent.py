from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentState:
    task: str
    steps: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    artifacts: dict[str, Any] = field(default_factory=dict)


class ReferenceAgent:
    """Minimal extension point for the AI Research Assistant.

    Replace the placeholder methods with pattern-specific planning, tool use,
    memory, graph transitions, approvals, or event handlers.
    """

    pattern = "ReAct Agent"

    def initialize(self, task: str) -> AgentState:
        return AgentState(task=task, steps=["initialize"])

    def record_observation(self, state: AgentState, observation: str) -> AgentState:
        state.observations.append(observation)
        return state
