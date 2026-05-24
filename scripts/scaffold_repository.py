from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[1]


PATTERNS = [
    ("react-agent", "ReAct Agent", "AI Research Assistant", "Reasoning and acting loop with tools and explicit observations."),
    ("planner-executor", "Planner-Executor", "Travel Planning Agent", "Separate strategic planning from tactical execution."),
    ("reflection-self-critique", "Reflection / Self-Critique", "Self-Correcting Coding Agent", "Critique, revise, and verify outputs before finalization."),
    ("tree-of-thoughts", "Tree of Thoughts", "Strategy Game Agent", "Explore, score, and prune multiple reasoning branches."),
    ("rag-agent", "RAG Agent", "Enterprise Document Chatbot", "Ground responses in retrieved, cited enterprise knowledge."),
    ("memory-centric-agent", "Memory-Centric Agent", "Persistent Personal Assistant", "Use durable short-term, episodic, and semantic memory."),
    ("multi-agent-collaboration", "Multi-Agent Collaboration", "Startup Company Simulation", "Coordinate specialized peers through shared protocols."),
    ("hierarchical-agents", "Hierarchical Agents", "Autonomous Software Company", "Delegate work through manager-worker agent layers."),
    ("debate-agents", "Debate Agents", "AI Debate Arena", "Use adversarial perspectives to improve conclusions."),
    ("graph-based-orchestration", "Graph-Based Orchestration", "Enterprise Workflow Engine", "Represent agent workflows as explicit state graphs."),
    ("event-driven-agents", "Event-Driven Agents", "Slack Incident Response Bot", "React to events through queues, handlers, and durable state."),
    ("human-in-the-loop", "Human-in-the-Loop", "Legal Contract Review Agent", "Escalate uncertain or high-risk decisions to people."),
    ("autonomous-goal-seeking-agents", "Autonomous Goal-Seeking Agents", "Autonomous Research Agent", "Continuously plan, execute, observe, and replan toward goals."),
    ("blackboard-architecture", "Blackboard Architecture", "Collaborative Problem Solving System", "Let independent specialists contribute to shared working memory."),
]


STORAGE = [
    ("vector-databases", "Vector Databases", "Semantic similarity search for retrieval, memory, and deduplication."),
    ("sql-databases", "SQL Databases", "Transactional state, audit logs, checkpoints, and user data."),
    ("knowledge-graphs", "Knowledge Graphs", "Entity, relation, provenance, and multi-hop reasoning stores."),
    ("redis-caching", "Redis / Caching", "Low-latency ephemeral state, locks, queues, and semantic caches."),
    ("hybrid-memory", "Hybrid Memory Systems", "Layered working, episodic, semantic, and procedural memory."),
    ("event-sourcing", "Event Sourcing", "Append-only agent state transitions and replayable workflows."),
    ("object-storage", "Blob/Object Storage", "Artifacts, documents, traces, model outputs, and large context payloads."),
    ("semantic-caching", "Semantic Caching", "Embedding-based reuse of prior completions and retrieval results."),
]


