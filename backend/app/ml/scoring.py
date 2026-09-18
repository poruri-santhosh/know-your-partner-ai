"""Scoring and normalization logic for the behavioral questionnaire."""

from typing import Dict, Any, Union
from app.data.questions import (
    DIMENSIONS,
    QUESTIONS,
    QUESTION_LOOKUP,
    MIN_POSSIBLE_SCORES,
    MAX_POSSIBLE_SCORES,
)

def calculate_raw_scores(answers: Dict[Union[int, str], str]) -> Dict[str, float]:
    """
    Calculate raw score sums across dimensions based on user answers.
    answers: dict mapping question_id (int or str) -> chosen option ('A', 'B', 'C', 'D')
    """
    raw_scores = {dim: 0.0 for dim in DIMENSIONS}
    
    for q_id_key, chosen_opt in answers.items():
        try:
            q_id = int(q_id_key)
        except (ValueError, TypeError):
            continue
            
        question = QUESTION_LOOKUP.get(q_id)
        if not question:
            continue
            
        chosen_opt = str(chosen_opt).strip().upper()
        option_scores = question["scores"].get(chosen_opt)
        if not option_scores:
            continue
            
        for dim, pts in option_scores.items():
            if dim in raw_scores:
                raw_scores[dim] += pts

    return raw_scores


def normalize_scores(raw_scores: Dict[str, float]) -> Dict[str, float]:
    """
    Normalize raw dimension scores into calibrated percentage values (0 - 100).
    Uses min-max bounds calibrated from question point distributions.
    """
    normalized: Dict[str, float] = {}
    
    for dim in DIMENSIONS:
        raw = raw_scores.get(dim, 0.0)
        min_score = MIN_POSSIBLE_SCORES.get(dim, 4.0)
        max_score = MAX_POSSIBLE_SCORES.get(dim, 20.0)
        
        if max_score > min_score:
            score_pct = ((raw - min_score) / (max_score - min_score)) * 100.0
        else:
            score_pct = 50.0
            
        # Clamp to [0, 100] and round to 1 decimal place
        clamped = max(0.0, min(100.0, score_pct))
        normalized[dim] = round(clamped, 1)
        
    return normalized


def calculate_behavioral_profile(answers: Dict[Union[int, str], str]) -> Dict[str, Any]:
    """
    Full scoring pipeline:
    Takes answers -> computes raw scores -> normalizes to 0-100 -> builds profile metadata.
    """
    raw_scores = calculate_raw_scores(answers)
    normalized = normalize_scores(raw_scores)
    
    # Sort traits to find primary dominant strengths & growth areas
    sorted_traits = sorted(normalized.items(), key=lambda item: item[1], reverse=True)
    
    dominant_traits = [
        {
            "dimension": dim,
            "name": DIMENSIONS[dim]["name"],
            "score": score,
            "level": "High" if score >= 75 else ("Moderate" if score >= 45 else "Low"),
            "description": DIMENSIONS[dim]["description"],
        }
        for dim, score in sorted_traits[:3]
    ]
    
    growth_traits = [
        {
            "dimension": dim,
            "name": DIMENSIONS[dim]["name"],
            "score": score,
            "level": "High" if score >= 75 else ("Moderate" if score >= 45 else "Low"),
            "description": DIMENSIONS[dim]["description"],
        }
        for dim, score in sorted_traits[-2:]
    ]

    dimension_details = {
        dim: {
            "name": DIMENSIONS[dim]["name"],
            "score": normalized[dim],
            "level": "High" if normalized[dim] >= 75 else ("Moderate" if normalized[dim] >= 45 else "Low"),
            "description": DIMENSIONS[dim]["description"],
            "weight": DIMENSIONS[dim]["weight"],
        }
        for dim in DIMENSIONS
    }
    
    return {
        "scores": normalized,
        "raw_scores": raw_scores,
        "dominant_traits": dominant_traits,
        "growth_traits": growth_traits,
        "dimension_details": dimension_details,
        "answered_count": len([k for k in answers if int(k) in QUESTION_LOOKUP]),
        "total_questions": len(QUESTIONS),
    }
