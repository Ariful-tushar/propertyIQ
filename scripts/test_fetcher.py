from config.config_loader import ConfigLoader

from selector_generator.page_fetcher import (
    PageFetcher
)


def main():

    config = ConfigLoader.load(
        "configs/search_config.json"
    )

    fetcher = PageFetcher()

    path = fetcher.fetch(
        str(config.start_url)
    )

    print(path)


if __name__ == "__main__":
    main()