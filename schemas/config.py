from enum import Enum
from typing import Any

from pydantic import BaseModel, HttpUrl, Field


class DiscoveryMode(str, Enum):
    SCRAPY = "scrapy"
    PLAYWRIGHT = "playwright"
    AUTO = "auto"


class ScrapeConfig(BaseModel):
    start_url: HttpUrl

    discovery_mode: DiscoveryMode = (
        DiscoveryMode.SCRAPY
    )

    fields: list[str]

    recommendation_criteria: dict[str, Any] = Field(
    default_factory=dict
)