from typing import Optional, List, Literal
from pydantic import BaseModel, Field


class Slide(BaseModel):
    slide_number: int = Field(..., description="Slide number")
    title: str = Field(..., description="Slide title")
    slide_content: Optional[str] = Field(None, description="Main slide text content")
    key_bullet_points: List[str] = Field(default_factory=list, description="Key bullet points")
    suggested_images: Optional[str] = Field(None, description="Suggested images")
    suggested_charts: Optional[str] = Field(None, description="Suggested charts")
    suggested_tables: Optional[str] = Field(None, description="Suggested tables")
    speaker_notes: str = Field(..., description="Speaker notes")

class PlanOutput(BaseModel):
    title: str = Field(..., description="Main presentation title")
    subtitle: str = Field(..., description="Presentation subtitle")
    topic: str = Field(..., description="Main topic")
    target_audience: str = Field(..., description="Target audience")
    number_of_slides: int = Field(..., description="Total number of slides")
    slides: List[Slide] = Field(..., description="List of slides")

class HitlDecision(BaseModel):
    action: Literal["approve", "revise", "edit"] = Field(description="type of decision")
    feedback: str | None = Field(description="feedback")