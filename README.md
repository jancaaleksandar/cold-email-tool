# Clay Clone - Lead Enrichment Platform

A powerful lead enrichment and management platform inspired by Clay. Built with Next.js, FastAPI, PostgreSQL, Redis, and Celery.

## 🎯 Features

- **Lead Management**: Upload, view, and manage leads via CSV or manual entry
- **Multi-Source Enrichment**: 
  - Apollo.io integration for B2B data
  - Email validation and discovery
  - AI-powered insights using OpenAI
  - Web scraping for company information
- **Async Processing**: Background job processing with Celery and Redis
- **Modern UI**: Beautiful, responsive interface built with Next.js and Tailwind CSS
- **Powerful Tables**: Advanced table functionality with TanStack Table

## 🏗️ Architecture

| Layer           | Stack                                  | Purpose                       |
| --------------- | -------------------------------------- | ----------------------------- |
| **Frontend**    | Next.js + Tailwind + TanStack Table    | UI for table & actions        |
| **Backend API** | Python (FastAPI)                       | Handle data, enrichment logic |
| **Database**    | PostgreSQL                             | Store leads & results         |
| **Queue**       | Celery + Redis                         | Handle async enrichment       |
| **AI & APIs**   | OpenAI + Apollo + Email validation API | Actual enrichment sources     |

## 📁 Project Structure

```
clay_clone/
│
├── frontend/              # Next.js app
│   ├── app/              # App router pages
│   ├── components/       # React components
│   ├── lib/              # API client and utilities
│   └── package.json
│
├── backend/              # FastAPI app
│   ├── main.py          # FastAPI application entry
│   ├── routes/          # API routes
│   │   ├── leads.py     # Lead CRUD operations
│   │   └── enrich.py    # Enrichment endpoints
│   ├── services/        # Business logic
│   │   ├── apollo_service.py
│   │   ├── email_validation.py
│   │   ├── ai_enrichment.py
│   │   └── scraper.py
│   ├── workers/         # Celery workers
│   │   └── tasks.py
│   ├── db/              # Database models
│   │   ├── models.py
│   │   └── database.py
│   └── requirements.txt
│
├── docker-compose.yml    # Docker orchestration
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (recommended)
- PostgreSQL 15+ (if not using Docker)
- Redis (if not using Docker)

### Option 1: Docker (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo>
cd clay_clone
```

2. **Set up environment variables**

Create `.env` file in the root directory:
```bash
# API Keys
OPENAI_API_KEY=your_openai_api_key
APOLLO_API_KEY=your_apollo_api_key
EMAIL_VALIDATION_API_KEY=your_email_validation_api_key
EMAIL_VALIDATION_PROVIDER=hunter
```

3. **Start all services**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL on port 5432
- Redis on port 6379
- Backend API on port 8000
- Celery worker
- Frontend on port 3000

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Option 2: Local Development

#### Backend Setup

1. **Create virtual environment**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create `backend/.env`:
```bash
DATABASE_URL=postgresql://clay_user:clay_password@localhost:5432/clay_clone
REDIS_URL=redis://localhost:6379/0
OPENAI_API_KEY=your_openai_api_key
APOLLO_API_KEY=your_apollo_api_key
EMAIL_VALIDATION_API_KEY=your_email_validation_api_key
EMAIL_VALIDATION_PROVIDER=hunter
ENVIRONMENT=development
DEBUG=true
```

4. **Start PostgreSQL and Redis**
```bash
# Using Docker for just DB and Redis
docker run -d -p 5432:5432 -e POSTGRES_USER=clay_user -e POSTGRES_PASSWORD=clay_password -e POSTGRES_DB=clay_clone postgres:15-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

5. **Run the backend**
```bash
uvicorn main:app --reload
```

6. **Start Celery worker** (in a new terminal)
```bash
cd backend
source venv/bin/activate
celery -A workers.tasks.celery_app worker --loglevel=info
```

#### Frontend Setup

1. **Install dependencies**
```bash
cd frontend
npm install
```

2. **Set up environment variables**

Create `frontend/.env.local`:
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

3. **Run the development server**
```bash
npm run dev
```

4. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📋 Usage

### 1. Upload Leads

- Click "Upload Leads" button
- Drop or select a CSV file
- CSV should contain columns like: `first_name`, `last_name`, `company`, `title`, `website`, `linkedin_url`, `email`, `phone`

Example CSV:
```csv
first_name,last_name,company,title,website,email
John,Doe,Acme Corp,CEO,https://acme.com,john@acme.com
Jane,Smith,Tech Inc,CTO,https://techinc.com,jane@techinc.com
```

### 2. Enrich Leads

- Select leads from the table (checkbox)
- Click "Enrich Selected"
- Choose enrichment types (automatically runs all: Apollo, Email, AI, Scraper)
- Monitor status in the table

### 3. View Enriched Data

- Enriched data appears in the table
- Status indicator shows enrichment progress
- Click on a lead to see detailed enriched information

## 🔑 API Keys Setup

### OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Add to `.env` as `OPENAI_API_KEY`

### Apollo.io API Key
1. Sign up at https://apollo.io
2. Go to Settings → API
3. Generate an API key
4. Add to `.env` as `APOLLO_API_KEY`

### Email Validation (Hunter.io)
1. Sign up at https://hunter.io
2. Get your API key from dashboard
3. Add to `.env` as `EMAIL_VALIDATION_API_KEY`

## 🛠️ Development

### Backend API Endpoints

#### Leads
- `GET /api/leads/` - Get all leads
- `POST /api/leads/` - Create a single lead
- `POST /api/leads/bulk` - Create multiple leads
- `POST /api/leads/upload-csv` - Upload CSV
- `GET /api/leads/{id}` - Get specific lead
- `PUT /api/leads/{id}` - Update lead
- `DELETE /api/leads/{id}` - Delete lead

#### Enrichment
- `POST /api/enrich/` - Trigger enrichment
- `GET /api/enrich/status/{lead_id}` - Get enrichment status
- `POST /api/enrich/retry/{lead_id}` - Retry failed enrichments

### Database Schema

**Leads Table**
- id, first_name, last_name, company, title
- website, linkedin_url, email, phone
- enrichment_status, enriched_data (JSON)
- created_at, updated_at

**EnrichmentTasks Table**
- id, lead_id, task_type, status
- result (JSON), error_message
- celery_task_id, created_at, completed_at

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📦 Deployment

### Deploy with Docker

```bash
# Build images
docker-compose build

# Start in production mode
docker-compose up -d

# View logs
docker-compose logs -f
```

### Deploy to Cloud

**Backend (FastAPI)**
- Heroku, Railway, Render, or AWS ECS
- Set environment variables in platform settings
- Use `uvicorn main:app --host 0.0.0.0 --port $PORT`

**Frontend (Next.js)**
- Vercel (recommended), Netlify, or Cloudflare Pages
- Set `NEXT_PUBLIC_API_URL` to your backend URL
- Deploy with `npm run build && npm start`

**Database**
- Supabase (free PostgreSQL)
- Neon (serverless PostgreSQL)
- ElephantSQL

**Redis**
- Redis Cloud (free tier)
- Upstash (serverless Redis)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- Inspired by [Clay](https://clay.com)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- UI powered by [Next.js](https://nextjs.org/) and [Tailwind CSS](https://tailwindcss.com/)
- Tables by [TanStack Table](https://tanstack.com/table)

## 📧 Support

For support, email your-email@example.com or open an issue on GitHub.

---

Made with ❤️ by Your Team
