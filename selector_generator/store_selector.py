import json

from pathlib import Path

from schemas.selector import (
    SelectorResult
)


class SelectorStore:

    def __init__(self):

        self.output_dir = Path(
            "logs/selectors"
        )

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

    def save(
        self,
        site_name: str,
        selector_type: str,
        selectors: SelectorResult,
    ):

        output_file = (
            self.output_dir
            /
            f"{site_name}_{selector_type}.json"
        )

        output_file.write_text(
            selectors.model_dump_json(
                indent=4
            ),
            encoding="utf-8",
        )

        return output_file