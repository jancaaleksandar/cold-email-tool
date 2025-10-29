# 🚀 Quick Start Guide

Get your Clay Clone up and running in 5 minutes!

## Prerequisites

- Docker & Docker Compose installed
- API keys for:
  - OpenAI (required for AI enrichment)
  - Apollo.io (optional, for B2B data)
  - Hunter.io (optional, for email validation)

## Step 1: Clone and Setup

```bash
# Clone the repository
cd clay_clone

# Create environment file
cp .env.example .env
```

## Step 2: Add Your API Keys

Edit `.env` file:

```bash
OPENAI_API_KEY=sk-your-openai-key-here
APOLLO_API_KEY=your-apollo-key-here  # Optional
EMAIL_VALIDATION_API_KEY=your-hunter-key-here  # Optional
```

## Step 3: Start Everything

```bash
# Make scripts executable
chmod +x scripts/*.sh

# Start all services
./scripts/start.sh

# Or manually with docker-compose
docker-compose up -d
```

## Step 4: Access Your Application

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## Step 5: Upload Sample Data

1. Go to http://localhost:3000
2. Click "Upload Leads"
3. Use the sample CSV file in `data/sample_leads.csv`
4. Select leads and click "Enrich Selected"

## 🎉 That's It!

Your Clay Clone is now running!

## What's Next?

1. **Explore the API**: Visit http://localhost:8000/docs
2. **Customize enrichment**: Edit `backend/services/*.py`
3. **Modify the UI**: Edit files in `frontend/components/`
4. **Add new features**: Check out the README.md for detailed docs

## Common Issues

### Services won't start
```bash
# Check Docker is running
docker info

# Check logs
docker-compose logs -f
```

### Database connection errors
```bash
# Restart services
docker-compose restart

# Or recreate everything
docker-compose down -v
docker-compose up -d
```

### Frontend can't connect to backend
- Make sure backend is running: http://localhost:8000/health
- Check `frontend/.env.local` has correct API URL

## Stop Services

```bash
# Stop all services
./scripts/stop.sh

# Or manually
docker-compose down

# To remove all data
docker-compose down -v
```

## Local Development (Without Docker)

If you prefer to run services locally:

```bash
./scripts/setup-local.sh
```

Then follow the instructions printed by the script.

## Need Help?

- Check the main [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Review logs: `docker-compose logs -f`

---

Happy enriching! 🎯

