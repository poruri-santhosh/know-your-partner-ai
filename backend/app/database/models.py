from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.database.database import Base


# ─────────────────────────────────────────────────────────────
# SQLAlchemy ORM Models (Stored in SQL Database)
# ─────────────────────────────────────────────────────────────

class SubmissionRecord(Base):
    """SQL table for user quiz submissions, behavioral archetypes, and results."""
    __tablename__ = "submissions"

    id = Column(String(64), primary_key=True, index=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    answered_count = Column(Integer, default=0)
    archetype_name = Column(String(128), nullable=True)
    archetype_badge = Column(String(64), nullable=True)
    profile_json = Column(Text, nullable=True)
    ideal_partner_json = Column(Text, nullable=True)
    result_json = Column(Text, nullable=True)

    # Relationships
    answers = relationship("AnswerRecord", back_populates="submission", cascade="all, delete-orphan")


class AnswerRecord(Base):
    """SQL table for individual question responses linked to a submission."""
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(String(64), ForeignKey("submissions.id"), index=True)
    question_id = Column(Integer, nullable=False)
    selected_option = Column(String(8), nullable=False)

    # Relationship back to submission
    submission = relationship("SubmissionRecord", back_populates="answers")


# ─────────────────────────────────────────────────────────────
# Pydantic Schemas (Used for FastAPI Request & Response Validation)
# ─────────────────────────────────────────────────────────────

class AnswerSubmission(BaseModel):
    question_id: int
    selected_option: str


class QuizSubmissionRequest(BaseModel):
    # Accepts either {"1": "A", "2": "B"} or list of AnswerSubmission
    answers: Union[Dict[str, str], List[AnswerSubmission]]
    partner_profile: Optional[Dict[str, float]] = None


class CompareProfilesRequest(BaseModel):
    user_profile: Dict[str, float]
    partner_profile: Dict[str, float]


class DimensionScore(BaseModel):
    name: str
    score: float
    level: str
    description: str
    weight: float


class ArchetypeInfo(BaseModel):
    name: str
    tagline: str
    badge: str


class CandidateMatch(BaseModel):
    id: str
    name: str
    archetype: str
    tagline: str
    avatar: str
    compatibility_score: float
    scores: Dict[str, float]


class FullAnalysisResult(BaseModel):
    submission_id: str
    user_profile: Dict[str, float]
    dimension_details: Dict[str, Any]
    dominant_traits: List[Dict[str, Any]]
    growth_traits: List[Dict[str, Any]]
    archetype: ArchetypeInfo
    ideal_partner_profile: Dict[str, float]
    ideal_trait_levels: Dict[str, str]
    overall_compatibility: float
    dimension_breakdown: Dict[str, Any]
    candidate_matches: List[CandidateMatch]
    ai_narrative: Dict[str, Any]
