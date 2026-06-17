import pytest

from config.config_loader import ConfigLoader


def test_valid_config_loads():
    config = ConfigLoader.load(
        "configs/search_config.json"
    )

    assert config.start_url is not None
    assert len(config.fields) > 0


def test_missing_file():
    with pytest.raises(FileNotFoundError):
        ConfigLoader.load(
            "configs/not_found.json"
        )


def test_invalid_url():
    pass


def test_empty_fields():
    pass


def test_missing_fields():
    pass