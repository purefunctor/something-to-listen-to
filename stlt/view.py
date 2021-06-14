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


def create_track_view(items: list[t.Mapping], *, columns: int = 3) -> Align:
    """Create a renderable view for tracks."""
    term_cols, _ = get_terminal_size()

    column_width = term_cols // columns - 1
    truncate_width = column_width - 10

    views = []
    for index, item in enumerate(items):
        track = item["track"]

        _name = Text.from_markup(f"[white not bold]{track['name']}[/white not bold]")
        _name.truncate(truncate_width, overflow="ellipsis")
        name = Columns(
            [
                f"[blue]{index}.[/blue]",
                _name,
            ]
        )

        _artists = ", ".join(artist["name"] for artist in track["artists"])
        artists = Text.from_markup(
            f"[blue bold]Artists:[/blue bold] [white]{_artists}[/white]"
        )
        artists.truncate(truncate_width, overflow="ellipsis")

        _duration = precisedelta(
            timedelta(milliseconds=track["duration_ms"]),
            format="%0.0f",
        )
        duration = Text.from_markup(
            f"[bold blue]Duration:[/bold blue] [white]{_duration}[/white]"
        )

        _album = track["album"]["name"]
        album = Text.from_markup(
            f"[blue bold]Album:[/blue bold] [white]{_album}[/white]"
        )
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

        _name = Text.from_markup(f"[white not bold]{album['name']}[/white not bold]")
        _name.truncate(truncate_width, overflow="ellipsis")
        name = Columns(
            [
                f"[blue]{index}.[/blue]",
                _name,
            ]
        )

        _label = album["label"]
        label = Text.from_markup(
            f"[blue bold]Label:[/blue bold] [white]{_label}[/white]"
        )
        label.truncate(truncate_width, overflow="ellipsis")

        _artists = ", ".join(artist["name"] for artist in album["artists"])
        artists = Text.from_markup(
            f"[blue bold]Artists:[/blue bold] [white]{_artists}[/white]"
        )
        artists.truncate(truncate_width, overflow="ellipsis")

        _tracks = len(album["tracks"]["items"])
        tracks = Text.from_markup(
            f"[blue bold]Tracks:[/blue bold] [white]{_tracks}[/white]"
        )

        _release_date = album["release_date"]
        release_date = Text.from_markup(
            f"[blue bold]Release:[/blue bold] [white]{_release_date}[/white]"
        )

        view = Table(expand=True, box=box.SIMPLE_HEAD, style="green")

        view.add_column(name)
        view.add_row(label)
        view.add_row(artists)
        view.add_row(tracks)
        view.add_row(release_date)

        views.append(view)

    return Align(Columns(views, width=column_width), align="center")
