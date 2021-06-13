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
    """Create a renderable view for tracks."""
    views = []
    for index, item in enumerate(items):
        track = item["track"]

        _name = Text(track["name"])
        _name.truncate(25, overflow="ellipsis")
        name = Columns(
            [
                Text(f"{index}."),
                _name,
            ]
        )

        _artists = ", ".join(artist["name"] for artist in track["artists"])
        artists = Text("Artists:", style="bold").append_text(
            Text(f" {_artists}", style="not bold")
        )
        artists.truncate(25, overflow="ellipsis")

        _duration = precisedelta(
            timedelta(milliseconds=track["duration_ms"]),
            format="%0.0f",
        )
        duration = f"[bold]Duration:[/bold] {_duration}"

        _album = track["album"]["name"]
        album = Text("Album:", style="bold").append_text(
            Text(f" {_album}", style="not bold")
        )
        album.truncate(25, overflow="ellipsis")

        view = Table(expand=True, box=box.SQUARE)

        view.add_column(name)
        view.add_row(artists)
        view.add_row(duration)
        view.add_row(album)

        views.append(view)

    return Align(Columns(views, width=35), align="center")


def create_album_view(items: list[t.Mapping]) -> RichRenderable:
    """Create renderable views from albums."""
    views = []
    for index, item in enumerate(items):
        album = item["album"]

        _name = Text(album["name"])
        _name.truncate(25, overflow="ellipsis")
        name = Columns([
            Text(f"{index}."),
            _name
        ])

        _label = album["label"]
        label = Text("Label:", style="bold").append_text(
            Text(f" {_label}", style="not bold")
        )
        label.truncate(25, overflow="ellipsis")

        _artists = ", ".join(artist["name"] for artist in album["artists"])
        artists = Text("Artists:", style="bold").append_text(
            Text(f" {_artists}", style="not bold")
        )
        artists.truncate(25, overflow="ellipsis")

        view = Table(expand=True, box=box.SQUARE)

        view.add_column(name)
        view.add_row(label)
        view.add_row(artists)

        views.append(view)

    return Align(Columns(views, width=35), align="center")
