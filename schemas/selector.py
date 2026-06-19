from pydantic import BaseModel


class SelectorResult(BaseModel):
    selectors: dict[str, str | None]