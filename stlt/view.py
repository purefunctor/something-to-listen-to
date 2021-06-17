"""Rich terminal frontend using `rich`."""
from __future__ import annotations

from datetime import timedelta
from shutil import get_terminal_size
import typing as t

import attr
from humanize import precisedelta  # type: ignore
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text

from stlt.config import StyleConfig


@attr.s
class _KvBuilder:
    """Helper class for building `rich` tables."""

    style: StyleConfig = attr.ib()
    truncate_width: int = attr.ib()
    _kvs: list[Text] = attr.ib(init=False, factory=list)

    def _surround_markup(self, text: str, surround: str) -> str:
        """Surround some `text` using console markup."""
        return f"[{surround}]{text}[/{surround}]"

    def append(self, lhs: str, rhs: str) -> None:
        """Append `lhs` and `rhs` to the current state."""
        _lhs = self._surround_markup(lhs, self.style.lhs_style)
        _rhs = self._surround_markup(rhs, self.style.rhs_style)

        text = Text.from_markup(f"{_lhs} {_rhs}")
        text.truncate(self.truncate_width, overflow="ellipsis")

        self._kvs.append(text)

    def create(self) -> Table:
        """Consume the current state and construct a `Table`."""
        view = Table(
            expand=True,
            box=getattr(box, self.style.box_style),
            style=self.style.box_color,
        )

        kvs = iter(self._kvs)
        view.add_column(next(kvs))
        for row in kvs:
            view.add_row(row)

        self.reset()

        return view

    def reset(self) -> None:
        """Reset the state."""
        self._kvs = []


@attr.s
class _ViewBuilder:
    """Helper class for building `rich` views of `Spotify` data."""

    style: StyleConfig = attr.ib()
    columns: int = attr.ib()

    _column_width: int = attr.ib(init=False)
    _kv_builder: _KvBuilder = attr.ib(init=False)

    _views: list = attr.ib(init=False, factory=list)

    def __attrs_post_init__(self) -> None:
        terminal_columns = get_terminal_size().columns
        self._column_width = terminal_columns // self.columns - 1
        self._kv_builder = _KvBuilder(self.style, self._column_width - 10)

    def append(self, kvs: t.Mapping[str, str]) -> None:
        """Append data to the current state."""
        for lhs, rhs in kvs.items():
            self._kv_builder.append(lhs, rhs)
        self._views.append(self._kv_builder.create())

    def create(self) -> Align:
        """Consume the current state and create an `Align`."""
        return Align(Columns(self._views, width=self._column_width), align="center")


def create_track_view(
    items: list[t.Mapping], style: StyleConfig, *, columns: int = 3
) -> Align:
    """Create a renderable view for tracks."""
    view_builder = _ViewBuilder(style, columns)

    for index, item in enumerate(items):
        track = item["track"]

        name = track["name"]
        artists = ", ".join([artist["name"] for artist in track["artists"]])
        duration = precisedelta(
            timedelta(milliseconds=track["duration_ms"]), format="%0.0f"
        )
        album = track["album"]["name"]

        view_builder.append(
            {
                f"{index}.": name,
                "Artists:": artists,
                "Duration:": duration,
                "Album:": album,
            }
        )

    return view_builder.create()


def create_album_view(
    items: list[t.Mapping], style: StyleConfig, *, columns: int = 3
) -> Align:
    """Create renderable views from albums."""
    view_builder = _ViewBuilder(style, columns)

    for index, item in enumerate(items):
        album = item["album"]

        name = album["name"]
        label = album["label"]
        artists = ", ".join([artist["name"] for artist in album["artists"]])
        tracks = str(len(album["tracks"]["items"]))
        release = album["release_date"]

        view_builder.append(
            {
                f"{index}.": name,
                "Label:": label,
                "Artists:": artists,
                "Tracks:": tracks,
                "Release:": release,
            }
        )

    return view_builder.create()
