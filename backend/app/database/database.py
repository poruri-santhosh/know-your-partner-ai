"""SQLAlchemy Database configuration, session management, and persistence."""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database path for SQLite default
if os.environ.get("VERCEL"):
    DEFAULT_SQLITE_PATH = Path("/tmp") / "database.sqlite"
else:
    DATA_DIR = Path(__file__).resolve().parent.parent / "data"
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    DEFAULT_SQLITE_PATH = DATA_DIR / "database.sqlite"

# Support SQLite or PostgreSQL from environment
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    # Use SQLite
    DATABASE_URL = f"sqlite:///{DEFAULT_SQLITE_PATH}"

# Configure engine
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI Dependency for database session management."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Create all SQL tables based on SQLAlchemy models."""
    from app.database.models import SubmissionRecord, AnswerRecord
    Base.metadata.create_all(bind=engine)
    print(f"SQL Database initialized using: {DATABASE_URL}", flush=True)


def save_submission(
    submission_id: str,
    answered_count: int,
    archetype_name: str,
    archetype_badge: str,
    profile_data: Dict[str, Any],
    ideal_partner_data: Dict[str, Any],
    result_data: Dict[str, Any],
    answers_map: Dict[int, str]
):
    """Save full submission and answers to SQL database via SQLAlchemy ORM."""
    from app.database.models import SubmissionRecord, AnswerRecord
    
    db = SessionLocal()
    try:
        # Check if exists
        existing = db.query(SubmissionRecord).filter(SubmissionRecord.id == submission_id).first()
        if existing:
            existing.answered_count = answered_count
            existing.archetype_name = archetype_name
            existing.archetype_badge = archetype_badge
            existing.profile_json = json.dumps(profile_data)
            existing.ideal_partner_json = json.dumps(ideal_partner_data)
            existing.result_json = json.dumps(result_data)
        else:
            record = SubmissionRecord(
                id=submission_id,
                answered_count=answered_count,
                archetype_name=archetype_name,
                archetype_badge=archetype_badge,
                profile_json=json.dumps(profile_data),
                ideal_partner_json=json.dumps(ideal_partner_data),
                result_json=json.dumps(result_data),
            )
            db.add(record)
            
        # Add answer records
        for q_id, opt in answers_map.items():
            ans = AnswerRecord(
                submission_id=submission_id,
                question_id=int(q_id),
                selected_option=str(opt),
            )
            db.add(ans)
            
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


def get_submission(submission_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full analysis result by submission ID using SQLAlchemy."""
    from app.database.models import SubmissionRecord
    
    db = SessionLocal()
    try:
        row = db.query(SubmissionRecord).filter(SubmissionRecord.id == submission_id).first()
        if not row:
            return None
            
        return {
            "id": row.id,
            "created_at": str(row.created_at),
            "answered_count": row.answered_count,
            "archetype_name": row.archetype_name,
            "archetype_badge": row.archetype_badge,
            "profile": json.loads(row.profile_json) if row.profile_json else {},
            "ideal_partner": json.loads(row.ideal_partner_json) if row.ideal_partner_json else {},
            "result": json.loads(row.result_json) if row.result_json else {},
        }
    finally:
        db.close()
