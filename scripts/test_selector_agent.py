from pathlib import Path
from config.config_loader import (
    ConfigLoader
)



from llm.selector_agent import (
    SelectorAgent
)

from selector_generator.store_selector import (
    SelectorStore
)


def main():

    config = ConfigLoader.load(
        "configs/search_config.json"
    )


    reduced_html = Path(
        "logs/html/reduced_html/huutokaupat_com.html"
    )

    selectors = (
        SelectorAgent()
        .generate(
            html_file=reduced_html,
            required_selectors=[
                "property_link",
                "next_page",
            ]
        )
    )

    print(
        selectors.model_dump()
    )

    path = (
        SelectorStore()
        .save(
            site_name="vuokraovi",
            selector_type="discovery",
            selectors=selectors,
        )
    )

    print(path)


if __name__ == "__main__":
    main()