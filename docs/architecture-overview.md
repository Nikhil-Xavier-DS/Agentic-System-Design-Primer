# Architecture Overview

Production agent systems are distributed systems with probabilistic components. The core design question is not only how to prompt a model, but how to coordinate state, tools, memory, failure handling, observability, and governance around model calls.

```mermaid
flowchart TB
    Request[User / Event / Schedule] --> Workflow[Workflow Orchestrator]
    Workflow --> Policy[Policy and Guardrails]
    Workflow --> Agent[Agent Runtime]
    Agent --> Router[Model Router]
    Agent --> ToolRuntime[Tool Runtime]
    Agent --> Memory[Memory Layer]
    Workflow --> Checkpoints[(Checkpoints)]
    Workflow --> Events[(Event Log)]
    Agent --> Telemetry[Traces / Metrics / Logs]
```

Key production boundaries:

- The orchestrator owns workflow state and retries.
- Agents own task reasoning and tool selection.
- Tools own deterministic external side effects.
- Memory systems own durable context and retrieval.
- Provider adapters own vendor-specific LLM behavior.
