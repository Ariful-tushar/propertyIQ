import scrapy
from urllib.parse import urljoin


class DiscoverySpider(scrapy.Spider):
    name = "discovery_spider"

    custom_settings = {
        "ROBOTSTXT_OBEY": False,
        "DOWNLOAD_DELAY": 1,
        "LOG_LEVEL": "INFO",
    }

    def __init__(self, start_url: str, max_pages: int = 5, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.start_urls = [start_url]
        self.max_pages = int(max_pages)

        self.visited_pages = []
        self.property_urls = set()

    def parse(self, response):
        self.visited_pages.append(response.url)

        for href in response.css("a::attr(href)").getall():
            full_url = urljoin(response.url, href)

            if self._is_property_url(full_url):
                self.property_urls.add(full_url)
                yield {
                    "type": "property_url",
                    "url": full_url,
                    "source_page": response.url,
                }

        if len(self.visited_pages) >= self.max_pages:
            return

        next_page = self._extract_next_page(response)

        if next_page and next_page not in self.visited_pages:
            yield scrapy.Request(
                next_page,
                callback=self.parse,
            )

    def _is_property_url(self, url: str) -> bool:
        url_lower = url.lower()

        keywords = [
            "vuokra-asunto",
            "asunto",
            "apartment",
            "property",
            "listing",
            "rental",
        ]

        return any(keyword in url_lower for keyword in keywords)

    def _extract_next_page(self, response) -> str | None:
        for link in response.css("a"):
            href = link.css("::attr(href)").get()
            text = " ".join(link.css("::text").getall()).strip().lower()

            if not href:
                continue

            if text in ["next", "seuraava", ">"]:
                return urljoin(response.url, href)

            if "page=" in href.lower() or "sivu=" in href.lower():
                return urljoin(response.url, href)

        return None