# Production Notes

The Enterprise Workflow Engine should use durable workflow checkpoints, typed tools, explicit state transitions, and provider-agnostic model calls.

Scaling concerns:

- Queue long-running work.
- Separate API and worker processes.
- Cache deterministic retrieval and tool outputs.
- Budget model calls by workflow and tenant.
- Use local Ollama inference for privacy-sensitive or offline paths.
