"""Reading and writing user configuration and secrets."""
from __future__ import annotations

from abc import ABC
from importlib import resources
from pathlib import Path
import typing as t

import attr
import toml

from stlt import assets
from stlt.errors import ConfigError


DEFAULT_CONFIG_FILE = toml.loads(resources.read_text(assets, "config.toml"))


_FromTomlType = t.TypeVar("_FromTomlType", bound="_FromToml")


class _FromToml(ABC):
    """Implements deserialization from `toml` into `attrs`."""

    def __init__(self, *args: t.Any, **kwargs: t.Any) -> None:  # pragma: no cover
        ...

    @classmethod
    def from_dict(cls: t.Type[_FromTomlType], data: t.Mapping) -> _FromTomlType:
        """Deserialize some `data` into an `attrs`-based `cls`."""
        kwargs = {}

        for field in attr.fields(cls):
            name = field.name
            meta = field.metadata

            try:
                if section := meta.get("section", False):
                    kwargs[name] = _nested_get(data, section)
                else:
                    kwargs[name] = data[name]
            except KeyError as e:
                if "section" in meta:
                    err = f"Missing required section {e.args[0]}"
                else:
                    err = f"Missing required key {name}"
                raise ConfigError(err)

            if builder := meta.get("builder", False):
                kwargs[name] = builder(kwargs[name])

        return cls(**kwargs)


@attr.s(slots=True)
class OAuthConfig(_FromToml):
    """Configuration data class for `SpotifyOAuth`."""

    client_id: str = attr.ib()
    client_secret: str = attr.ib()
    redirect_uri: str = attr.ib()
    scope: str = attr.ib()


@attr.s
class CacheConfig(_FromToml):
    """Configuration data class for the cache."""

    auth_cache: Path = attr.ib(converter=Path)


@attr.s(slots=True)
class Config(_FromToml):
    """Configuration data class for the project."""

    oauth: OAuthConfig = attr.ib(
        metadata={"section": ["oauth"], "builder": OAuthConfig.from_dict}
    )

    cache: CacheConfig = attr.ib(
        metadata={"section": ["cache"], "builder": CacheConfig.from_dict}
    )


def ensure_config(config: Path) -> None:
    """Ensure that the `config` file exists and is valid."""
    config.parent.mkdir(parents=True, exist_ok=True)

    if config.exists():
        return None

    with config.open("w") as f:
        toml.dump(DEFAULT_CONFIG_FILE, f)


def load_config(config: Path) -> t.Mapping:
    """Deserialize the `config` file into a `Mapping`."""
    ensure_config(config)
    return toml.load(config)


def _nested_get(mapping: t.Mapping[str, t.Any], keys: list[str]) -> t.Any:
    current = mapping
    for key in keys:
        current = current[key]
    return current
