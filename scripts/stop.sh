#!/bin/bash

# Stop script for Clay Clone

echo "🛑 Stopping Clay Clone services..."

docker-compose down

echo "✅ All services stopped."
echo ""
echo "💡 To remove all data (database, Redis):"
echo "   docker-compose down -v"
echo ""

