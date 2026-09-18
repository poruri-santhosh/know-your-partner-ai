"""Feature engineering pipeline for pair compatibility analysis."""

import math
from typing import Dict, List, Any
from app.data.questions import DIMENSIONS

DIMENSION_KEYS = list(DIMENSIONS.keys())

# Ordered feature column names used for training and prediction
FEATURE_NAMES = [
    f"{dim}_diff" for dim in DIMENSION_KEYS
] + [
    "comm_x_conflict_diff",
    "finance_x_career_diff",
    "family_x_lifestyle_diff",
    "mean_abs_diff",
    "max_abs_diff",
    "euclidean_distance",
]


def extract_pair_features(
    profile_a: Dict[str, float],
    profile_b: Dict[str, float]
) -> Dict[str, float]:
    """
    Extract pairwise comparison features between two behavioral profiles.
    Inputs are dimension scores on a 0-100 scale.
    """
    features: Dict[str, float] = {}
    diffs = []
    
    for dim in DIMENSION_KEYS:
        score_a = float(profile_a.get(dim, 50.0))
        score_b = float(profile_b.get(dim, 50.0))
        diff = abs(score_a - score_b)
        features[f"{dim}_diff"] = round(diff, 2)
        diffs.append(diff)
        
    # Interaction terms
    features["comm_x_conflict_diff"] = round(
        (features["communication_diff"] * features["conflict_handling_diff"]) / 100.0, 2
    )
    features["finance_x_career_diff"] = round(
        (features["financial_attitude_diff"] * features["career_orientation_diff"]) / 100.0, 2
    )
    features["family_x_lifestyle_diff"] = round(
        (features["family_orientation_diff"] * features["lifestyle_preference_diff"]) / 100.0, 2
    )
    
    # Aggregate differences
    features["mean_abs_diff"] = round(sum(diffs) / len(diffs), 2)
    features["max_abs_diff"] = round(max(diffs), 2)
    features["euclidean_distance"] = round(
        math.sqrt(sum(d ** 2 for d in diffs)), 2
    )
    
    return features


def features_to_vector(features: Dict[str, float]) -> List[float]:
    """Convert features dictionary into an ordered vector for ML models."""
    return [features.get(name, 0.0) for name in FEATURE_NAMES]
