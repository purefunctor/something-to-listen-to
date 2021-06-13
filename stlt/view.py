"""Rich terminal frontend using `rich`."""

from datetime import timedelta
import typing as t

from humanize import precisedelta
from rich import box
from rich.abc import RichRenderable
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text


def create_track_view(items: list[t.Mapping]) -> RichRenderable:
    """Create renderable views for tracks."""
    columns = []
    for index, item in enumerate(items):
        track = item["track"]
        table = Table(expand=True, box=box.SQUARE)
        name = track["name"]
        _name = Text(f"{name}")
        _name.truncate(25, overflow="ellipsis")
        table.add_column(Columns([Text(f"{index}."), _name]))
        artist = track["artists"][0]["name"]
        table.add_row(f"[bold]Artist:[/bold] {artist}")
        duration = timedelta(milliseconds=track["duration_ms"])
        duration = precisedelta(duration, format="%0.0f")
        table.add_row(f"[bold]Duration:[/bold] {duration}")
        album = track["album"]["name"]
        _album = Text("Album: ", style="bold").append_text(
            Text(album, style="not bold")
        )
        _album.truncate(25, overflow="ellipsis")
        table.add_row(_album)
        columns.append(table)
    return Align(Columns(columns, width=35), align="center")


def create_album_view(items: list[t.Mapping]) -> RichRenderable:
    """Create renderable views from albums."""
    columns = []
    for index, item in enumerate(items):
        album = item["album"]
        name = album["name"]
        label = album["label"]
        artist = album["artists"][0]["name"]
        table = Table(expand=True, box=box.SQUARE)
        _name = Text(name)
        _name.truncate(25, overflow="ellipsis")
        table.add_column(Columns([Text(f"{index}."), _name]))
        table.add_row(f"[bold]Label: [/bold] {label}")
        table.add_row(f"[bold]Artist: [/bold] {artist}")
        columns.append(table)
    return Align(Columns(columns, width=35), align="center")
