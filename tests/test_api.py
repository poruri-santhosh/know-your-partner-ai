"""Integration tests for FastAPI endpoints."""

import pytest
import sys
from pathlib import Path
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.main import app

client = TestClient(app)


def test_health_check():
    """Verify health check endpoint returns 200 and model status."""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "compatibility_model_loaded" in data


def test_get_questions():
    """Verify GET /api/questions returns all 40 questions."""
    response = client.get("/api/questions")
    assert response.status_code == 200
    questions = response.json()
    assert len(questions) == 40
    assert questions[0]["id"] == 1
    assert len(questions[0]["options"]) == 4


def test_get_dimensions():
    """Verify GET /api/dimensions returns 10 dimensions with metadata."""
    response = client.get("/api/dimensions")
    assert response.status_code == 200
    dims = response.json()
    assert len(dims) == 10
    assert "communication" in dims
    assert "weight" in dims["communication"]


def test_submit_and_analyze():
    """Verify POST /api/analyze executes full pipeline with realistic responses."""
    # Build answers for 40 questions
    answers = {str(i): "A" if i % 2 == 1 else "B" for i in range(1, 41)}
    
    response = client.post("/api/analyze", json={"answers": answers})
    assert response.status_code == 200
    res = response.json()
    
    assert "submission_id" in res
    assert "user_profile" in res
    assert len(res["user_profile"]) == 10
    assert "archetype" in res
    assert "overall_compatibility" in res
    assert "candidate_matches" in res
    assert len(res["candidate_matches"]) > 0
    assert "ai_narrative" in res
    assert "summary" in res["ai_narrative"]


def test_compare_profiles_endpoint():
    """Verify POST /api/compare evaluates two profile vectors."""
    payload = {
        "user_profile": {
            "communication": 85,
            "emotional_openness": 70,
            "social_nature": 60,
            "independence": 75,
            "family_orientation": 90,
            "financial_attitude": 85,
            "career_orientation": 80,
            "adventure": 65,
            "conflict_handling": 85,
            "lifestyle_preference": 75,
        },
        "partner_profile": {
            "communication": 80,
            "emotional_openness": 75,
            "social_nature": 65,
            "independence": 70,
            "family_orientation": 85,
            "financial_attitude": 80,
            "career_orientation": 85,
            "adventure": 60,
            "conflict_handling": 80,
            "lifestyle_preference": 80,
        },
    }
    response = client.post("/api/compare", json=payload)
    assert response.status_code == 200
    res = response.json()
    assert "overall_compatibility" in res
    assert res["overall_compatibility"] > 50.0


def test_get_candidates():
    """Verify GET /api/candidates returns candidate archetypes."""
    response = client.get("/api/candidates")
    assert response.status_code == 200
    candidates = response.json()
    assert len(candidates) >= 5
