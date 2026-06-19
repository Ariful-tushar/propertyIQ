from schemas.config import DiscoveryMode

from discovery.scrapy_discovery import (
    ScrapyDiscovery
)


class DiscoveryManager:

    def run(self, config):

        if (
            config.discovery_mode
            == DiscoveryMode.SCRAPY
        ):
            return (
                ScrapyDiscovery()
                .discover(
                    str(config.start_url)
                )
            )

        raise ValueError(
            f"Unsupported discovery mode: "
            f"{config.discovery_mode}"
        )