ROOT_FILES = {
    "README.md": """
        # Production Agent Engineering

        A production-grade system design repository for agentic AI architectures across cloud and local-first inference.

        This repository is organized like an engineering handbook plus runnable reference implementations. It focuses on how real agent systems are designed, deployed, observed, evaluated, and scaled.

        ## What This Repository Covers

        - Agentic design patterns with theory, diagrams, tradeoffs, and failure modes
        - Runnable Python projects for each pattern
        - Shared provider abstraction for OpenAI, Anthropic, Ollama, OpenAI-compatible APIs, and local GGUF-backed serving
        - Storage and memory architectures for vector, SQL, graph, cache, event-sourced, and hybrid systems
        - Orchestration patterns using explicit workflow state, eventing, graphs, and human approvals
        - Production concerns: observability, security, governance, retries, cost, latency, context engineering, and auditability
        - Evaluation and benchmarking harnesses for latency, retrieval quality, hallucination risk, tool reliability, and local model performance

        ## Quick Start

        ```bash
        python -m venv .venv
        source .venv/bin/activate
        pip install -e .
        cp .env.example .env
        python projects/react-agent-ai-research-assistant/src/main.py "Research local-first agent architectures"
        ```

        Local-first with Ollama:

        ```bash
        ollama pull llama3
        ollama pull mistral
        ollama serve
        MODEL_PROVIDER=ollama OLLAMA_MODEL=llama3 python projects/rag-agent-enterprise-document-chatbot/src/main.py "Summarize the policy corpus"
        ```

        Cloud mode:

        ```bash
        MODEL_PROVIDER=openai OPENAI_MODEL=gpt-4o-mini OPENAI_API_KEY=... python projects/planner-executor-travel-planning-agent/src/main.py "Plan 5 days in Tokyo"
        ```

        ## Repository Map

        ```text
        patterns/            Pattern theory, architecture, diagrams, tradeoffs, failure modes
        projects/            Runnable implementations mapped to every pattern
        shared/              Provider abstraction, telemetry, tools, memory, evaluation helpers
        storage-patterns/    Vector, SQL, graph, cache, event sourcing, object storage, semantic cache
        orchestration/       Workflow, event-driven, graph, checkpointing, and HITL design notes
        benchmarks/          Benchmark harnesses and experiment templates
        comparisons/         Pattern, provider, storage, framework, and model comparison matrices
        diagrams/            Global Mermaid architecture diagrams
        docs/                Production engineering guides
        papers/              Reading lists and annotated paper notes
        datasets/            Dataset manifests and small sample data
        notebooks/           Experiment notebooks
        ```

        ## Design Patterns

        | Pattern | Runnable Project | Best For |
        | --- | --- | --- |
        | ReAct Agent | AI Research Assistant | Tool use, search, stepwise reasoning |
        | Planner-Executor | Travel Planning Agent | Complex tasks with decomposable subtasks |
        | Reflection / Self-Critique | Self-Correcting Coding Agent | Quality improvement and verification loops |
        | Tree of Thoughts | Strategy Game Agent | Branching search and strategic reasoning |
        | RAG Agent | Enterprise Document Chatbot | Grounded answers over private knowledge |
        | Memory-Centric Agent | Persistent Personal Assistant | Personalized durable context |
        | Multi-Agent Collaboration | Startup Company Simulation | Specialist collaboration |
        | Hierarchical Agents | Autonomous Software Company | Delegation and management layers |
        | Debate Agents | AI Debate Arena | Adversarial evaluation and robust conclusions |
        | Graph-Based Orchestration | Enterprise Workflow Engine | Typed state machines and workflow control |
        | Event-Driven Agents | Slack Incident Response Bot | Async events, alerts, incidents |
        | Human-in-the-Loop | Legal Contract Review Agent | Approval gates and high-risk workflows |
        | Autonomous Goal-Seeking Agents | Autonomous Research Agent | Long-running goal pursuit |
        | Blackboard Architecture | Collaborative Problem Solving System | Shared problem state across specialists |

        ## Provider Abstraction

        ```mermaid
        flowchart LR
            Agent[Agent Logic] --> Router[Model Router]
            Router --> Policy[Routing Policy]
            Router --> OpenAI[OpenAI Provider]
            Router --> Anthropic[Anthropic Provider]
            Router --> Ollama[Ollama Provider]
            Router --> Compatible[OpenAI-Compatible API]
            Ollama --> LocalModels[llama3 / mistral / qwen / codellama / phi / deepseek-coder]
            Agent --> Tools[Tools]
            Agent --> Memory[Memory Stores]
            Agent --> Traces[OpenTelemetry Traces]
        ```

        Agents depend on `shared.llm.base_provider.LLMProvider`, not vendor SDKs. This keeps provider swapping, fallback routing, local/offline execution, and test doubles isolated from agent logic.

        ## Ollama Setup

        ```bash
        brew install ollama
        ollama serve
        ollama pull llama3
        ollama pull mistral
        ollama pull qwen
        ollama pull codellama
        ollama pull phi
        ollama pull deepseek-coder
        ```

        See [docs/ollama-local-models.md](docs/ollama-local-models.md) for CPU-only operation, GPU acceleration, Docker, quantization, llama.cpp, vLLM, batching, and performance tuning.

        ## Global Architecture

        ```mermaid
        flowchart TB
            UI[API / CLI / Worker] --> Orchestrator[Agent Orchestrator]
            Orchestrator --> AgentState[(Checkpointed Agent State)]
            Orchestrator --> LLM[Provider Router]
            Orchestrator --> Tools[Tool Runtime]
            Orchestrator --> Memory[Memory Layer]
            Memory --> Vector[(Qdrant)]
            Memory --> SQL[(PostgreSQL)]
            Memory --> Graph[(Neo4j)]
            Memory --> Cache[(Redis)]
            Memory --> Blob[(Object Storage)]
            Orchestrator --> Eval[Evaluation Harness]
            Orchestrator --> Obs[OpenTelemetry / Prometheus / Grafana]
        ```

        ## Benchmarks

        ```bash
        python benchmarks/run_latency.py --provider ollama --model llama3
        python benchmarks/run_retrieval_quality.py --dataset datasets/sample_corpus.jsonl
        python projects/tree-of-thoughts-strategy-game-agent/benchmarks/benchmark.py
        ```

        Benchmark dimensions include latency, tokens, cost, retrieval quality, tool success rate, orchestration overhead, hallucination risk, and quantized local model throughput.

        ## Roadmap

        - Add complete FastAPI services for selected reference projects
        - Add LangGraph, CrewAI, and AutoGen variants for comparable workflows
        - Add Qdrant/PostgreSQL/Redis/Neo4j docker profiles
        - Add golden task suites and regression evaluation dashboards
        - Add local model benchmark reports for llama3, mistral, qwen, codellama, phi, and deepseek-coder
        - Add production deployment guides for Kubernetes and GPU-backed local inference

        ## Contributing

        Contributions should improve engineering depth: runnable code, better failure analysis, measurement, operational guidance, diagrams, or realistic production tradeoffs.
    """,
    ".env.example": """
        MODEL_PROVIDER=mock
        MODEL_FALLBACK_PROVIDERS=ollama,openai
        OPENAI_API_KEY=
        OPENAI_MODEL=gpt-4o-mini
        ANTHROPIC_API_KEY=
        ANTHROPIC_MODEL=claude-3-5-haiku-latest
        OPENAI_COMPATIBLE_BASE_URL=
        OPENAI_COMPATIBLE_API_KEY=
        OPENAI_COMPATIBLE_MODEL=
        OLLAMA_BASE_URL=http://localhost:11434
        OLLAMA_MODEL=llama3
        LOCAL_GGUF_MODEL_PATH=
        LOG_LEVEL=INFO
        OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
    """,
    "pyproject.toml": """
        [build-system]
        requires = ["setuptools>=68", "wheel"]
        build-backend = "setuptools.build_meta"

        [project]
        name = "production-agent-engineering"
        version = "0.1.0"
        description = "Agentic AI system design patterns for cloud and local-first AI systems."
        requires-python = ">=3.10"
        dependencies = [
          "pydantic>=2.6",
          "httpx>=0.26",
          "tenacity>=8.2",
          "python-dotenv>=1.0",
          "fastapi>=0.110",
          "uvicorn>=0.27",
        ]

        [project.optional-dependencies]
        cloud = ["openai>=1.30", "anthropic>=0.25"]
        storage = ["redis>=5", "qdrant-client>=1.9", "neo4j>=5", "psycopg[binary]>=3.1"]
        observability = ["opentelemetry-api>=1.24", "opentelemetry-sdk>=1.24", "prometheus-client>=0.20"]
        dev = ["pytest>=8.0", "ruff>=0.4"]

        [tool.setuptools.packages.find]
        include = ["shared*"]

        [tool.ruff]
        line-length = 100
    """,
    "Makefile": """
        .PHONY: install test lint ollama benchmark

        install:
        \tpip install -e ".[dev,cloud,storage,observability]"

        test:
        \tpytest

        lint:
        \truff check .

        ollama:
        \tollama serve

        benchmark:
        \tpython benchmarks/run_latency.py --provider $${MODEL_PROVIDER:-mock} --model $${OLLAMA_MODEL:-mock-model}
    """,
    "docker-compose.yml": """
        services:
          postgres:
            image: postgres:16
            environment:
              POSTGRES_PASSWORD: agent
              POSTGRES_USER: agent
              POSTGRES_DB: agents
            ports: ["5432:5432"]
          redis:
            image: redis:7
            ports: ["6379:6379"]
          qdrant:
            image: qdrant/qdrant:latest
            ports: ["6333:6333"]
          neo4j:
            image: neo4j:5
            environment:
              NEO4J_AUTH: neo4j/agentpassword
            ports: ["7474:7474", "7687:7687"]
          prometheus:
            image: prom/prometheus:latest
            volumes:
              - ./infra/prometheus.yml:/etc/prometheus/prometheus.yml
            ports: ["9090:9090"]
          grafana:
            image: grafana/grafana:latest
            ports: ["3000:3000"]
    """,
    "CONTRIBUTING.md": """
        # Contributing

        Contributions should be practical, measurable, and production-oriented.

        Preferred contribution types:

        - Runnable implementations for a pattern or storage architecture
        - Better architecture diagrams
        - Failure mode analysis grounded in real systems
        - Benchmarks and evaluation datasets
        - Provider support improvements
        - Observability, security, and deployment guidance

        Every project contribution should include `.env.example`, local/offline mode, cloud mode, Docker support, observability notes, benchmark scripts, and security considerations.
    """,
    "LICENSE": "MIT License\n\nCopyright (c) 2026\n\nPermission is hereby granted, free of charge, to any person obtaining a copy.\n",
}


