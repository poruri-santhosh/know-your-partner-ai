"""API endpoints for behavioral scoring, ML compatibility analysis, and profile comparison."""

from fastapi import APIRouter, HTTPException, status
from typing import Dict, Any, List

from app.database.models import QuizSubmissionRequest, CompareProfilesRequest
from app.services.partner_analysis import analyze_quiz_submission
from app.ml.predict import predict_pair_compatibility
from app.ml.compatibility import CANDIDATE_ARCHETYPES
from app.ml.preprocessing import clean_profile_vector

router = APIRouter(prefix="/api", tags=["analysis"])


@router.post("/analyze")
def submit_and_analyze(payload: QuizSubmissionRequest):
    """
    Main analysis pipeline:
    Receives user questionnaire answers, computes behavioral scores across 10 dimensions,
    classifies behavioral archetype via K-Means, synthesizes ideal partner profile,
    evaluates pairwise compatibility via trained ML regressor, ranks candidate archetypes,
    and returns rich AI narrative explanations.
    """
    try:
        result = analyze_quiz_submission(
            raw_answers=payload.answers,
            custom_partner_profile=payload.partner_profile,
        )
        return result
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis pipeline encountered an error: {str(e)}"
        )


@router.post("/compare")
def compare_profiles(payload: CompareProfilesRequest):
    """
    Compare two arbitrary behavioral profiles (0-100 scores across 10 dimensions).
    Runs pairwise feature engineering, ML compatibility prediction, and dimension breakdown.
    """
    try:
        profile_a = clean_profile_vector(payload.user_profile)
        profile_b = clean_profile_vector(payload.partner_profile)
        
        result = predict_pair_compatibility(profile_a, profile_b)
        return {
            "overall_compatibility": result["overall_compatibility"],
            "model_used": result["model_used"],
            "is_ml": result["is_ml"],
            "dimension_breakdown": result["dimension_breakdown"],
            "features": result["features"],
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Profile comparison failed: {str(e)}"
        )


@router.get("/candidates", response_model=List[Dict[str, Any]])
def get_candidate_archetypes():
    """Retrieve pre-configured partner candidate archetypes for exploration."""
    return CANDIDATE_ARCHETYPES
