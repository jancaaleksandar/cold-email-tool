#!/bin/bash

# Start script for Clay Clone

echo "🚀 Starting Clay Clone..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your API keys before continuing."
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "📦 Starting services with Docker Compose..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "✅ Clay Clone is running!"
echo ""
echo "📍 Access points:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📊 View logs:"
echo "   All logs:     docker-compose logs -f"
echo "   Backend:      docker-compose logs -f backend"
echo "   Frontend:     docker-compose logs -f frontend"
echo "   Celery:       docker-compose logs -f celery_worker"
echo ""
echo "🛑 Stop services:"
echo "   docker-compose down"
echo ""

