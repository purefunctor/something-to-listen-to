"""Tests for the `stlt.config` module."""
from pathlib import Path

import pytest
import toml

from stlt.config import (
    CacheConfig,
    Config,
    DEFAULT_CONFIG_FILE,
    ensure_config,
    load_config,
    OAuthConfig,
    StyleConfig,
)
from stlt.errors import ConfigError


@pytest.fixture
def path(tmp_path: Path) -> Path:
    """Fixture for the configuration file."""
    return tmp_path / ".config" / "config.toml"


class TestEnsureConfig:
    """Tests for the `ensure_config` function."""

    def test_creates_a_placeholder_configuration_file(self, path: Path) -> None:
        """Test if a placeholder is created."""
        ensure_config(path)

        assert toml.load(path) == DEFAULT_CONFIG_FILE

    def test_creates_parent_folders(self, path: Path) -> None:
        """Test if parent directories are created."""
        ensure_config(path)

        assert path.parent.exists()

    def test_does_not_override_existing_configuration(self, path: Path) -> None:
        """Test if existing configuration files are preserved."""
        config = {**DEFAULT_CONFIG_FILE}
        config["oauth"]["scope"] = "user-library-read"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w") as f:
            toml.dump(config, f)

        ensure_config(path)

        with path.open("r") as f:
            assert toml.load(f) == config


class TestLoadConfig:
    """Tests for the `load_config` function."""

    def test_loads_a_placeholder_configuration_file(self, path: Path) -> None:
        """Test if a placeholder file is returned."""
        assert load_config(path) == Config.from_dict(DEFAULT_CONFIG_FILE)


class TestOAuthConfig:
    """Tests for the `OAuthConfig` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `OAuthConfig.from_dict`."""
        expected = OAuthConfig(**DEFAULT_CONFIG_FILE["oauth"])

        assert OAuthConfig.from_dict(DEFAULT_CONFIG_FILE["oauth"]) == expected

    def test_from_dict_fails_on_missing_keys(self, path: Path) -> None:
        """Test invalid serialization with `OAuthConfig.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required key"):
            OAuthConfig.from_dict({})


class TestCacheConfig:
    """Test for the `CacheConfig` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `CacheConfig.from_dict`."""
        expected = CacheConfig(**DEFAULT_CONFIG_FILE["cache"])

        assert CacheConfig.from_dict(DEFAULT_CONFIG_FILE["cache"]) == expected

    def test_from_dict_fails_on_missing_keys(self, path: Path) -> None:
        """Test invalid serialization with `CacheConfig.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required key"):
            CacheConfig.from_dict({})


class TestStyleConfig:
    """Tests for the `StyleConfig` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `StyleConfig.from_dict`."""
        expected = StyleConfig(**DEFAULT_CONFIG_FILE["style"])

        assert StyleConfig.from_dict(DEFAULT_CONFIG_FILE["style"]) == expected

    def test_from_dict_fails_on_missing_keys(self, path: Path) -> None:
        """Test invalid serialization with `CacheConfig.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required key"):
            StyleConfig.from_dict({})


class TestConfig:
    """Tests for the `Config` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `Config.from_dict`."""
        expected = Config(
            oauth=OAuthConfig(**DEFAULT_CONFIG_FILE["oauth"]),
            cache=CacheConfig(**DEFAULT_CONFIG_FILE["cache"]),
            style=StyleConfig(**DEFAULT_CONFIG_FILE["style"]),
        )

        assert Config.from_dict(DEFAULT_CONFIG_FILE) == expected

    def test_from_dict_fails_on_missing_sections(self, path: Path) -> None:
        """Test invalid serialization with `Config.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required section"):
            Config.from_dict({})
