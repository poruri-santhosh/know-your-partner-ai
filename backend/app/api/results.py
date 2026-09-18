"""API endpoints for result retrieval and model inspection."""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any

from app.database.database import get_submission
from app.ml.predict import load_compatibility_model, load_kmeans_model
from app.ml.feature_engineering import FEATURE_NAMES

router = APIRouter(prefix="/api", tags=["results"])


@router.get("/results/{submission_id}")
def get_analysis_result(submission_id: str):
    """Retrieve saved questionnaire analysis result by submission ID."""
    data = get_submission(submission_id)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No submission found with ID: {submission_id}"
        )
    return data["result"]


@router.get("/model-info")
def get_model_info() -> Dict[str, Any]:
    """Retrieve current ML model metadata, architecture comparison, and metrics."""
    comp_model = load_compatibility_model()
    kmeans_model = load_kmeans_model()
    
    return {
        "active_model": comp_model.get("model_name", "Weighted Mathematical Formula") if comp_model else "Not Loaded",
        "features_count": len(FEATURE_NAMES),
        "features": FEATURE_NAMES,
        "metrics": comp_model.get("metrics", {}) if comp_model else {},
        "benchmark_comparison": comp_model.get("all_metrics", {}) if comp_model else {},
        "clustering_archetypes": kmeans_model.get("archetype_labels", {}) if kmeans_model else {},
    }


@router.get("/database/stats")
def get_database_stats() -> Dict[str, Any]:
    """Inspect current SQL database records, row counts, and recent activity."""
    from app.database.database import SessionLocal, DATABASE_URL
    from app.database.models import SubmissionRecord, AnswerRecord
    
    db = SessionLocal()
    try:
        total_sub = db.query(SubmissionRecord).count()
        total_ans = db.query(AnswerRecord).count()
        
        recent = db.query(SubmissionRecord).order_by(SubmissionRecord.created_at.desc()).limit(10).all()
        recent_list = [
            {
                "submission_id": r.id,
                "created_at": str(r.created_at),
                "archetype": r.archetype_name,
                "badge": r.archetype_badge,
                "answered_count": r.answered_count,
            }
            for r in recent
        ]
        
        return {
            "database_url": DATABASE_URL.split("@")[-1] if "@" in DATABASE_URL else DATABASE_URL,
            "total_submissions": total_sub,
            "total_answers_logged": total_ans,
            "recent_submissions": recent_list,
        }
    finally:
        db.close()