SHARED_FILES = {
    "shared/__init__.py": "",
    "shared/llm/__init__.py": """
        from .base_provider import ChatMessage, ChatRequest, ChatResponse, LLMProvider, ToolCall
        from .model_router import ModelRouter, build_default_router

        __all__ = [
            "ChatMessage",
            "ChatRequest",
            "ChatResponse",
            "LLMProvider",
            "ModelRouter",
            "ToolCall",
            "build_default_router",
        ]
    """,
    "shared/llm/base_provider.py": """
        from __future__ import annotations

        from abc import ABC, abstractmethod
        from collections.abc import AsyncIterator
        from dataclasses import dataclass, field
        from typing import Any


        @dataclass(frozen=True)
        class ChatMessage:
            role: str
            content: str
            name: str | None = None
            metadata: dict[str, Any] = field(default_factory=dict)


        @dataclass(frozen=True)
        class ToolCall:
            name: str
            arguments: dict[str, Any]


        @dataclass(frozen=True)
        class ChatRequest:
            messages: list[ChatMessage]
            model: str | None = None
            temperature: float = 0.2
            max_tokens: int | None = None
            tools: list[dict[str, Any]] = field(default_factory=list)
            response_format: dict[str, Any] | None = None
            metadata: dict[str, Any] = field(default_factory=dict)


        @dataclass(frozen=True)
        class ChatResponse:
            content: str
            model: str
            provider: str
            usage: dict[str, Any] = field(default_factory=dict)
            tool_calls: list[ToolCall] = field(default_factory=list)
            raw: Any | None = None


        class LLMProvider(ABC):
            name: str

            @abstractmethod
            async def chat(self, request: ChatRequest) -> ChatResponse:
                raise NotImplementedError

            async def stream(self, request: ChatRequest) -> AsyncIterator[str]:
                response = await self.chat(request)
                yield response.content

            async def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
                raise NotImplementedError(f"{self.name} does not implement embeddings")
    """,
    "shared/llm/config.py": """
        from __future__ import annotations

        import os
        from dataclasses import dataclass


        @dataclass(frozen=True)
        class LLMConfig:
            model_provider: str = "mock"
            fallback_providers: tuple[str, ...] = ()
            openai_api_key: str | None = None
            openai_model: str = "gpt-4o-mini"
            anthropic_api_key: str | None = None
            anthropic_model: str = "claude-3-5-haiku-latest"
            ollama_base_url: str = "http://localhost:11434"
            ollama_model: str = "llama3"
            openai_compatible_base_url: str | None = None
            openai_compatible_api_key: str | None = None
            openai_compatible_model: str | None = None
            local_gguf_model_path: str | None = None
            request_timeout_seconds: float = 60.0

            @classmethod
            def from_env(cls) -> "LLMConfig":
                fallbacks = tuple(
                    item.strip()
                    for item in os.getenv("MODEL_FALLBACK_PROVIDERS", "").split(",")
                    if item.strip()
                )
                return cls(
                    model_provider=os.getenv("MODEL_PROVIDER", "mock"),
                    fallback_providers=fallbacks,
                    openai_api_key=os.getenv("OPENAI_API_KEY") or None,
                    openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY") or None,
                    anthropic_model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-haiku-latest"),
                    ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
                    ollama_model=os.getenv("OLLAMA_MODEL", "llama3"),
                    openai_compatible_base_url=os.getenv("OPENAI_COMPATIBLE_BASE_URL") or None,
                    openai_compatible_api_key=os.getenv("OPENAI_COMPATIBLE_API_KEY") or None,
                    openai_compatible_model=os.getenv("OPENAI_COMPATIBLE_MODEL") or None,
                    local_gguf_model_path=os.getenv("LOCAL_GGUF_MODEL_PATH") or None,
                    request_timeout_seconds=float(os.getenv("LLM_TIMEOUT_SECONDS", "60")),
                )
    """,
    "shared/llm/ollama_provider.py": """
        from __future__ import annotations

        import httpx
        from tenacity import retry, stop_after_attempt, wait_exponential

        from .base_provider import ChatRequest, ChatResponse, LLMProvider
        from .config import LLMConfig


        class OllamaProvider(LLMProvider):
            name = "ollama"

            def __init__(self, config: LLMConfig):
                self.config = config

            @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=0.5, max=4))
            async def chat(self, request: ChatRequest) -> ChatResponse:
                model = request.model or self.config.ollama_model
                payload = {
                    "model": model,
                    "messages": [
                        {"role": message.role, "content": message.content}
                        for message in request.messages
                    ],
                    "stream": False,
                    "options": {"temperature": request.temperature},
                }
                async with httpx.AsyncClient(timeout=self.config.request_timeout_seconds) as client:
                    response = await client.post(f"{self.config.ollama_base_url}/api/chat", json=payload)
                    response.raise_for_status()
                    data = response.json()
                return ChatResponse(
                    content=data.get("message", {}).get("content", ""),
                    model=model,
                    provider=self.name,
                    usage={
                        "prompt_eval_count": data.get("prompt_eval_count"),
                        "eval_count": data.get("eval_count"),
                    },
                    raw=data,
                )

            async def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
                selected_model = model or self.config.ollama_model
                vectors: list[list[float]] = []
                async with httpx.AsyncClient(timeout=self.config.request_timeout_seconds) as client:
                    for text in texts:
                        response = await client.post(
                            f"{self.config.ollama_base_url}/api/embeddings",
                            json={"model": selected_model, "prompt": text},
                        )
                        response.raise_for_status()
                        vectors.append(response.json()["embedding"])
                return vectors
    """,
    "shared/llm/openai_provider.py": """
        from __future__ import annotations

        from .base_provider import ChatRequest, ChatResponse, LLMProvider
        from .config import LLMConfig


        class OpenAIProvider(LLMProvider):
            name = "openai"

            def __init__(self, config: LLMConfig):
                self.config = config

            async def chat(self, request: ChatRequest) -> ChatResponse:
                try:
                    from openai import AsyncOpenAI
                except ImportError as exc:
                    raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
                client = AsyncOpenAI(api_key=self.config.openai_api_key)
                model = request.model or self.config.openai_model
                response = await client.chat.completions.create(
                    model=model,
                    messages=[message.__dict__ for message in request.messages],
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )
                return ChatResponse(
                    content=response.choices[0].message.content or "",
                    model=model,
                    provider=self.name,
                    usage=response.usage.model_dump() if response.usage else {},
                    raw=response,
                )


        class OpenAICompatibleProvider(OpenAIProvider):
            name = "openai-compatible"

            async def chat(self, request: ChatRequest) -> ChatResponse:
                try:
                    from openai import AsyncOpenAI
                except ImportError as exc:
                    raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
                client = AsyncOpenAI(
                    api_key=self.config.openai_compatible_api_key,
                    base_url=self.config.openai_compatible_base_url,
                )
                model = request.model or self.config.openai_compatible_model or self.config.openai_model
                response = await client.chat.completions.create(
                    model=model,
                    messages=[message.__dict__ for message in request.messages],
                    temperature=request.temperature,
                    max_tokens=request.max_tokens,
                )
                return ChatResponse(
                    content=response.choices[0].message.content or "",
                    model=model,
                    provider=self.name,
                    usage=response.usage.model_dump() if response.usage else {},
                    raw=response,
                )
    """,
    "shared/llm/anthropic_provider.py": """
        from __future__ import annotations

        from .base_provider import ChatRequest, ChatResponse, LLMProvider
        from .config import LLMConfig


        class AnthropicProvider(LLMProvider):
            name = "anthropic"

            def __init__(self, config: LLMConfig):
                self.config = config

            async def chat(self, request: ChatRequest) -> ChatResponse:
                try:
                    from anthropic import AsyncAnthropic
                except ImportError as exc:
                    raise RuntimeError("Install the cloud extras: pip install -e '.[cloud]'") from exc
                client = AsyncAnthropic(api_key=self.config.anthropic_api_key)
                system = "\\n".join(m.content for m in request.messages if m.role == "system")
                messages = [
                    {"role": m.role, "content": m.content}
                    for m in request.messages
                    if m.role != "system"
                ]
                model = request.model or self.config.anthropic_model
                response = await client.messages.create(
                    model=model,
                    max_tokens=request.max_tokens or 1024,
                    temperature=request.temperature,
                    system=system or None,
                    messages=messages,
                )
                text = "".join(block.text for block in response.content if block.type == "text")
                return ChatResponse(content=text, model=model, provider=self.name, raw=response)
    """,
    "shared/llm/model_router.py": """
        from __future__ import annotations

        from collections.abc import Iterable

        from .anthropic_provider import AnthropicProvider
        from .base_provider import ChatRequest, ChatResponse, LLMProvider
        from .config import LLMConfig
        from .ollama_provider import OllamaProvider
        from .openai_provider import OpenAICompatibleProvider, OpenAIProvider


        class MockProvider(LLMProvider):
            name = "mock"

            async def chat(self, request: ChatRequest) -> ChatResponse:
                last = request.messages[-1].content if request.messages else ""
                return ChatResponse(
                    content=f"[mock] Planned response for: {last}",
                    model=request.model or "mock-model",
                    provider=self.name,
                    usage={"prompt_tokens": len(last.split()), "completion_tokens": 6},
                )

            async def embed(self, texts: list[str], model: str | None = None) -> list[list[float]]:
                return [[float((hash(text) + i) % 997) / 997 for i in range(16)] for text in texts]


        class ModelRouter:
            def __init__(self, providers: dict[str, LLMProvider], default_provider: str, fallbacks: Iterable[str] = ()):
                self.providers = providers
                self.default_provider = default_provider
                self.fallbacks = tuple(fallbacks)

            async def chat(self, request: ChatRequest, provider: str | None = None) -> ChatResponse:
                provider_chain = (provider or self.default_provider, *self.fallbacks, "mock")
                errors: list[str] = []
                for provider_name in provider_chain:
                    selected = self.providers.get(provider_name)
                    if selected is None:
                        continue
                    try:
                        return await selected.chat(request)
                    except Exception as exc:  # noqa: BLE001 - router must preserve fallback behavior
                        errors.append(f"{provider_name}: {exc}")
                raise RuntimeError("All providers failed: " + " | ".join(errors))


        def build_default_router(config: LLMConfig | None = None) -> ModelRouter:
            cfg = config or LLMConfig.from_env()
            providers: dict[str, LLMProvider] = {
                "mock": MockProvider(),
                "ollama": OllamaProvider(cfg),
                "openai": OpenAIProvider(cfg),
                "anthropic": AnthropicProvider(cfg),
                "openai-compatible": OpenAICompatibleProvider(cfg),
            }
            return ModelRouter(providers, cfg.model_provider, cfg.fallback_providers)
    """,
    "shared/llm/embeddings.py": """
        from __future__ import annotations

        from .model_router import build_default_router


        async def embed_texts(texts: list[str], provider: str | None = None, model: str | None = None) -> list[list[float]]:
            router = build_default_router()
            selected = router.providers[provider or router.default_provider]
            return await selected.embed(texts, model=model)
    """,
    "shared/llm/structured_output.py": """
        from __future__ import annotations

        import json
        from typing import TypeVar

        from pydantic import BaseModel, ValidationError

        from .base_provider import ChatMessage, ChatRequest
        from .model_router import build_default_router


        T = TypeVar("T", bound=BaseModel)


        async def generate_structured(prompt: str, schema: type[T]) -> T:
            router = build_default_router()
            response = await router.chat(
                ChatRequest(
                    messages=[
                        ChatMessage(role="system", content="Return only valid JSON matching the requested schema."),
                        ChatMessage(role="user", content=f"{prompt}\\nSchema: {schema.model_json_schema()}"),
                    ],
                    temperature=0,
                )
            )
            try:
                return schema.model_validate_json(response.content)
            except ValidationError:
                return schema.model_validate(json.loads(response.content))
    """,
}


