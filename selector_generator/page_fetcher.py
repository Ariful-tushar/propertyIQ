from pathlib import Path
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright


class PageFetcher:

    def __init__(
        self,
        output_dir: str = "logs/html/raw_html",
        headless: bool = False,
    ):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.headless = headless

    def fetch(
        self,
        url: str,
    ) -> Path:

        filename = self._generate_filename(url)

        output_file = (
            self.output_dir
            / filename
        )

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=self.headless
            )

            page = browser.new_page()

            page.goto(
                url,
                wait_until="networkidle",
                timeout=60000,
            )

            html = page.content()

            output_file.write_text(
                html,
                encoding="utf-8",
            )

            browser.close()

        return output_file

    def _generate_filename(
        self,
        url: str,
    ) -> str:

        parsed = urlparse(url)

        filename = (
            parsed.netloc
            .replace(".", "_")
        )

        return f"{filename}.html"