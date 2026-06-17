from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PropertyAnalysis(BaseModel):
    property_id: int

    deal_score: int

    recommendation_label: Optional[str] = None

    summary: Optional[str] = None

    pros: List[str] = []

    cons: List[str] = []

    model_name: Optional[str] = None

    prompt_version: Optional[str] = None

    created_at: Optional[datetime] = None