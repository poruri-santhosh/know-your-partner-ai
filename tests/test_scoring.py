"""Unit tests for questionnaire scoring and normalization."""

import pytest
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.data.questions import QUESTIONS, DIMENSIONS, MIN_POSSIBLE_SCORES, MAX_POSSIBLE_SCORES
from app.ml.scoring import calculate_raw_scores, normalize_scores, calculate_behavioral_profile


def test_questionnaire_definition_integrity():
    """Verify that all 40 questions are defined across the 10 dimensions with 4 options each."""
    assert len(QUESTIONS) == 40
    assert len(DIMENSIONS) == 10
    
    # Check that each question has ID 1 to 40
    q_ids = [q["id"] for q in QUESTIONS]
    assert q_ids == list(range(1, 41))
    
    # Check that each question has options A, B, C, D
    for q in QUESTIONS:
        option_ids = [opt["id"] for opt in q["options"]]
        assert option_ids == ["A", "B", "C", "D"]
        assert "scores" in q
        assert set(q["scores"].keys()) == {"A", "B", "C", "D"}


def test_scoring_all_high_options():
    """Verify that choosing all 'A' (generally highest behavioral score) produces elevated scores."""
    answers = {q["id"]: "A" for q in QUESTIONS}
    raw = calculate_raw_scores(answers)
    normalized = normalize_scores(raw)
    
    for dim in DIMENSIONS:
        assert dim in normalized
        assert normalized[dim] >= 55.0, f"Dimension {dim} was {normalized[dim]}, expected >= 55"
        assert normalized[dim] <= 100.0


def test_scoring_dimension_maximum_possible():
    """Verify that selecting the best option for a specific dimension achieves near 100%."""
    # For communication, pick the option with highest communication points in each question
    comm_answers = {}
    for q in QUESTIONS:
        best_opt = "A"
        best_pts = -1
        for opt_id, score_map in q["scores"].items():
            pts = score_map.get("communication", 0)
            if pts > best_pts:
                best_pts = pts
                best_opt = opt_id
        comm_answers[q["id"]] = best_opt
        
    raw = calculate_raw_scores(comm_answers)
    normalized = normalize_scores(raw)
    assert normalized["communication"] >= 99.0


def test_scoring_all_low_options():
    """Verify that choosing all 'D' produces low scores."""
    answers = {q["id"]: "D" for q in QUESTIONS}
    raw = calculate_raw_scores(answers)
    normalized = normalize_scores(raw)
    
    for dim in DIMENSIONS:
        assert dim in normalized
        assert normalized[dim] <= 25.0, f"Dimension {dim} was {normalized[dim]}, expected <= 25"
        assert normalized[dim] >= 0.0


def test_behavioral_profile_structure():
    """Verify calculate_behavioral_profile returns complete metadata and bounds."""
    answers = {q["id"]: "B" for q in QUESTIONS}
    profile = calculate_behavioral_profile(answers)
    
    assert "scores" in profile
    assert len(profile["scores"]) == 10
    assert "dominant_traits" in profile
    assert len(profile["dominant_traits"]) == 3
    assert "growth_traits" in profile
    assert len(profile["growth_traits"]) == 2
    assert profile["answered_count"] == 40
    assert profile["total_questions"] == 40
    
    for dim, score in profile["scores"].items():
        assert 0.0 <= score <= 100.0


def test_partial_answers_handling():
    """Verify that answering a subset of questions gracefully calculates available dimensions."""
    answers = {1: "A", 2: "A", 5: "B"}
    profile = calculate_behavioral_profile(answers)
    
    assert profile["answered_count"] == 3
    assert len(profile["scores"]) == 10
