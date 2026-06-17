from pydantic import BaseModel
from typing import Any, Dict, Optional
from datetime import datetime


class PropertyMetadata(BaseModel):
    property_id: int

    attributes: Dict[str, Any] = {}

    ai_signals: Dict[str, Any] = {}

    created_at: Optional[datetime] = None