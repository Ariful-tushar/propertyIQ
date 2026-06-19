from pathlib import Path
from typing import cast

from dotenv import load_dotenv

from langchain_groq import ChatGroq

from schemas.selector import (
    SelectorResult
)


class SelectorAgent:

    def __init__(self):

        load_dotenv()

        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0,
        )

        self.structured_llm = (
            self.llm.with_structured_output(
                SelectorResult
            )
        )

    def generate(
        self,
        html_file: Path,
        required_selectors: list[str],
    ) -> SelectorResult:

        reduced_html = (
            html_file.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        )

        prompt = self._build_prompt(
            reduced_html,
            required_selectors,
        )
        result = self.structured_llm.invoke(
            prompt
        )

        return cast(
            SelectorResult,
            result
        )

    def _build_prompt(
        self,
        html: str,
        required_selectors: list[str],
    ) -> str:

        return f"""
You are an expert web scraping engineer.

Generate XPath selectors.

Required selectors:

{required_selectors}

Rules:

- Return XPath only
- Return null if selector not found
- No explanation
- No markdown
- Use href selectors for links

HTML:

{html}
"""