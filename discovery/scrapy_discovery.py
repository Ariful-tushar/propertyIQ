from pathlib import Path
import json
import uuid

from scrapy.crawler import CrawlerProcess

from schemas.discovery import DiscoveryResult
from scrapy_app.spiders.discovery_spider import DiscoverySpider


class ScrapyDiscovery:
    def __init__(self, max_pages: int = 5):
        self.max_pages = max_pages

    def discover(self, start_url: str) -> DiscoveryResult:
        output_dir = Path("logs/discovery")
        output_dir.mkdir(parents=True, exist_ok=True)

        output_file = output_dir / f"discovery_{uuid.uuid4().hex}.jsonl"

        process = CrawlerProcess(
            settings={
                "FEEDS": {
                    str(output_file): {
                        "format": "jsonlines",
                        "encoding": "utf8",
                    }
                },
                "LOG_LEVEL": "INFO",
            }
        )

        process.crawl(
            DiscoverySpider,
            start_url=start_url,
            max_pages=self.max_pages,
        )

        process.start()

        property_urls = set()
        visited_pages = set()

        with output_file.open("r", encoding="utf-8") as file:
            for line in file:
                item = json.loads(line)

                if item.get("type") == "property_url":
                    property_urls.add(item["url"])
                    visited_pages.add(item["source_page"])

        return DiscoveryResult(
            start_url=start_url,
            visited_pages=sorted(visited_pages),
            property_urls=sorted(property_urls),
            total_properties=len(property_urls),
        )