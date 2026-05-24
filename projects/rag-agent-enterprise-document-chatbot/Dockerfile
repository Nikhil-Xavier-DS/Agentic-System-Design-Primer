FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install /app
WORKDIR /app/projects/rag-agent-enterprise-document-chatbot
CMD ["python", "src/main.py", "Run the reference workflow"]
