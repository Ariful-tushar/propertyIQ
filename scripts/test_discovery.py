from config.config_loader import ConfigLoader
from discovery.discovery_manager import DiscoveryManager


def main():
    config = ConfigLoader.load("configs/search_config.json")

    result = DiscoveryManager().run(config)

    print()
    print("DISCOVERY RESULT")
    print("----------------")
    print("Visited pages:", len(result.visited_pages))
    print("Total properties:", result.total_properties)

    print()
    for url in result.property_urls:
        print(url)


if __name__ == "__main__":
    main()