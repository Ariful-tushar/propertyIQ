from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime


class PropertyItem(BaseModel):
    title: str

    price: Optional[int] = None

    size_of_property: Optional[float] = None

    rooms: Optional[float] = None

    location_of_property: Optional[str] = None

    description_of_property: Optional[str] = None

    property_url: HttpUrl

    image_url: Optional[HttpUrl] = None

    source: str

    created_at: Optional[datetime] = None

    updated_at: Optional[datetime] = None