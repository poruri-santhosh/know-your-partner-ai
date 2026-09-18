import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path

# Ensure backend and root are in sys.path from any working directory
BACKEND_DIR = Path(__file__).resolve().parent.parent
ROOT_DIR = BACKEND_DIR.parent
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

try:
    from dotenv import load_dotenv
    load_dotenv(ROOT_DIR / ".env")
    load_dotenv(BACKEND_DIR / ".env")
except ImportError:
    pass

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.database.database import init_db
from app.ml.predict import load_compatibility_model, load_kmeans_model
from app.api.questions import router as questions_router
from app.api.analysis import router as analysis_router
from app.api.results import router as results_router

BASE_DIR = ROOT_DIR
FRONTEND_DIR = BASE_DIR / "frontend"


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    print("Initializing Know Your Partner AI database...", flush=True)
    init_db()
    print("Loading machine learning models...", flush=True)
    load_compatibility_model()
    load_kmeans_model()
    print("Startup sequence complete.", flush=True)
    yield


app = FastAPI(
    title="Know Your Partner AI",
    description="Scientific behavioral profiling, machine learning compatibility prediction, and relationship insights.",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(questions_router)
app.include_router(analysis_router)
app.include_router(results_router)


@app.get("/api/health")
def health_check():
    """Health status and service liveness check."""
    comp_model = load_compatibility_model()
    kmeans_model = load_kmeans_model()
    return {
        "status": "healthy",
        "service": "Know Your Partner AI",
        "version": "1.0.0",
        "compatibility_model_loaded": comp_model is not None,
        "kmeans_archetypes_loaded": kmeans_model is not None,
    }


# Mount frontend static directory if exists
if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")