DOCS = {
    "docs/architecture-overview.md": """
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
    """,
    "docs/ollama-local-models.md": """
        # Ollama and Local Model Setup

        Ollama is the primary local inference path in this repository.

        ```bash
        brew install ollama
        ollama serve
        ollama pull llama3
        ollama pull mistral
        ollama pull deepseek-coder
        ollama pull qwen
        ollama pull codellama
        ollama pull phi
        ```

        CPU-only mode works for small and quantized models, but latency rises quickly with context size. Use smaller quantizations, reduce max output tokens, and prefer retrieval over long prompt stuffing.

        GPU acceleration depends on platform support. On Linux with NVIDIA GPUs, run Ollama with the NVIDIA container runtime or native drivers. For higher throughput serving, compare Ollama with vLLM for batching and llama.cpp for GGUF portability.

        Local deployment pattern:

        ```mermaid
        flowchart LR
            Agent[Agent Service] --> Router[Model Router]
            Router --> Ollama[Ollama Server]
            Ollama --> Models[(Local Model Cache)]
            Router --> Fallback[Cloud Fallback]
            Agent --> Cache[(Semantic Cache)]
        ```

        Optimization checklist:

        - Keep prompts compact and structured.
        - Use quantized models for memory-constrained devices.
        - Batch independent requests when throughput matters.
        - Cache embeddings and deterministic tool results.
        - Benchmark per task, not only generic tokens per second.
    """,
    "docs/provider-abstraction.md": """
        # Provider Abstraction

        Agent logic calls `ModelRouter.chat()` and never imports vendor SDKs directly. Providers implement a common contract for chat, streaming, embeddings, tool calling, structured outputs, retries, and rate limits.

        ```mermaid
        classDiagram
            class LLMProvider {
              +chat(ChatRequest) ChatResponse
              +stream(ChatRequest) AsyncIterator~str~
              +embed(list~str~) list~vector~
            }
            class ModelRouter {
              +chat(ChatRequest, provider)
            }
            LLMProvider <|-- OpenAIProvider
            LLMProvider <|-- AnthropicProvider
            LLMProvider <|-- OllamaProvider
            LLMProvider <|-- OpenAICompatibleProvider
            ModelRouter --> LLMProvider
        ```

        Design goals:

        - Swap providers without changing agents.
        - Prefer local-first operation with cloud fallback.
        - Support offline demos through the mock provider.
        - Centralize retries, timeouts, rate limits, and structured output handling.
    """,
    "docs/production-engineering.md": """
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
    """,
    "docs/observability.md": """
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
    """,
    "docs/security-governance.md": """
        # Security and Governance

        Agent systems expand the attack surface because models interpret untrusted text and can trigger tools.

        Controls:

        - Treat retrieved documents and web content as untrusted input.
        - Isolate tools with least privilege credentials.
        - Require human approval for irreversible or high-impact actions.
        - Redact secrets before prompts and logs.
        - Use allowlisted tools and typed schemas.
        - Store model calls and actions in audit logs.
        - Evaluate prompt injection, data exfiltration, and unsafe tool use.
    """,
    "docs/docker-deployment.md": """
        # Docker Architecture

        ```mermaid
        flowchart TB
            Compose[Docker Compose] --> AgentAPI[Agent API]
            Compose --> Worker[Agent Worker]
            Compose --> Ollama[Ollama]
            Compose --> Postgres[(PostgreSQL)]
            Compose --> Redis[(Redis)]
            Compose --> Qdrant[(Qdrant)]
            Compose --> Neo4j[(Neo4j)]
            Compose --> Prometheus[Prometheus]
            Compose --> Grafana[Grafana]
        ```

        Use compose profiles to run only what a project needs. Local-first projects can run entirely without cloud credentials when `MODEL_PROVIDER=ollama` or `MODEL_PROVIDER=mock`.
    """,
    "docs/roadmap.md": """
        # Roadmap

        - Complete end-to-end FastAPI services for flagship projects.
        - Add LangGraph, CrewAI, and AutoGen versions for selected workflows.
        - Add benchmark reports across local and cloud models.
        - Add Kubernetes manifests and GPU deployment examples.
        - Add prompt injection and tool abuse evaluation suites.
        - Add realistic datasets and golden task regression tests.
    """,
    "docs/repo-names.md": """
        # Suggested Repository Names

        - production-agent-engineering
        - agentic-system-design-primer
        - agent-architecture-primer
        - local-first-agent-systems
        - ai-agent-design-patterns
        - scalable-agent-engineering
        - agentic-ai-systems-handbook
    """,
}


