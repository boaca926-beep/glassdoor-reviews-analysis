#!/bin/bash
# deploy.sh - Docker deployment (includes Ollama in container)

set -e

echo "🐳 Deploying Glassdoor RAG with Docker"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Build and start containers
echo "📦 Building Docker images..."
docker-compose build

echo "🐳 Starting containers..."
docker-compose up -d

# Wait for Ollama to be ready
echo "⏳ Waiting for Ollama to start..."
sleep 10

# Pull model inside container (still downloads ~4GB)
echo "📥 Pulling llama3.2 model inside container (this may take several minutes)..."
docker-compose exec ollama ollama pull llama3.2 || true

echo ""
echo "✅ Docker deployment complete!"
echo ""
echo "Commands:"
echo "  docker-compose exec app bash     - Enter the container"
echo "  docker-compose exec app python main.py - Run the app"
echo "  docker-compose logs -f           - View logs"
echo "  docker-compose down              - Stop everything"
