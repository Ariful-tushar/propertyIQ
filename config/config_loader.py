from pathlib import Path
import json

from schemas.config import ScrapeConfig


class ConfigLoader:

    @staticmethod
    def load(config_path: str) -> ScrapeConfig:

        path = Path(config_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Config file not found: {config_path}"
            )

        with open(path, "r", encoding="utf-8") as file:
            raw_data = json.load(file)

        return ScrapeConfig(**raw_data)