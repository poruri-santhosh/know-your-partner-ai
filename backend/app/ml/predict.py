"""Inference service for compatibility prediction and archetype classification."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import joblib
import numpy as np

from app.data.questions import DIMENSIONS
from app.ml.feature_engineering import DIMENSION_KEYS, FEATURE_NAMES, extract_pair_features, features_to_vector
from app.ml.compatibility import calculate_mathematical_compatibility

MODELS_DIR = Path(__file__).resolve().parent.parent / "models"
MODEL_PATH = MODELS_DIR / "compatibility_model.pkl"
KMEANS_PATH = MODELS_DIR / "kmeans_archetypes.pkl"

_COMPATIBILITY_MODEL_CACHE: Optional[Dict[str, Any]] = None
_KMEANS_MODEL_CACHE: Optional[Dict[str, Any]] = None


def load_compatibility_model() -> Optional[Dict[str, Any]]:
    """Load cached compatibility model from disk."""
    global _COMPATIBILITY_MODEL_CACHE
    if _COMPATIBILITY_MODEL_CACHE is not None:
        return _COMPATIBILITY_MODEL_CACHE
        
    if MODEL_PATH.exists():
        try:
            _COMPATIBILITY_MODEL_CACHE = joblib.load(MODEL_PATH)
            return _COMPATIBILITY_MODEL_CACHE
        except Exception as e:
            print(f"[Warning] Failed to load compatibility model: {e}")
            return None
    return None


def load_kmeans_model() -> Optional[Dict[str, Any]]:
    """Load cached K-Means clustering model from disk."""
    global _KMEANS_MODEL_CACHE
    if _KMEANS_MODEL_CACHE is not None:
        return _KMEANS_MODEL_CACHE
        
    if KMEANS_PATH.exists():
        try:
            _KMEANS_MODEL_CACHE = joblib.load(KMEANS_PATH)
            return _KMEANS_MODEL_CACHE
        except Exception as e:
            print(f"[Warning] Failed to load K-Means model: {e}")
            return None
    return None


def predict_pair_compatibility(
    profile_a: Dict[str, float],
    profile_b: Dict[str, float]
) -> Dict[str, Any]:
    """
    Predict compatibility score between two profiles.
    Uses trained ML model if available, falling back gracefully to weighted mathematical distance.
    """
    feats = extract_pair_features(profile_a, profile_b)
    math_result = calculate_mathematical_compatibility(profile_a, profile_b)
    
    model_payload = load_compatibility_model()
    
    if model_payload and "model" in model_payload:
        try:
            import pandas as pd
            model = model_payload["model"]
            vector = features_to_vector(feats)
            df_input = pd.DataFrame([vector], columns=FEATURE_NAMES)
            pred_val = float(model.predict(df_input)[0])
            score = round(max(10.0, min(99.0, pred_val)), 1)
            model_used = model_payload.get("model_name", "Machine Learning Model")
            is_ml = True
        except Exception as e:
            score = math_result["overall_compatibility"]
            model_used = f"Weighted Formula (Fallback due to: {e})"
            is_ml = False
    else:
        score = math_result["overall_compatibility"]
        model_used = "Weighted Mathematical Formula"
        is_ml = False
        
    return {
        "overall_compatibility": score,
        "model_used": model_used,
        "is_ml": is_ml,
        "features": feats,
        "dimension_breakdown": math_result["dimension_breakdown"],
    }


def predict_archetype(user_profile: Dict[str, float]) -> Dict[str, str]:
    """Classify user profile into a behavioral archetype using K-Means clustering."""
    kmeans_payload = load_kmeans_model()
    
    if kmeans_payload and "kmeans" in kmeans_payload:
        try:
            kmeans = kmeans_payload["kmeans"]
            cluster_mapping = kmeans_payload["cluster_mapping"]
            vector = [float(user_profile.get(dim, 50.0)) for dim in DIMENSION_KEYS]
            cluster_id = int(kmeans.predict([vector])[0])
            archetype_info = cluster_mapping.get(cluster_id)
            if archetype_info:
                return archetype_info
        except Exception as e:
            print(f"[Warning] K-Means prediction failed: {e}")
            
    # Heuristic fallback based on dominant trait
    sorted_traits = sorted(user_profile.items(), key=lambda x: x[1], reverse=True)
    top_trait = sorted_traits[0][0] if sorted_traits else "communication"
    
    fallbacks = {
        "family_orientation": {
            "name": "The Grounded Anchor",
            "tagline": "Values deep family roots, financial security, and organized stability.",
            "badge": "Anchor",
        },
        "financial_attitude": {
            "name": "The Grounded Anchor",
            "tagline": "Values deep family roots, financial security, and organized stability.",
            "badge": "Anchor",
        },
        "career_orientation": {
            "name": "The Trailblazer",
            "tagline": "Driven by career vision, intellectual ambition, and mutual autonomy.",
            "badge": "Trailblazer",
        },
        "independence": {
            "name": "The Trailblazer",
            "tagline": "Driven by career vision, intellectual ambition, and mutual autonomy.",
            "badge": "Trailblazer",
        },
        "emotional_openness": {
            "name": "The Empathetic Harmonizer",
            "tagline": "Prioritizes deep emotional connection, open dialogue, and gentle conflict resolution.",
            "badge": "Harmonizer",
        },
        "adventure": {
            "name": "The Spontaneous Explorer",
            "tagline": "Energized by adventure, social discovery, novelty, and flexible spontaneity.",
            "badge": "Explorer",
        },
        "social_nature": {
            "name": "The Spontaneous Explorer",
            "tagline": "Energized by adventure, social discovery, novelty, and flexible spontaneity.",
            "badge": "Explorer",
        },
        "communication": {
            "name": "The Thoughtful Diplomat",
            "tagline": "A calm, highly communicative presence who builds balanced, peaceful partnerships.",
            "badge": "Diplomat",
        },
        "conflict_handling": {
            "name": "The Thoughtful Diplomat",
            "tagline": "A calm, highly communicative presence who builds balanced, peaceful partnerships.",
            "badge": "Diplomat",
        },
        "lifestyle_preference": {
            "name": "The Grounded Anchor",
            "tagline": "Values deep family roots, financial security, and organized stability.",
            "badge": "Anchor",
        },
    }
    
    return fallbacks.get(top_trait, fallbacks["communication"])
