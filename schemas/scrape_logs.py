from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ScrapeLog(BaseModel):
    run_id: Optional[str] = None

    url: str

    source: Optional[str] = None

    status: str

    extraction_method: Optional[str] = None

    used_llm: bool = False

    retry_count: int = 0

    error_type: Optional[str] = None

    error_message: Optional[str] = None

    started_at: Optional[datetime] = None

    finished_at: Optional[datetime] = None

    created_at: Optional[datetime] = None