FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN pip install /app
WORKDIR /app/projects/event-driven-agents-slack-incident-response-bot
CMD ["python", "src/main.py", "Run the reference workflow"]