def clean(text: str) -> str:
    return dedent(text).strip() + "\n"


def write(path: str, content: str) -> None:
    target = ROOT / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(clean(content), encoding="utf-8")


def slug_project(pattern_slug: str, project: str) -> str:
    return f"{pattern_slug}-{project.lower().replace(' / ', '-').replace(' ', '-').replace(',', '').replace('–', '-')}"


def pattern_readme(slug: str, name: str, project: str, summary: str) -> str:
    return f"""
        # {name}

        {summary}

        ## Production Use Cases

        - Build workflows where reasoning must be explicit and inspectable.
        - Separate probabilistic decisions from deterministic tools.
        - Capture intermediate state for replay, evaluation, and debugging.

        ## Architecture

        ```mermaid
        flowchart TB
            Input[Task Input] --> Agent[{name}]
            Agent --> State[(Working State)]
            Agent --> Tools[Tool Layer]
            Agent --> Router[Provider Router]
            Router --> Cloud[Cloud LLM]
            Router --> Local[Ollama / Local Model]
            Agent --> Eval[Evaluation]
            Agent --> Obs[Observability]
        ```

        ## Runnable Project

        See `projects/{slug_project(slug, project)}`.

        ## Engineering Checklist

        - Define state schema before prompts.
        - Make every tool call typed, observable, and retry-aware.
        - Add evaluation tasks for expected behavior and known failure modes.
        - Provide local/offline mode through Ollama or mock provider.
    """


