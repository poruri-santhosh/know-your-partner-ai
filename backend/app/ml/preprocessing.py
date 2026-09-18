"""Data cleaning, validation, and preprocessing helpers."""

from typing import Dict, Any, Tuple
from app.data.questions import DIMENSIONS, QUESTION_LOOKUP

def validate_answers_payload(raw_answers: Any) -> Tuple[bool, Dict[int, str], str]:
    """
    Validate and sanitize user answer inputs.
    raw_answers can be:
    - dict of {question_id: 'A'/'B'/'C'/'D'}
    - list of [{'question_id': 1, 'selected_option': 'A'}, ...]
    """
    cleaned: Dict[int, str] = {}
    
    if isinstance(raw_answers, dict):
        for k, v in raw_answers.items():
            try:
                qid = int(k)
            except (ValueError, TypeError):
                continue
            if qid in QUESTION_LOOKUP:
                cleaned[qid] = str(v).strip().upper()
    elif isinstance(raw_answers, list):
        for item in raw_answers:
            if isinstance(item, dict):
                qid = item.get("question_id") or item.get("id")
                opt = item.get("selected_option") or item.get("option") or item.get("answer")
                try:
                    qid_int = int(qid)
                except (ValueError, TypeError):
                    continue
                if qid_int in QUESTION_LOOKUP and opt:
                    cleaned[qid_int] = str(opt).strip().upper()
    else:
        return False, {}, "Invalid answer payload format. Expected dict or list."
        
    if not cleaned:
        return False, {}, "No valid answers found in submission."
        
    return True, cleaned, ""


def clean_profile_vector(profile_dict: Dict[str, Any]) -> Dict[str, float]:
    """Ensure all 10 dimension keys exist, bounded to [0.0, 100.0]."""
    cleaned = {}
    for dim in DIMENSIONS:
        val = profile_dict.get(dim, 50.0)
        try:
            val_float = float(val)
        except (ValueError, TypeError):
            val_float = 50.0
        cleaned[dim] = max(0.0, min(100.0, val_float))
    return cleaned
