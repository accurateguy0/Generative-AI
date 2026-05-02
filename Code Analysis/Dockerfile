WORKDIR /app
RUN pip install --no-cache-dir \
    langchain \
    langchain-openai \
    llama-index \
    bandit \
    ruff \
    openai
COPY Workflow.py /app/Workflow.py
CMD ["python", "/app/Workflow.py"]
