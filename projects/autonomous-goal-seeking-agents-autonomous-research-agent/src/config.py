from __future__ import annotations

from pydantic import BaseModel


class ProjectConfig(BaseModel):
    model_provider: str = "mock"
    enable_observability: bool = True
    max_workflow_steps: int = 12
    checkpoint_backend: str = "memory"
