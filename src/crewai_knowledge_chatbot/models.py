from pydantic import BaseModel, Field
from typing import List, Dict

class SkillAssessment(BaseModel):
    problem_solving: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    coding_skills: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    system_design_knowledge: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    general_knowledge: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    essential_skills: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    communication_clarity: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    confidence_level: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    logical_thinking: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    time_management: int = Field(..., ge=0, le=100, description="Score between 0-100%")
    technical_depth: int = Field(..., ge=0, le=100, description="Score between 0-100%")

class EvaluationOutput(BaseModel):
    overall_score: int = Field(..., ge=0, le=10, description="Overall interview score (0-10)")
    skill_assessment: SkillAssessment
    improvement_suggestions: str
    strong_areas: List[str]
    weak_areas: List[str]
    recommended_resources: Dict[str, List[str]]  # Books, Online Courses, Practice Platforms
    final_verdict: str
