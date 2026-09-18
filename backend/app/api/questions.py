"""API endpoints for question and dimension metadata."""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from app.data.questions import QUESTIONS, DIMENSIONS, QUESTION_LOOKUP

router = APIRouter(tags=["questions"])


@router.get("/questions", response_model=List[Dict[str, Any]])
def get_all_questions():
    """
    Return all 40 questions formatted for the frontend client.
    Option weights are stripped to preserve testing integrity.
    """
    client_questions = []
    for q in QUESTIONS:
        client_questions.append({
            "id": q["id"],
            "dimension": q["dimension"],
            "dimension_name": q["dimension_name"],
            "question": q["question"],
            "options": q["options"],
        })
    return client_questions


@router.get("/questions/{question_id}", response_model=Dict[str, Any])
def get_single_question(question_id: int):
    """Retrieve a single question by its numerical ID (1 - 40)."""
    q = QUESTION_LOOKUP.get(question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return {
        "id": q["id"],
        "dimension": q["dimension"],
        "dimension_name": q["dimension_name"],
        "question": q["question"],
        "options": q["options"],
    }


@router.get("/dimensions", response_model=Dict[str, Dict[str, Any]])
def get_dimensions():
    """Return all 10 behavioral dimensions with definitions, weights, and icons."""
    return DIMENSIONS