def project_main(project_title: str, pattern_name: str) -> str:
    return f"""
        from __future__ import annotations

        import asyncio
        import sys
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[3]
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))

        from shared.llm import ChatMessage, ChatRequest, build_default_router


        SYSTEM_PROMPT = \"\"\"You are running the {project_title} reference implementation.
        Use the {pattern_name} architecture. Be explicit about plan, state, tools, risks, and next action.
        Keep the response concise but implementation-minded.\"\"\"


        async def run(task: str) -> str:
            router = build_default_router()
            response = await router.chat(
                ChatRequest(
                    messages=[
                        ChatMessage(role="system", content=SYSTEM_PROMPT),
                        ChatMessage(role="user", content=task),
                    ],
                    temperature=0.2,
                )
            )
            return response.content


        def main() -> None:
            task = " ".join(sys.argv[1:]) or "Run a smoke test and explain the architecture."
            print(asyncio.run(run(task)))


        if __name__ == "__main__":
            main()
    """


def project_agent(project_title: str, pattern_name: str) -> str:
    return f"""
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
            \"\"\"Minimal extension point for the {project_title}.

            Replace the placeholder methods with pattern-specific planning, tool use,
            memory, graph transitions, approvals, or event handlers.
            \"\"\"

            pattern = "{pattern_name}"

            def initialize(self, task: str) -> AgentState:
                return AgentState(task=task, steps=["initialize"])

            def record_observation(self, state: AgentState, observation: str) -> AgentState:
                state.observations.append(observation)
                return state
    """


def project_readme(slug: str, name: str, project: str, summary: str) -> str:
    return f"""
        # {project}

        Pattern: **{name}**

        {summary}

        ## Architecture

        ```mermaid
        flowchart TB
            User[User / Trigger] --> API[CLI or FastAPI Entry]
            API --> Agent[{project}]
            Agent --> State[(Typed State)]
            Agent --> Router[Shared Provider Router]
            Router --> Ollama[Ollama Local Models]
            Router --> Cloud[Cloud Providers]
            Agent --> Tools[Project Tools]
            Agent --> Memory[Memory / Storage]
            Agent --> Eval[Evaluations]
            Agent --> Obs[Telemetry]
        ```

        ## Run

        ```bash
        cp .env.example .env
        MODEL_PROVIDER=mock python src/main.py "Run the reference workflow"
        MODEL_PROVIDER=ollama OLLAMA_MODEL=llama3 python src/main.py "Run locally"
        MODEL_PROVIDER=openai OPENAI_MODEL=gpt-4o-mini python src/main.py "Run in cloud mode"
        ```

        ## Main Components

        - `src/main.py`: CLI entry point using the shared provider abstraction.
        - `src/agent.py`: Agent state and extension points.
        - `benchmarks/benchmark.py`: Latency and workflow benchmark placeholder.
        - `evals/eval.py`: Golden task and behavior evaluation placeholder.
        - `docs/production.md`: Scaling, failure, observability, and security notes.

        ## Production Concerns

        - Checkpoint state between model/tool calls.
        - Add idempotency keys for side-effecting tools.
        - Trace provider calls, tool calls, memory reads, and memory writes.
        - Budget tokens, latency, and cost per workflow.
        - Prefer local Ollama mode for privacy-sensitive development and offline demos.

        ## Failure Modes

        - Invalid tool arguments
        - Stale or polluted memory
        - Prompt injection through user or retrieved content
        - Provider timeout or rate limit
        - Non-idempotent retries

        ## Benchmarks

        Track latency, token usage, tool success rate, retries, retrieval quality where applicable, and local model throughput.
    """


def generate_patterns() -> None:
    for slug, name, project, summary in PATTERNS:
        base = f"patterns/{slug}"
        files = {
            "README.md": pattern_readme(slug, name, project, summary),
            "theory.md": f"# Theory\\n\\n{name} focuses on {summary.lower()} The central design move is to make reasoning state explicit enough to inspect, replay, and evaluate.\\n",
            "architecture.md": f"# Architecture\\n\\nUse this pattern when the workflow benefits from {summary.lower()} Keep model calls behind the shared provider abstraction and keep tools typed.\\n",
            "production-notes.md": "# Production Notes\n\nAdd retries, checkpointing, telemetry, prompt injection controls, and cost budgets before production use.\n",
            "failure-modes.md": "# Failure Modes\n\n- Hallucinated state transitions\n- Invalid tool arguments\n- Unbounded loops\n- Context drift\n- Weak evaluation coverage\n",
            "tradeoffs.md": "# Tradeoffs\n\nThis pattern improves control and interpretability at the cost of orchestration complexity, latency, and more operational surfaces.\n",
            "observability.md": "# Observability\n\nTrace each model call, tool call, state transition, memory lookup, and evaluation score.\n",
            "security.md": "# Security\n\nUse least-privilege tools, secret redaction, approval gates for risky actions, and prompt injection testing.\n",
            "evals.md": "# Evaluations\n\nEvaluate task completion, groundedness, tool reliability, latency, cost, and regression behavior on golden tasks.\n",
            "diagrams/architecture.mmd": f"flowchart TB\n  Input[Input] --> Agent[{name}]\n  Agent --> State[(State)]\n  Agent --> Tools[Tools]\n  Agent --> LLM[Provider Router]\n  Agent --> Output[Output]\n",
            "implementation/README.md": f"# Implementation Notes\n\nReference implementation: `projects/{slug_project(slug, project)}`.\n",
        }
        for rel, content in files.items():
            write(f"{base}/{rel}", content)


