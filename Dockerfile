# Dockerfile
FROM python:3.12-slim

# Install system dependencies for sentence-transformers
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Set Python environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    OLLAMA_HOST=http://ollama:11434

# Copy requirements first (better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir \
    langchain-ollama \
    langchain-core \
    langchain-community \
    sentence-transformers \
    pandas \
    chromadb

# Copy your application code
COPY main.py .
COPY vector.py .
COPY requirements.txt .

# Create directories for persistent data
RUN mkdir -p /app/data /app/chroma_db

# Default command - runs your main.py
CMD ["python", "main.py"]
