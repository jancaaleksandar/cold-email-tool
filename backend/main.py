from contextlib import asynccontextmanager

from db.database import Base, engine
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import enrich, leads


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed


app = FastAPI(
    title="Clay Clone API", description="Lead enrichment and management API", version="1.0.0", lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/api/leads", tags=["leads"])
app.include_router(enrich.router, prefix="/api/enrich", tags=["enrich"])


@app.get("/")
async def root():
    return {"message": "Clay Clone API is running", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
