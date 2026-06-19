from pathlib import Path
from config.config_loader import (
    ConfigLoader
)



from selector_generator.html_reducer import (
    HtmlReducerForSelectors
)


def main():

    config = ConfigLoader.load(
        "configs/search_config.json"
    )

    html_file = "logs/html/raw_html/huutokaupat_com.html"

    reduced_file = (
        HtmlReducerForSelectors()
        .reduce(
            Path(html_file),    
            max_chars=15000,
        )
    )

    print(
        f"Raw HTML: {html_file}"
    )

    print(
        f"Reduced HTML: {reduced_file}"
    )


if __name__ == "__main__":
    main()