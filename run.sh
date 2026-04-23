#!/bin/bash
# run.sh - Run the Glassdoor RAG application

set -e

echo "🚀 Starting Glassdoor RAG Application"

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "❌ Ollama is not running!"
    echo "Please start Ollama first:"
    echo "   macOS/Linux: ollama serve"
    echo "   Or download from https://ollama.com"
    exit 1
fi

# Check if model is pulled
if ! ollama list | grep -q "llama3.2"; then
    echo "📥 Pulling llama3.2 model (first time, ~4GB)..."
    ollama pull llama3.2
fi

# Check if data exists
if [ ! -f "data/glassdoor-companies-reviews.csv" ]; then
    echo "⚠️ Warning: No CSV data found in ./data/"
    echo "Please download the dataset from:"
    echo "https://github.com/luminati-io/Glassdoor-dataset-samples"
fi

# Run the application
echo "✅ Running Glassdoor RAG..."
uv run python run_analysis.py