def generate_projects() -> None:
    for slug, name, project, summary in PATTERNS:
        project_slug = slug_project(slug, project)
        base = f"projects/{project_slug}"
        files = {
            "README.md": project_readme(slug, name, project, summary),
            ".env.example": """
                MODEL_PROVIDER=mock
                MODEL_FALLBACK_PROVIDERS=ollama,openai
                OLLAMA_BASE_URL=http://localhost:11434
                OLLAMA_MODEL=llama3
                OPENAI_MODEL=gpt-4o-mini
                OPENAI_API_KEY=
                ANTHROPIC_MODEL=claude-3-5-haiku-latest
                ANTHROPIC_API_KEY=
                LOG_LEVEL=INFO
            """,
            "requirements.txt": "-e ../../\n",
            "Dockerfile": f"""
                FROM python:3.11-slim
                WORKDIR /app
                COPY . /app
                RUN pip install /app
                WORKDIR /app/projects/{project_slug}
                CMD ["python", "src/main.py", "Run the reference workflow"]
            """,
            "docker-compose.yml": """
                services:
                  app:
                    build:
                      context: ../..
                      dockerfile: projects/${PROJECT_DIR:-PROJECT}/Dockerfile
                    environment:
                      MODEL_PROVIDER: ${MODEL_PROVIDER:-ollama}
                      OLLAMA_BASE_URL: http://ollama:11434
                      OLLAMA_MODEL: ${OLLAMA_MODEL:-llama3}
                  ollama:
                    image: ollama/ollama:latest
                    ports: ["11434:11434"]
                    volumes:
                      - ollama:/root/.ollama
                volumes:
                  ollama:
            """.replace("PROJECT", project_slug),
            "src/main.py": project_main(project, name),
            "src/__init__.py": "",
            "src/agent.py": project_agent(project, name),
            "src/config.py": """
                from __future__ import annotations

                from pydantic import BaseModel


                class ProjectConfig(BaseModel):
                    model_provider: str = "mock"
                    enable_observability: bool = True
                    max_workflow_steps: int = 12
                    checkpoint_backend: str = "memory"
            """,
            "tests/test_smoke.py": f"""
                from pathlib import Path
                import sys

                PROJECT_ROOT = Path(__file__).resolve().parents[1]
                if str(PROJECT_ROOT) not in sys.path:
                    sys.path.insert(0, str(PROJECT_ROOT))

                from src.agent import ReferenceAgent


                def test_agent_initializes_state():
                    state = ReferenceAgent().initialize("test task")
                    assert state.task == "test task"
                    assert "{name}" == ReferenceAgent.pattern
            """,
            "benchmarks/benchmark.py": """
                from __future__ import annotations

                import asyncio
                import sys
                import time
                from pathlib import Path

                ROOT = Path(__file__).resolve().parents[3]
                if str(ROOT) not in sys.path:
                    sys.path.insert(0, str(ROOT))
                PROJECT_ROOT = Path(__file__).resolve().parents[1]
                if str(PROJECT_ROOT) not in sys.path:
                    sys.path.insert(0, str(PROJECT_ROOT))

                from src.main import run


                async def main() -> None:
                    start = time.perf_counter()
                    await run("Benchmark the reference workflow.")
                    elapsed = time.perf_counter() - start
                    print({"latency_seconds": round(elapsed, 4)})


                if __name__ == "__main__":
                    asyncio.run(main())
            """,
            "evals/eval.py": """
                from __future__ import annotations

                GOLDEN_TASKS = [
                    "Explain the workflow state.",
                    "List likely failure modes.",
                    "Recommend observability signals.",
                ]


                def main() -> None:
                    for task in GOLDEN_TASKS:
                        print({"task": task, "status": "pending-human-review"})


                if __name__ == "__main__":
                    main()
            """,
            "docs/production.md": f"""
                # Production Notes

                The {project} should use durable workflow checkpoints, typed tools, explicit state transitions, and provider-agnostic model calls.

                Scaling concerns:

                - Queue long-running work.
                - Separate API and worker processes.
                - Cache deterministic retrieval and tool outputs.
                - Budget model calls by workflow and tenant.
                - Use local Ollama inference for privacy-sensitive or offline paths.
            """,
            "docs/security.md": """
                # Security

                - Never pass secrets into prompts.
                - Validate tool arguments with schemas.
                - Treat retrieved content as untrusted.
                - Require approval for irreversible actions.
                - Store audit logs for model calls and tool calls.
            """,
            "docs/observability.md": """
                # Observability

                Capture traces for workflow nodes, provider calls, tool calls, retrieval, memory writes, retries, and approvals. Emit metrics for latency, token usage, cost, error rate, and evaluation scores.
            """,
            "diagrams/architecture.mmd": f"flowchart TB\n  User --> Agent[{project}]\n  Agent --> Router[Provider Router]\n  Router --> Ollama[Ollama]\n  Router --> Cloud[Cloud LLM]\n  Agent --> State[(State)]\n  Agent --> Tools[Tools]\n  Agent --> Obs[Observability]\n",
        }
        for rel, content in files.items():
            write(f"{base}/{rel}", content)


