"""Unit tests for feature engineering, compatibility engine, and archetype clustering."""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "backend"))

from app.ml.feature_engineering import extract_pair_features, features_to_vector, FEATURE_NAMES
from app.ml.compatibility import (
    calculate_mathematical_compatibility,
    synthesize_ideal_partner_profile,
    CANDIDATE_ARCHETYPES,
)
from app.ml.predict import predict_pair_compatibility, predict_archetype


@pytest.fixture
def sample_profiles():
    profile_a = {
        "communication": 85.0,
        "emotional_openness": 80.0,
        "social_nature": 65.0,
        "independence": 70.0,
        "family_orientation": 88.0,
        "financial_attitude": 85.0,
        "career_orientation": 82.0,
        "adventure": 60.0,
        "conflict_handling": 85.0,
        "lifestyle_preference": 75.0,
    }
    profile_b = {
        "communication": 80.0,
        "emotional_openness": 75.0,
        "social_nature": 60.0,
        "independence": 75.0,
        "family_orientation": 85.0,
        "financial_attitude": 80.0,
        "career_orientation": 80.0,
        "adventure": 65.0,
        "conflict_handling": 80.0,
        "lifestyle_preference": 80.0,
    }
    return profile_a, profile_b


def test_feature_extraction(sample_profiles):
    """Verify pair feature extraction produces valid differences and interaction terms."""
    p_a, p_b = sample_profiles
    feats = extract_pair_features(p_a, p_b)
    
    assert "communication_diff" in feats
    assert feats["communication_diff"] == 5.0
    assert "mean_abs_diff" in feats
    assert feats["mean_abs_diff"] > 0
    assert "euclidean_distance" in feats
    
    vec = features_to_vector(feats)
    assert len(vec) == len(FEATURE_NAMES)


def test_mathematical_compatibility_identical_profiles():
    """Identical profiles must have 100% mathematical compatibility."""
    profile = {dim: 80.0 for dim in [
        "communication", "emotional_openness", "social_nature", "independence",
        "family_orientation", "financial_attitude", "career_orientation",
        "adventure", "conflict_handling", "lifestyle_preference"
    ]}
    result = calculate_mathematical_compatibility(profile, profile)
    assert result["overall_compatibility"] == 100.0


def test_mathematical_compatibility_differing_profiles(sample_profiles):
    """Similar profiles should yield a high compatibility score."""
    p_a, p_b = sample_profiles
    result = calculate_mathematical_compatibility(p_a, p_b)
    assert 85.0 <= result["overall_compatibility"] <= 98.0
    assert len(result["dimension_breakdown"]) == 10


def test_ml_prediction_pipeline(sample_profiles):
    """Verify ML model predict service runs and bounds predictions."""
    p_a, p_b = sample_profiles
    res = predict_pair_compatibility(p_a, p_b)
    
    assert "overall_compatibility" in res
    assert 10.0 <= res["overall_compatibility"] <= 99.0
    assert "model_used" in res
    assert "dimension_breakdown" in res


def test_archetype_prediction():
    """Verify K-Means / fallback archetype classification returns structured label."""
    high_family_profile = {
        "communication": 75.0,
        "emotional_openness": 70.0,
        "social_nature": 50.0,
        "independence": 55.0,
        "family_orientation": 95.0,
        "financial_attitude": 90.0,
        "career_orientation": 65.0,
        "adventure": 40.0,
        "conflict_handling": 80.0,
        "lifestyle_preference": 85.0,
    }
    archetype = predict_archetype(high_family_profile)
    assert "name" in archetype
    assert "badge" in archetype


def test_synthesize_ideal_partner(sample_profiles):
    """Verify ideal partner profile synthesis provides reasonable scores."""
    p_a, _ = sample_profiles
    ideal = synthesize_ideal_partner_profile(p_a)
    assert "ideal_scores" in ideal
    assert "trait_levels" in ideal
    assert len(ideal["ideal_scores"]) == 10
    
    # Communication should remain robust
    assert ideal["ideal_scores"]["communication"] >= 75.0
