"""
AI candidate scoring models.

These models represent the AI evaluation of a candidate
against a specific job description.
"""

from enum import Enum
from typing import List

from pydantic import BaseModel, Field


class FitCategory(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class MatchDetail(BaseModel):
    matched: bool = False
    score: float = Field(default=0, ge=0, le=100)
    reason: str = ""


class CandidateScore(BaseModel):
    overall_score: float = Field(default=0, ge=0, le=100)

    fit_category: FitCategory = FitCategory.LOW

    ai_confidence: float = Field(default=0, ge=0, le=100)

    skills_match: MatchDetail = Field(default_factory=MatchDetail)

    experience_match: MatchDetail = Field(default_factory=MatchDetail)

    salary_alignment: MatchDetail = Field(default_factory=MatchDetail)

    location_alignment: MatchDetail = Field(default_factory=MatchDetail)

    education_match: MatchDetail = Field(default_factory=MatchDetail)

    language_match: MatchDetail = Field(default_factory=MatchDetail)

    certification_match: MatchDetail = Field(default_factory=MatchDetail)

    key_strengths: List[str] = Field(default_factory=list)

    missing_requirements: List[str] = Field(default_factory=list)

    red_flags: List[str] = Field(default_factory=list)

    recruiter_summary: str = ""

    recommended_next_action: str = ""