def generate_storage() -> None:
    for slug, name, summary in STORAGE:
        write(
            f"storage-patterns/{slug}/README.md",
            f"""
            # {name}

            {summary}

            ## Why Agents Need It

            Agents need this storage layer to preserve context, coordinate workflows, support retrieval, and make behavior auditable across model calls.

            ## Architecture

            ```mermaid
            flowchart LR
                Agent[Agent Runtime] --> MemoryAPI[Memory API]
                MemoryAPI --> Store[{name}]
                Store --> Eval[Quality Evaluation]
                Store --> Obs[Telemetry]
            ```

            ## Tradeoffs

            Consider latency, consistency, operational cost, data lifecycle, privacy, backup strategy, and query complexity.

            ## Production Scaling

            Add indexes, quotas, retention policies, backups, schema migrations, monitoring, and load tests before production use.

            ## Implementation Example

            See `examples/example.py`.
            """,
        )
        write(
            f"storage-patterns/{slug}/examples/example.py",
            f"""
            def describe() -> dict[str, str]:
                return {{
                    "storage": "{name}",
                    "purpose": "{summary}",
                    "status": "reference placeholder",
                }}


            if __name__ == "__main__":
                print(describe())
            """,
        )


def generate_misc() -> None:
    for path, content in ROOT_FILES.items():
        write(path, content)
    for path, content in SHARED_FILES.items():
        write(path, content)
    for path, content in DOCS.items():
        write(path, content)

    write("orchestration/README.md", "# Orchestration\n\nWorkflow orchestration covers graph execution, event-driven agents, checkpointing, retries, and human approval gates.\n")
    write("orchestration/workflow-state.md", "# Workflow State\n\nRepresent state as typed, versioned, replayable data. Avoid hidden state in prompts.\n")
    write("orchestration/checkpointing.md", "# Checkpointing\n\nCheckpoint before and after model calls, tool calls, approvals, and external side effects.\n")
    write("orchestration/event-driven.md", "# Event-Driven Agents\n\nUse queues, event logs, idempotency keys, and replay tools for asynchronous agent systems.\n")
    write("benchmarks/run_latency.py", """
        from __future__ import annotations

        import argparse
        import asyncio
        import sys
        import time
        from pathlib import Path

        ROOT = Path(__file__).resolve().parents[1]
        if str(ROOT) not in sys.path:
            sys.path.insert(0, str(ROOT))

        from shared.llm import ChatMessage, ChatRequest, build_default_router


        async def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--provider", default=None)
            parser.add_argument("--model", default=None)
            args = parser.parse_args()
            router = build_default_router()
            start = time.perf_counter()
            response = await router.chat(
                ChatRequest(
                    messages=[ChatMessage(role="user", content="Return a concise benchmark response.")],
                    model=args.model,
                ),
                provider=args.provider,
            )
            print({
                "provider": response.provider,
                "model": response.model,
                "latency_seconds": round(time.perf_counter() - start, 4),
                "usage": response.usage,
            })


        if __name__ == "__main__":
            asyncio.run(main())
    """)
    write("benchmarks/run_retrieval_quality.py", """
        from __future__ import annotations

        import argparse


        def main() -> None:
            parser = argparse.ArgumentParser()
            parser.add_argument("--dataset", required=True)
            args = parser.parse_args()
            print({"dataset": args.dataset, "metric": "nDCG@5", "status": "template"})


        if __name__ == "__main__":
            main()
    """)
    write("comparisons/pattern-matrix.md", """
        # Pattern Comparison Matrix

        | Pattern | Strength | Cost | Failure Risk |
        | --- | --- | --- | --- |
        | ReAct | Simple tool reasoning | Low-medium | Looping, weak planning |
        | Planner-Executor | Better decomposition | Medium | Bad plans cascade |
        | Reflection | Quality improvement | Medium-high | Self-confirming critique |
        | Tree of Thoughts | Search quality | High | Branch explosion |
        | RAG | Grounded answers | Medium | Retrieval misses |
        | Multi-Agent | Specialization | High | Coordination overhead |
    """)
    write("comparisons/provider-matrix.md", """
        # Provider Comparison Matrix

        | Provider | Strength | Tradeoff | Best Use |
        | --- | --- | --- | --- |
        | Ollama | Local-first, private, offline | Hardware-bound | Development, privacy, edge |
        | OpenAI | Strong general models | Cloud dependency | Production quality workloads |
        | Anthropic | Strong long-context reasoning | Cloud dependency | Review, analysis, safety-sensitive drafting |
        | OpenAI-compatible | Flexible serving | Varies by backend | vLLM, hosted OSS, internal gateways |
        | GGUF / llama.cpp | Portable local inference | Integration work | Embedded and constrained deployments |
    """)
    write("diagrams/provider-abstraction.mmd", "flowchart LR\n  Agent --> Router[Model Router]\n  Router --> OpenAI\n  Router --> Anthropic\n  Router --> Ollama\n  Router --> Compatible[OpenAI-Compatible]\n")
    write("diagrams/local-ai-deployment.mmd", "flowchart TB\n  App[Agent App] --> Ollama[Ollama]\n  Ollama --> Models[(Local Models)]\n  App --> Cache[(Redis / Semantic Cache)]\n")
    write("diagrams/observability.mmd", "flowchart LR\n  Agent --> OTEL[OpenTelemetry]\n  OTEL --> Prometheus\n  OTEL --> Grafana\n  Agent --> Audit[(Audit Log)]\n")
    write("papers/README.md", "# Papers\n\nAnnotated reading list for agent architectures, tool use, RAG, memory, orchestration, and evaluation.\n")
    write("datasets/README.md", "# Datasets\n\nStore dataset manifests, sample corpora, golden tasks, and benchmark metadata here.\n")
    write("datasets/sample_corpus.jsonl", '{"id":"doc-1","text":"Agent systems require observability, memory, tool safety, and evaluation."}\n')
    write("notebooks/README.md", "# Notebooks\n\nExperiment notebooks for retrieval, memory, local model benchmarks, and evaluation analysis.\n")
    write("infra/prometheus.yml", """
        global:
          scrape_interval: 15s
        scrape_configs:
          - job_name: agent-services
            static_configs:
              - targets: ["host.docker.internal:8000"]
    """)


def main() -> None:
    generate_misc()
    generate_patterns()
    generate_projects()
    generate_storage()


if __name__ == "__main__":
    main()
