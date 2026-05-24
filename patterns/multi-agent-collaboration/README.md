# Multi-Agent Collaboration

Coordinate specialized peers through shared protocols.

## Production Use Cases

- Build workflows where reasoning must be explicit and inspectable.
- Separate probabilistic decisions from deterministic tools.
- Capture intermediate state for replay, evaluation, and debugging.

## Architecture

```mermaid
flowchart TB
    Input[Task Input] --> Agent[Multi-Agent Collaboration]
    Agent --> State[(Working State)]
    Agent --> Tools[Tool Layer]
    Agent --> Router[Provider Router]
    Router --> Cloud[Cloud LLM]
    Router --> Local[Ollama / Local Model]
    Agent --> Eval[Evaluation]
    Agent --> Obs[Observability]
```

## Runnable Project

See `projects/multi-agent-collaboration-startup-company-simulation`.

## Engineering Checklist

- Define state schema before prompts.
- Make every tool call typed, observable, and retry-aware.
- Add evaluation tasks for expected behavior and known failure modes.
- Provide local/offline mode through Ollama or mock provider.
