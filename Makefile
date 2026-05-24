.PHONY: install test lint ollama benchmark

install:
	pip install -e ".[dev,cloud,storage,observability]"

test:
	pytest

lint:
	ruff check .

ollama:
	ollama serve

benchmark:
	python benchmarks/run_latency.py --provider $${MODEL_PROVIDER:-mock} --model $${OLLAMA_MODEL:-mock-model}
