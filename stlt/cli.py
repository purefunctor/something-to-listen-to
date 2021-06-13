"""Command-line interface using `click`."""

from pathlib import Path

import attr
import click
from rich import print
from spotipy import Spotify  # type: ignore
from spotipy.cache_handler import CacheFileHandler  # type: ignore
from spotipy.oauth2 import SpotifyOAuth  # type: ignore

from stlt.config import load_config
from stlt.constants import CONFIG_FILE_PATH
from stlt.view import create_album_view, create_track_view


pass_spotify = click.make_pass_decorator(Spotify)


@click.group(
    name="stlt", help="A command-line tool for getting songs to listen to in Spotify."
)
@click.option(
    "--config-file",
    default=CONFIG_FILE_PATH,
    help=f"Override the default config file path ({CONFIG_FILE_PATH}).",
    type=Path,
)
@click.pass_context
def stlt(context: click.Context, config_file: Path) -> None:  # noqa: D103
    # Ensure that no side-effects are run
    # when no subcommand is invoked.
    if context.invoked_subcommand is None:
        return None

    context.ensure_object(dict)
    config = load_config(config_file)
    context.obj = Spotify(
        auth_manager=SpotifyOAuth(
            **attr.asdict(config.oauth),
            cache_handler=CacheFileHandler(config.cache.auth_cache),
        )
    )


@stlt.group(name="saved")
@pass_spotify
def saved(client: Spotify) -> None:
    """Query the user's saved items."""


@saved.command(name="albums")
@click.option("-l", "--limit", default=20)
@click.option("-c", "--columns", default=3)
@pass_spotify
def saved_albums(client: Spotify, limit: int, columns: int) -> None:
    """List the user's saved albums."""
    response = client.current_user_saved_albums(limit=limit)
    print(create_album_view(response["items"], columns=columns))


@saved.command(name="tracks")
@click.option("-l", "--limit", default=20)
@click.option("-c", "--columns", default=3)
@pass_spotify
def saved_tracks(client: Spotify, limit: int, columns: int) -> None:
    """List the user's saved tracks."""
    response = client.current_user_saved_tracks(limit=limit)
    print(create_track_view(response["items"], columns=columns))


@stlt.command(name="login")
@pass_spotify
def login(client: Spotify) -> None:
    """Log in using Spotify OAuth."""
    if client.auth_manager.cache_handler.get_cached_token() is not None:
        click.echo("Logged in!")
    else:
        click.echo("Logging you in...")
        client.auth_manager.get_access_token()
