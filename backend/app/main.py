import os
import sys
from contextlib import asynccontextmanager
from pathlib import Path
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse

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

PUBLIC_DIR = ROOT_DIR / "public"
FRONTEND_DIR = ROOT_DIR / "frontend"
STATIC_DIR = PUBLIC_DIR if PUBLIC_DIR.exists() else FRONTEND_DIR


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup and shutdown events."""
    print("Initializing Know Your Partner AI database...", flush=True)
    try:
        init_db()
    except Exception as e:
        print(f"[Warning] DB init error: {e}", flush=True)
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

# Vercel Path Normalization Middleware
class VercelPathFixMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Vercel passes x-matched-path when rewrites are used
        matched_path = request.headers.get("x-matched-path")
        current_path = request.scope.get("path", "")
        if matched_path and (current_path == "/api/index.py" or current_path.endswith("index.py")):
            request.scope["path"] = matched_path
        return await call_next(request)

app.add_middleware(VercelPathFixMiddleware)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers with BOTH /api prefix AND empty prefix
app.include_router(questions_router, prefix="/api")
app.include_router(questions_router, prefix="")
app.include_router(analysis_router, prefix="/api")
app.include_router(analysis_router, prefix="")
app.include_router(results_router, prefix="/api")
app.include_router(results_router, prefix="")


@app.get("/api/health")
@app.get("/health")
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


# Direct Page Handlers (guarantees HTML serving even if static rewrites miss)
def _serve_page(filename: str):
    file_path = STATIC_DIR / filename
    if file_path.exists():
        return FileResponse(str(file_path))
    return JSONResponse(status_code=404, content={"detail": f"{filename} not found"})


@app.get("/")
@app.get("/index.html")
def root_index():
    return _serve_page("index.html")


@app.get("/quiz")
@app.get("/quiz.html")
def root_quiz():
    return _serve_page("quiz.html")


@app.get("/analysis")
@app.get("/analysis.html")
def root_analysis():
    return _serve_page("analysis.html")


@app.get("/result")
@app.get("/result.html")
def root_result():
    return _serve_page("result.html")


# Mount static assets (CSS, JS)
if (STATIC_DIR / "css").exists():
    app.mount("/css", StaticFiles(directory=str(STATIC_DIR / "css")), name="css")
if (STATIC_DIR / "js").exists():
    app.mount("/js", StaticFiles(directory=str(STATIC_DIR / "js")), name="js")
