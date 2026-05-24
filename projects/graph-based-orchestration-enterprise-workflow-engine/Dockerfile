FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install /app
WORKDIR /app/projects/graph-based-orchestration-enterprise-workflow-engine
CMD ["python", "src/main.py", "Run the reference workflow"]
