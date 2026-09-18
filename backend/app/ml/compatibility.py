"""Compatibility calculation, candidate archetypes, and recommendation engine."""

from typing import Dict, List, Any
from app.data.questions import DIMENSIONS

# Core dimension weights for baseline mathematical compatibility formula
DIMENSION_WEIGHTS = {
    "communication": 0.18,
    "conflict_handling": 0.18,
    "financial_attitude": 0.14,
    "family_orientation": 0.12,
    "emotional_openness": 0.12,
    "lifestyle_preference": 0.10,
    "career_orientation": 0.06,
    "social_nature": 0.04,
    "independence": 0.03,
    "adventure": 0.03,
}

# Distinct candidate archetypes used for recommendations and comparison
CANDIDATE_ARCHETYPES = [
    {
        "id": "cand_anchor",
        "name": "Alex - The Grounded Anchor",
        "archetype": "The Grounded Anchor",
        "tagline": "Values warmth, financial stability, strong family roots, and steady habits.",
        "avatar": "anchor",
        "scores": {
            "communication": 82.0,
            "emotional_openness": 75.0,
            "social_nature": 55.0,
            "independence": 60.0,
            "family_orientation": 90.0,
            "financial_attitude": 88.0,
            "career_orientation": 76.0,
            "adventure": 48.0,
            "conflict_handling": 84.0,
            "lifestyle_preference": 85.0,
        },
    },
    {
        "id": "cand_trailblazer",
        "name": "Jordan - The Trailblazer",
        "archetype": "The Trailblazer",
        "tagline": "Driven by career vision, intellectual ambition, and mutual autonomy.",
        "avatar": "briefcase",
        "scores": {
            "communication": 86.0,
            "emotional_openness": 68.0,
            "social_nature": 65.0,
            "independence": 85.0,
            "family_orientation": 65.0,
            "financial_attitude": 82.0,
            "career_orientation": 92.0,
            "adventure": 68.0,
            "conflict_handling": 80.0,
            "lifestyle_preference": 72.0,
        },
    },
    {
        "id": "cand_harmonizer",
        "name": "Taylor - The Empathetic Harmonizer",
        "archetype": "The Empathetic Harmonizer",
        "tagline": "Deep emotional attunement, compassionate listening, and cooperative conflict resolution.",
        "avatar": "heart",
        "scores": {
            "communication": 92.0,
            "emotional_openness": 90.0,
            "social_nature": 70.0,
            "independence": 65.0,
            "family_orientation": 82.0,
            "financial_attitude": 74.0,
            "career_orientation": 70.0,
            "adventure": 58.0,
            "conflict_handling": 90.0,
            "lifestyle_preference": 78.0,
        },
    },
    {
        "id": "cand_explorer",
        "name": "Sam - The Spontaneous Explorer",
        "archetype": "The Spontaneous Explorer",
        "tagline": "Thrives on travel, outdoor adventures, spontaneity, and creative energy.",
        "avatar": "compass",
        "scores": {
            "communication": 78.0,
            "emotional_openness": 72.0,
            "social_nature": 82.0,
            "independence": 80.0,
            "family_orientation": 60.0,
            "financial_attitude": 62.0,
            "career_orientation": 75.0,
            "adventure": 92.0,
            "conflict_handling": 74.0,
            "lifestyle_preference": 52.0,
        },
    },
    {
        "id": "cand_diplomat",
        "name": "Morgan - The Thoughtful Diplomat",
        "archetype": "The Thoughtful Diplomat",
        "tagline": "Balanced, patient, highly adaptable, and master of calm conversation.",
        "avatar": "scale",
        "scores": {
            "communication": 88.0,
            "emotional_openness": 80.0,
            "social_nature": 62.0,
            "independence": 72.0,
            "family_orientation": 78.0,
            "financial_attitude": 80.0,
            "career_orientation": 80.0,
            "adventure": 64.0,
            "conflict_handling": 88.0,
            "lifestyle_preference": 80.0,
        },
    },
]


def calculate_mathematical_compatibility(
    profile_a: Dict[str, float],
    profile_b: Dict[str, float]
) -> Dict[str, Any]:
    """
    Calculate baseline mathematical compatibility using weighted dimension distance.
    Returns overall score (0-100) and dimension-by-dimension breakdown.
    """
    dimension_breakdown = {}
    weighted_diff_sum = 0.0
    
    for dim, weight in DIMENSION_WEIGHTS.items():
        score_a = float(profile_a.get(dim, 50.0))
        score_b = float(profile_b.get(dim, 50.0))
        diff = abs(score_a - score_b)
        dim_compatibility = max(0.0, min(100.0, 100.0 - diff))
        
        weighted_diff_sum += weight * diff
        
        dimension_breakdown[dim] = {
            "dimension": dim,
            "name": DIMENSIONS[dim]["name"],
            "user_score": round(score_a, 1),
            "partner_score": round(score_b, 1),
            "difference": round(diff, 1),
            "compatibility": round(dim_compatibility, 1),
            "weight": weight,
        }
        
    overall = max(0.0, min(100.0, 100.0 - weighted_diff_sum))
    
    return {
        "overall_compatibility": round(overall, 1),
        "dimension_breakdown": dimension_breakdown,
        "method": "weighted_distance",
    }


def synthesize_ideal_partner_profile(user_profile: Dict[str, float]) -> Dict[str, Any]:
    """
    Synthesize the ideal complementary partner profile based on relationship science principles:
    - High communication & conflict handling are universal anchors.
    - Financial & family orientation thrive on close alignment.
    - Independence & social nature flourish with healthy complementary balance.
    """
    ideal_scores: Dict[str, float] = {}
    trait_levels: Dict[str, str] = {}
    
    for dim in DIMENSIONS:
        u_score = float(user_profile.get(dim, 50.0))
        
        if dim in ["communication", "conflict_handling"]:
            # Healthy relationships need strong communication/conflict resolution
            ideal = max(78.0, min(95.0, (u_score * 0.5) + 45.0))
        elif dim in ["financial_attitude", "family_orientation", "lifestyle_preference"]:
            # Strong alignment needed on financial values, family, and home routine
            ideal = max(35.0, min(95.0, (u_score * 0.85) + 10.0))
        elif dim in ["adventure", "social_nature"]:
            # Moderate complementary flexibility
            if u_score < 45.0:
                ideal = u_score + 15.0  # Slightly more social/adventurous to bring balance
            elif u_score > 80.0:
                ideal = u_score - 10.0  # Grounding influence
            else:
                ideal = u_score
        else:
            ideal = max(40.0, min(90.0, u_score))
            
        ideal = round(ideal, 1)
        ideal_scores[dim] = ideal
        trait_levels[dim] = "High" if ideal >= 75 else ("Moderate" if ideal >= 45 else "Low")
        
    return {
        "ideal_scores": ideal_scores,
        "trait_levels": trait_levels,
    }
