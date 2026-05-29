# Storage

The ReAct research assistant uses SQLite as its default durable local storage.

Default database:

```text
projects/react-agent-ai-research-assistant/storage/research_memory.sqlite3
```

Stored data:

- `research_runs`: task, metadata, final answer, run timestamps
- `research_steps`: thought/action/observation records for every ReAct step
- `research_sources`: source provenance for observations
- `memories`: reusable research summaries and source sets recalled in future runs

Override the database path:

```bash
RESEARCH_MEMORY_DB=/tmp/research.sqlite3 python projects/react-agent-ai-research-assistant/src/main.py "Research local-first agent architectures"
python projects/react-agent-ai-research-assistant/src/main.py --memory-db /tmp/research.sqlite3 "Research local-first agent architectures"
```

Inspect recent runs:

```bash
python projects/react-agent-ai-research-assistant/src/main.py --show-memory
```
