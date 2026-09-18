"""Orchestration service for behavioral profiling, compatibility analysis, and AI narrative synthesis."""

import os
import uuid
from typing import Dict, Any, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.data.questions import DIMENSIONS
from app.ml.scoring import calculate_behavioral_profile
from app.ml.preprocessing import validate_answers_payload, clean_profile_vector
from app.ml.compatibility import (
    CANDIDATE_ARCHETYPES,
    synthesize_ideal_partner_profile,
)
from app.ml.predict import predict_pair_compatibility, predict_archetype
from app.database.database import save_submission


def generate_psychological_narrative(
    user_profile: Dict[str, float],
    archetype: Dict[str, str],
    ideal_partner: Dict[str, float],
    top_candidate: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Generate in-depth psychological explanation and relationship insights.
    Uses Gemini API when GEMINI_API_KEY is present, or a rich behavioral science heuristic engine.
    """
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    
    if api_key:
        try:
            from google import genai
            client = genai.Client(api_key=api_key)
            
            prompt = f"""
            You are a relationship psychologist and behavioral compatibility expert.
            Analyze this user's behavioral profile:
            - Archetype: {archetype.get('name')} ({archetype.get('tagline')})
            - User Dimension Scores (0-100): {user_profile}
            - Ideal Complementary Partner Profile: {ideal_partner}
            - Top Matching Candidate Archetype: {top_candidate.get('name')} with {top_candidate.get('compatibility_score')}% compatibility.

            Provide an insightful, encouraging, and scientifically sound relationship analysis in JSON format with keys:
            - "summary": A 2-sentence summary of the user's relational approach and core values.
            - "ideal_partner_qualities": A paragraph explaining what behavioral traits best complement them and why.
            - "relationship_strengths": 2-3 key assets they bring into a partnership.
            - "growth_advice": 1-2 constructive communication or behavioral tips for long-term harmony.
            - "disclaimer": Mention that this represents a behavioral science estimation rather than marital certainty.
            """
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={"response_mime_type": "application/json"}
            )
            import json
            ai_data = json.loads(response.text)
            ai_data["source"] = "Gemini Generative AI"
            return ai_data
        except Exception as e:
            print(f"[Info] Generative AI API fallback invoked: {e}")

    # Psychological Heuristic Narrative Engine (Calibrated Behavioral Science Fallback)
    sorted_traits = sorted(user_profile.items(), key=lambda x: x[1], reverse=True)
    top_trait, top_score = sorted_traits[0]
    second_trait, second_score = sorted_traits[1]
    lowest_trait, lowest_score = sorted_traits[-1]
    
    top_name = DIMENSIONS[top_trait]["name"]
    second_name = DIMENSIONS[second_trait]["name"]
    lowest_name = DIMENSIONS[lowest_trait]["name"]
    
    summary = (
        f"Your behavioral profile reflects a strong foundation in {top_name} ({top_score}%) and "
        f"{second_name} ({second_score}%), identifying you with {archetype.get('name')}. "
        f"You approach relationships with intentionality, seeking meaningful alignment in how you navigate daily life."
    )
    
    ideal_partner_qualities = (
        f"Given your emphasis on {top_name}, you thrive best with a partner who mirrors your dedication to "
        f"constructive engagement while offering steady reassurance. A partner exhibiting high emotional maturity "
        f"and complementary pacing on {lowest_name.lower()} will provide both safety and mutual encouragement to grow."
    )
    
    strengths = [
        f"High {top_name}: You communicate with clarity and bring proactive energy to shared relationship goals.",
        f"Strong {second_name}: You provide a reliable emotional anchor when facing life's joint decisions.",
        "Collaborative Mindset: You value fair problem-solving over defensive posturing in moments of tension.",
    ]
    
    growth_advice = (
        f"Pay attention to how differences in {lowest_name} manifest during high-stress periods. "
        f"Granting each other grace when your partner processes decisions at a different speed will turn potential friction into connection."
    )
    
    return {
        "source": "Psychological Behavioral Engine",
        "summary": summary,
        "ideal_partner_qualities": ideal_partner_qualities,
        "relationship_strengths": strengths,
        "growth_advice": growth_advice,
        "disclaimer": "This analysis represents a hypothetical compatibility pattern based on questionnaire responses, not a deterministic prediction.",
    }


def analyze_quiz_submission(
    raw_answers: Any,
    custom_partner_profile: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """
    Execute full analysis pipeline:
    1. Validation -> 2. Scoring -> 3. Archetype -> 4. Ideal Partner -> 5. Candidate Matches -> 6. AI Narrative
    """
    valid, cleaned_answers, err = validate_answers_payload(raw_answers)
    if not valid:
        raise ValueError(err)
        
    profile_result = calculate_behavioral_profile(cleaned_answers)
    user_scores = profile_result["scores"]
    
    # 3. Classify Archetype
    archetype = predict_archetype(user_scores)
    
    # 4. Synthesize Ideal Complementary Partner
    ideal_partner_data = synthesize_ideal_partner_profile(user_scores)
    ideal_scores = ideal_partner_data["ideal_scores"]
    
    # 5. Evaluate Target Partner Compatibility
    target_partner = clean_profile_vector(custom_partner_profile) if custom_partner_profile else ideal_scores
    target_compatibility = predict_pair_compatibility(user_scores, target_partner)
    
    # 6. Rank Candidate Matches
    candidate_matches = []
    for cand in CANDIDATE_ARCHETYPES:
        cand_compat = predict_pair_compatibility(user_scores, cand["scores"])
        candidate_matches.append({
            "id": cand["id"],
            "name": cand["name"],
            "archetype": cand["archetype"],
            "tagline": cand["tagline"],
            "avatar": cand["avatar"],
            "compatibility_score": cand_compat["overall_compatibility"],
            "model_used": cand_compat["model_used"],
            "scores": cand["scores"],
        })
        
    candidate_matches.sort(key=lambda c: c["compatibility_score"], reverse=True)
    top_candidate = candidate_matches[0]
    
    # 7. Generate Narrative
    narrative = generate_psychological_narrative(
        user_profile=user_scores,
        archetype=archetype,
        ideal_partner=ideal_scores,
        top_candidate=top_candidate,
    )
    
    submission_id = str(uuid.uuid4())
    
    full_result = {
        "submission_id": submission_id,
        "user_profile": user_scores,
        "dimension_details": profile_result["dimension_details"],
        "dominant_traits": profile_result["dominant_traits"],
        "growth_traits": profile_result["growth_traits"],
        "archetype": archetype,
        "ideal_partner_profile": ideal_scores,
        "ideal_trait_levels": ideal_partner_data["trait_levels"],
        "overall_compatibility": target_compatibility["overall_compatibility"],
        "model_used": target_compatibility["model_used"],
        "is_ml": target_compatibility["is_ml"],
        "dimension_breakdown": target_compatibility["dimension_breakdown"],
        "candidate_matches": candidate_matches,
        "ai_narrative": narrative,
        "answered_count": profile_result["answered_count"],
        "total_questions": profile_result["total_questions"],
    }
    
    # 8. Persist to SQLite
    try:
        save_submission(
            submission_id=submission_id,
            answered_count=profile_result["answered_count"],
            archetype_name=archetype.get("name", "Unknown"),
            archetype_badge=archetype.get("badge", "Profile"),
            profile_data=user_scores,
            ideal_partner_data=ideal_scores,
            result_data=full_result,
            answers_map=cleaned_answers,
        )
    except Exception as e:
        print(f"[Warning] Failed to save submission to database: {e}")
        
    return full_result
