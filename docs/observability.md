# Observability

Observe model calls, tool calls, workflow transitions, retrieval, memory writes, and human approvals.

```mermaid
flowchart LR
    Agent --> Traces[OpenTelemetry Traces]
    Agent --> Metrics[Prometheus Metrics]
    Agent --> Logs[Structured Logs]
    Traces --> Grafana[Grafana]
    Metrics --> Grafana
    Logs --> SIEM[Security / Audit Store]
```

Recommended telemetry:

- Latency by provider, model, tool, and workflow node
- Token usage and estimated cost
- Retrieval hit rate and citation coverage
- Tool error rates and retry counts
- Human approval queue age
- Hallucination and groundedness evaluation scores
