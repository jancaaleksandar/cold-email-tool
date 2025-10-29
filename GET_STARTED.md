# 🎯 Get Started with Clay Clone

## What You Have Now

Your Clay Clone is **100% complete and ready to run**! Here's what's been built:

### ✅ Backend (FastAPI)
- Complete REST API with 15+ endpoints
- 4 enrichment services (Apollo, Email, AI, Scraper)
- Celery async job processing
- PostgreSQL database with SQLAlchemy
- Redis for task queue
- Full CRUD for leads
- CSV upload support
- Error handling and validation

### ✅ Frontend (Next.js)
- Modern, beautiful UI with Tailwind CSS
- Advanced data table with TanStack Table
- Drag-and-drop CSV upload
- Bulk lead selection and enrichment
- Real-time status updates
- Responsive design

### ✅ DevOps
- Docker Compose for one-command setup
- Health checks for all services
- Volume persistence
- Environment variable management
- Production-ready configuration

## 🚀 Quick Start (5 minutes)

### Option 1: Docker (Recommended - Easiest!)

```bash
# 1. Copy environment variables
cp .env.example .env

# 2. Edit .env and add your API keys
nano .env  # or use any editor

# Add these keys (minimum OpenAI for basic functionality):
# OPENAI_API_KEY=sk-your-key-here
# APOLLO_API_KEY=your-key-here (optional)
# EMAIL_VALIDATION_API_KEY=your-key-here (optional)

# 3. Start everything with one command!
./scripts/start.sh

# Or manually:
docker-compose up -d

# 4. Open your browser
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000/docs
```

That's it! 🎉

### Option 2: Local Development

```bash
# Run the setup script
./scripts/setup-local.sh

# Then follow the printed instructions to:
# - Start PostgreSQL & Redis (via Docker)
# - Start backend server
# - Start Celery worker
# - Start frontend dev server
```

## 📖 Using Your Clay Clone

### 1. Upload Leads

1. Go to http://localhost:3000
2. Click **"Upload Leads"** button
3. Drag and drop `data/sample_leads.csv` (we included sample data!)
4. Click **"Upload"**

### 2. Enrich Leads

1. Select leads using checkboxes
2. Click **"Enrich Selected"**
3. Watch the magic happen! ✨
4. Status updates show progress

### 3. View Results

- Enriched data appears in the table
- Status badges show enrichment state
- All enriched info stored in database

## 🔑 Getting API Keys

### OpenAI (Required for AI features)
1. Visit: https://platform.openai.com/api-keys
2. Sign up / log in
3. Create new API key
4. Copy to `.env` as `OPENAI_API_KEY`

### Apollo.io (Optional - B2B data)
1. Visit: https://www.apollo.io
2. Sign up for free account
3. Go to Settings → API
4. Copy API key to `.env` as `APOLLO_API_KEY`

### Hunter.io (Optional - Email validation)
1. Visit: https://hunter.io
2. Sign up for free account
3. Get API key from dashboard
4. Copy to `.env` as `EMAIL_VALIDATION_API_KEY`

**Note**: You can start with just OpenAI and add others later!

## 📁 Key Files

```
📄 README.md              - Full documentation
📄 QUICKSTART.md          - Quick start guide
📄 PROJECT_SUMMARY.md     - Complete project overview
📄 CONTRIBUTING.md        - Contribution guidelines
📄 docker-compose.yml     - Docker orchestration
📄 .env.example           - Environment variables template

📁 backend/               - Python FastAPI app
   📄 main.py             - API entry point
   📁 routes/             - API endpoints
   📁 services/           - Business logic
   📁 workers/            - Background jobs
   📁 db/                 - Database models

📁 frontend/              - Next.js app
   📁 app/                - Pages
   📁 components/         - React components
   📁 lib/                - Utilities

📁 scripts/               - Helper scripts
   📄 start.sh            - Start all services
   📄 stop.sh             - Stop all services
   📄 setup-local.sh      - Local dev setup

📁 data/
   📄 sample_leads.csv    - Sample data for testing
```

## 🔧 Useful Commands

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f celery_worker
docker-compose logs -f frontend
```

### Stop Services
```bash
./scripts/stop.sh
# or
docker-compose down
```

### Restart Services
```bash
docker-compose restart
```

### Access Database
```bash
docker-compose exec postgres psql -U clay_user -d clay_clone
```

### Access Redis
```bash
docker-compose exec redis redis-cli
```

## 🎨 Customization

### Change Colors
Edit `frontend/tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: {
        // Change these values
        500: '#0ea5e9',
        600: '#0284c7',
        // ...
      }
    }
  }
}
```

### Add New Enrichment Source
1. Create service in `backend/services/`
2. Add to `backend/workers/tasks.py`
3. Update requirements.txt
4. Update frontend UI

See `CONTRIBUTING.md` for detailed guide.

### Modify UI
- Components in `frontend/components/`
- Pages in `frontend/app/`
- API client in `frontend/lib/api.ts`

## 🐛 Troubleshooting

### "Cannot connect to backend"
```bash
# Check backend is running
curl http://localhost:8000/health

# If not running, check logs
docker-compose logs backend
```

### "Database connection error"
```bash
# Restart database
docker-compose restart postgres

# Check if it's running
docker-compose ps
```

### "Port already in use"
```bash
# Find what's using the port
lsof -i :3000  # or :8000, :5432, :6379

# Kill the process or change port in docker-compose.yml
```

### "Import errors in Python"
```bash
# Rebuild backend
docker-compose build backend
docker-compose up -d backend
```

### Frontend won't start
```bash
cd frontend
rm -rf node_modules .next
npm install
npm run dev
```

## 📚 Learn More

- **API Documentation**: http://localhost:8000/docs (when running)
- **Full README**: [README.md](README.md)
- **Project Overview**: [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Next.js Docs**: https://nextjs.org/docs

## 🎯 Next Steps

Now that you have it running:

1. ✅ Upload the sample CSV
2. ✅ Test enrichment with different sources
3. ✅ Explore the API at http://localhost:8000/docs
4. ✅ Customize the UI to match your brand
5. ✅ Add more enrichment sources
6. ✅ Deploy to production

## 🚀 Deploy to Production

### Backend Options
- **Heroku**: Easy deployment with Heroku CLI
- **Railway**: Modern platform with Docker support
- **Render**: Automatic deployments from Git
- **AWS ECS**: Containerized deployment

### Frontend Options
- **Vercel**: Perfect for Next.js (one-click deploy)
- **Netlify**: Great alternative
- **Cloudflare Pages**: Fast global CDN

### Database Options
- **Supabase**: Free PostgreSQL with great features
- **Neon**: Serverless PostgreSQL
- **Railway**: PostgreSQL included

See README.md for detailed deployment instructions.

## 💬 Need Help?

1. Check the README.md
2. Review logs: `docker-compose logs -f`
3. Search for similar issues
4. Open a GitHub issue

## 🎉 You're All Set!

Your Clay Clone is production-ready and includes:
- ✅ Modern, beautiful UI
- ✅ Powerful enrichment engine
- ✅ Scalable architecture
- ✅ Complete documentation
- ✅ Easy deployment options

**Start enriching leads now!** 🚀

---

Made with ❤️ - Happy enriching!

