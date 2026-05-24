# Production Engineering

Agent systems need the same rigor as distributed systems, plus controls for nondeterminism.

Critical topics:

- Explicit workflow state and checkpointing
- Retry policies with idempotency keys
- Tool sandboxing and permission boundaries
- Prompt injection defenses for retrieved and user-provided content
- Audit logging for actions, approvals, model calls, and tool calls
- Cost, latency, and token budgets
- Context engineering and memory compaction
- Multi-tenant isolation and secret management
- Golden task evaluation before deployment
