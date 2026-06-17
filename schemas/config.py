from typing import Any

from pydantic import BaseModel, HttpUrl


class ScrapeConfig(BaseModel):
    start_url: HttpUrl
    fields: list[str]
    recommendation_criteria: dict[str, Any] = {}