"""Reading and writing user configuration and secrets."""
from __future__ import annotations

from importlib import resources
from pathlib import Path
import typing as t

import attr
import toml

from stlt import assets
from stlt.errors import ConfigError


EMPTY_CONFIG_FILE = toml.loads(resources.read_text(assets, "config.toml"))


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
                err = f"Missing required key '{name}'"
                raise ConfigError(err) from None
        return cls(**fields)


@attr.s(slots=True)
class Config:
    """Configuration data class for the project."""

    oauth: OAuthConfig = attr.ib(
        metadata={"section": ["oauth"], "builder": OAuthConfig.from_dict}
    )

    @classmethod
    def from_dict(cls, data: t.Mapping) -> Config:
        """Create a `Config` from a `toml`-based mapping."""
        sections = {}
        for field in attr.fields(cls):
            name = field.name
            meta = field.metadata
            builder = meta["builder"]
            section = meta["section"]
            try:
                sections[name] = builder(_nested_get(data, section))
            except KeyError as e:
                err = f"Missing required section '{e.args[0]}'"
                raise ConfigError(err) from None
        return cls(**sections)


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


def _nested_get(mapping: t.Mapping[str, t.Any], keys: list[str]) -> t.Any:
    current = mapping
    for key in keys:
        current = current[key]
    return current
