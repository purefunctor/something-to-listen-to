"""Reading and writing user configuration and secrets."""
from __future__ import annotations

from pathlib import Path
import typing as t

import attr
import toml

from stlt.errors import ConfigError


EMPTY_CONFIG_FILE = {
    "oauth": {
        "client_id": "CLIENT_ID",
        "client_secret": "CLIENT_SECRET",
        "redirect_uri": "REDIRECT_URI",
        "scope": "SCOPE",
    }
}


@attr.s(slots=True)
class OAuthConfig:
    """Configuration data class for `SpotifyOAuth`."""

    client_id: str = attr.ib()
    client_secret: str = attr.ib()
    redirect_uri: str = attr.ib()
    scope: str = attr.ib()

    @classmethod
    def from_dict(cls, data: t.Mapping) -> OAuthConfig:
        """Create an `OAuthConfig` from a `toml`-based mapping."""
        fields = {}
        for field in attr.fields(cls):
            name = field.name
            try:
                fields[name] = data[name]
            except KeyError:
                raise ConfigError(f"Missing required key '{name}'") from None
        return cls(**fields)


@attr.s(slots=True)
class Config:
    """Configuration data class for the project."""

    oauth: OAuthConfig = attr.ib()

    @classmethod
    def from_dict(cls, data: t.Mapping) -> Config:
        """Create a `Config` from a `toml`-based mapping."""
        builders = {
            "oauth": OAuthConfig.from_dict,
        }
        fields = {}
        for field in attr.fields(cls):
            name = field.name
            try:
                fields[name] = builders[name](data[name])
            except KeyError:
                raise ConfigError(f"Missing required section '{name}'") from None
        return cls(**fields)


def ensure_config(config: Path) -> None:
    """Ensure that the `config` file exists and is valid."""
    config.parent.mkdir(parents=True, exist_ok=True)

    if config.exists():
        return None

    with config.open("w") as f:
        toml.dump(EMPTY_CONFIG_FILE, f)


def load_config(config: Path) -> t.Mapping:
    """Deserialize the `config` file into a `Mapping`."""
    ensure_config(config)
    return toml.load(config)
