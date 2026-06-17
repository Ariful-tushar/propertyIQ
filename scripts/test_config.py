from config.config_loader import ConfigLoader


def main():

    config = ConfigLoader.load(
        "configs/search_config.json"
    )

    print(config)

    print()
    print("START URL")
    print(config.start_url)

    print()
    print("FIELDS")
    print(config.fields)

    print()
    print("RECOMMENDATION")
    print(config.recommendation_criteria)


if __name__ == "__main__":
    main()