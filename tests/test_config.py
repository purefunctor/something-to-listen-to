"""Tests for the `stlt.config` module."""
from pathlib import Path

import pytest
import toml

from stlt.config import (
    Config,
    EMPTY_CONFIG_FILE,
    ensure_config,
    load_config,
    OAuthConfig,
)
from stlt.errors import ConfigError


@pytest.fixture
def path(tmp_path: Path) -> Path:
    """Fixture for the configuration file."""
    return tmp_path / ".config" / "config.toml"


class TestEnsureConfig:
    """Tests for the `ensure_config` function."""

    def test_creates_a_placeholder_configuration_file(self, path: Path) -> None:
        """Test whether `ensure_config` creates a placeholder file."""
        ensure_config(path)

        assert toml.load(path) == EMPTY_CONFIG_FILE

    def test_creates_parent_folders(self, path: Path) -> None:
        """Test whether `ensure_config` creates parent directories."""
        ensure_config(path)

        assert path.parent.exists()


class TestLoadConfig:
    """Tests for the `load_config` function."""

    def test_loads_a_placeholder_configuration_file(self, path: Path) -> None:
        """Test whether `load_config` returns a placeholder file."""
        assert load_config(path) == EMPTY_CONFIG_FILE


class TestOAuthConfig:
    """Tests for the `OAuthConfig` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `OAuthConfig.from_dict`."""
        expected = OAuthConfig(**EMPTY_CONFIG_FILE["oauth"])

        assert OAuthConfig.from_dict(EMPTY_CONFIG_FILE["oauth"]) == expected

    def test_from_dict_fails_on_missing_keys(self, path: Path) -> None:
        """Test invalid serialization with `OAuthConfig.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required key"):
            OAuthConfig.from_dict({})


class TestConfig:
    """Tests for the `Config` class."""

    def test_from_dict_parses_a_valid_mapping(self, path: Path) -> None:
        """Test valid serialization with `Config.from_dict`."""
        expected = Config(oauth=OAuthConfig.from_dict(EMPTY_CONFIG_FILE["oauth"]))

        assert Config.from_dict(EMPTY_CONFIG_FILE) == expected

    def test_from_dict_fails_on_missing_sections(self, path: Path) -> None:
        """Test invalid serialization with `Config.from_dict`."""
        with pytest.raises(ConfigError, match="Missing required section"):
            Config.from_dict({})
