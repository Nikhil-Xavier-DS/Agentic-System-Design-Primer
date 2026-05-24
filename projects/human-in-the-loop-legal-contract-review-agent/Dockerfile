FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install /app
WORKDIR /app/projects/human-in-the-loop-legal-contract-review-agent
CMD ["python", "src/main.py", "Run the reference workflow"]
