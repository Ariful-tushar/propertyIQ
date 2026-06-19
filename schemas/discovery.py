from pydantic import BaseModel

class DiscoveryResult(BaseModel):

    start_url : str
    visited_pages : list[str]
    property_urls : list[str]
    total_properties : int    