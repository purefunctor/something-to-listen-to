"""Rich terminal frontend using `rich`."""

from datetime import timedelta
from shutil import get_terminal_size
import typing as t

from humanize import precisedelta  # type: ignore
from rich import box
from rich.align import Align
from rich.columns import Columns
from rich.table import Table
from rich.text import Text


def create_text(lhs: str, rhs: str, lhs_style: str, rhs_style: str) -> Text:
    """Create text to be used for views."""
    return Text.from_markup(
        f"[{lhs_style}]{lhs}[/{lhs_style}] [{rhs_style}]{rhs}[/{rhs_style}]"
    )


def create_track_view(items: list[t.Mapping], *, columns: int = 3) -> Align:
    """Create a renderable view for tracks."""
    term_cols, _ = get_terminal_size()

    column_width = term_cols // columns - 1
    truncate_width = column_width - 10

    views = []
    for index, item in enumerate(items):
        track = item["track"]

        _name = track["name"]
        name = create_text(f"{index}.", _name, "blue", "white not bold")
        name.truncate(truncate_width, overflow="ellipsis")

        _artists = ", ".join(artist["name"] for artist in track["artists"])
        artists = create_text("Artists:", _artists, "blue bold", "white")
        artists.truncate(truncate_width, overflow="ellipsis")

        _duration = precisedelta(
            timedelta(milliseconds=track["duration_ms"]),
            format="%0.0f",
        )
        duration = create_text("Duration:", _duration, "blue bold", "white")

        _album = track["album"]["name"]
        album = create_text("Album:", _album, "blue bold", "white")
        album.truncate(truncate_width, overflow="ellipsis")

        view = Table(expand=True, box=box.SIMPLE_HEAD, style="green")

        view.add_column(name)
        view.add_row(artists)
        view.add_row(duration)
        view.add_row(album)

        views.append(view)

    return Align(Columns(views, width=column_width), align="center")


def create_album_view(items: list[t.Mapping], *, columns: int = 3) -> Align:
    """Create renderable views from albums."""
    term_cols, _ = get_terminal_size()

    column_width = term_cols // columns - 1
    truncate_width = column_width - 10

    views = []
    for index, item in enumerate(items):
        album = item["album"]

        _name = album["name"]
        name = create_text(f"{index}.", _name, "blue", "white not bold")
        name.truncate(truncate_width, overflow="ellipsis")

        _label = album["label"]
        label = create_text("Label:", _label, "blue bold", "white")
        label.truncate(truncate_width, overflow="ellipsis")

        _artists = ", ".join(artist["name"] for artist in album["artists"])
        artists = create_text("Artists:", _artists, "blue bold", "white")
        artists.truncate(truncate_width, overflow="ellipsis")

        _tracks = len(album["tracks"]["items"])
        tracks = create_text("Tracks:", str(_tracks), "blue bold", "white")
        tracks.truncate(truncate_width, overflow="ellipsis")

        _release_date = album["release_date"]
        release_date = create_text("Release:", _release_date, "blue bold", "white")
        release_date.truncate(truncate_width, overflow="ellipsis")

        view = Table(expand=True, box=box.SIMPLE_HEAD, style="green")

        view.add_column(name)
        view.add_row(label)
        view.add_row(artists)
        view.add_row(tracks)
        view.add_row(release_date)

        views.append(view)

    return Align(Columns(views, width=column_width), align="center")
