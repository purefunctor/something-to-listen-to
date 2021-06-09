import pytest
import toml

from stlt.config import (
    Config,
    EMPTY_CONFIG_FILE,
    OAuthConfig,
    ensure_config,
    load_config,
)
from stlt.errors import ConfigError


@pytest.fixture
def path(tmp_path):
    return tmp_path / ".config" / "config.toml"


class TestEnsureConfig:
    def test_creates_a_placeholder_configuration_file(self, path):
        ensure_config(path)

        assert toml.load(path) == EMPTY_CONFIG_FILE

    def test_creates_parent_folders(self, path):
        ensure_config(path)

        assert path.parent.exists()


class TestLoadConfig:
    def test_loads_a_placeholder_configuration_file(self, path):
        assert load_config(path) == EMPTY_CONFIG_FILE


class TestOAuthConfig:
    def test_from_dict_parses_a_valid_mapping(self, path):
        expected = OAuthConfig(**EMPTY_CONFIG_FILE["oauth"])

        assert OAuthConfig.from_dict(EMPTY_CONFIG_FILE["oauth"]) == expected

    def test_from_dict_fails_on_missing_keys(self, path):
        with pytest.raises(ConfigError, match="Missing required key"):
            OAuthConfig.from_dict({})


class TestConfig:
    def test_from_dict_parses_a_valid_mapping(self, path):
        expected = Config(oauth=OAuthConfig.from_dict(EMPTY_CONFIG_FILE["oauth"]))

        assert Config.from_dict(EMPTY_CONFIG_FILE) == expected

    def test_from_dict_fails_on_missing_sections(self, path):
        with pytest.raises(ConfigError, match="Missing required section"):
            Config.from_dict({})
