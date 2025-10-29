#!/bin/bash

# Local development setup script

echo "🔧 Setting up Clay Clone for local development..."

# Backend setup
echo ""
echo "📦 Setting up Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "Creating backend .env file..."
    cp .env.example .env
fi

cd ..

# Frontend setup
echo ""
echo "📦 Setting up Frontend..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing Node dependencies..."
    npm install
fi

if [ ! -f ".env.local" ]; then
    echo "Creating frontend .env.local file..."
    echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local
fi

cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env with your API keys"
echo "2. Start PostgreSQL and Redis:"
echo "   docker run -d -p 5432:5432 -e POSTGRES_USER=clay_user -e POSTGRES_PASSWORD=clay_password -e POSTGRES_DB=clay_clone postgres:15-alpine"
echo "   docker run -d -p 6379:6379 redis:7-alpine"
echo ""
echo "3. Start Backend (in terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn main:app --reload"
echo ""
echo "4. Start Celery Worker (in terminal 2):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   celery -A workers.tasks.celery_app worker --loglevel=info"
echo ""
echo "5. Start Frontend (in terminal 3):"
echo "   cd frontend"
echo "   npm run dev"
echo ""

