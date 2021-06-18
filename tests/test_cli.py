"""Tests for the command-line interface."""

from pathlib import Path
from unittest.mock import Mock

from click.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
from spotipy import Spotify  # type: ignore
import toml

from stlt.cli import Context, stlt
from stlt.config import Config, DEFAULT_CONFIG_FILE


@pytest.fixture
def config(tmp_path: Path) -> Path:
    """Fixture for the config `Path`."""
    _config = tmp_path / "config.toml"
    with _config.open("w") as f:
        toml.dump(DEFAULT_CONFIG_FILE, f)
    return _config


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for the `CliRunner`."""
    return CliRunner()


class TestContext:
    """Tests for the top-level context."""

    def create_context(self, mocker: MockerFixture) -> Context:
        """Create a mocked `Context`."""
        client = mocker.Mock(spec=Spotify)
        config = mocker.Mock(spec=Config)
        return Context(client, config)

    def test_saved_albums(self, mocker: MockerFixture) -> None:
        """Test queries for saved albums."""
        context = self.create_context(mocker)
        context.client.current_user_saved_albums.return_value = mocker.MagicMock(
            spec=dict
        )
        albums = mocker.patch("stlt.cli.create_album_view").return_value
        rprint = mocker.patch("stlt.cli.print")

        context.saved_albums(limit=-1, columns=-1)

        rprint.assert_called_once_with(albums)

    def test_saved_tracks(self, mocker: MockerFixture) -> None:
        """Test queries for saved tracks."""
        context = self.create_context(mocker)
        context.client.current_user_saved_tracks.return_value = mocker.MagicMock(
            spec=dict
        )
        tracks = mocker.patch("stlt.cli.create_track_view").return_value
        rprint = mocker.patch("stlt.cli.print")

        context.saved_tracks(limit=-1, columns=-1)

        rprint.assert_called_once_with(tracks)

    def test_login_cached(self, mocker: MockerFixture) -> None:
        """Test cached logins."""
        context = self.create_context(mocker)
        auth_manager = context.client.auth_manager
        cache_handler = auth_manager.cache_handler
        cache_handler.get_cached_token.return_value = "token"
        rprint = mocker.patch("stlt.cli.print")

        context.login()

        rprint.assert_called_once()

    def test_login_fresh(self, mocker: MockerFixture) -> None:
        """Test fresh logins."""
        context = self.create_context(mocker)
        auth_manager = context.client.auth_manager
        cache_handler = auth_manager.cache_handler
        cache_handler.get_cached_token.return_value = None
        rprint = mocker.patch("stlt.cli.print")

        context.login()

        rprint.assert_called_once()
        auth_manager.get_access_token.assert_called_once()


class TestStlt:
    """Tests for the top-level command."""

    def test_no_side_effects_run(
        self, mocker: MockerFixture, runner: CliRunner
    ) -> None:
        """Test side effects if present."""
        load_config = mocker.patch("stlt.cli.load_config")

        result = runner.invoke(stlt)

        assert result.exit_code == 0
        assert result.output != ""
        load_config.assert_not_called()

    def test_overrides_default_config_file(
        self, mocker: MockerFixture, runner: CliRunner, config: Path
    ) -> None:
        """Test override for default config file."""
        configuration = Config.from_dict(DEFAULT_CONFIG_FILE)
        load_config = mocker.patch("stlt.cli.load_config", return_value=configuration)

        @stlt.command()
        def debug() -> None:
            """Force a command group to be executed."""
            print("debug")

        result = runner.invoke(stlt, ["--config-file", str(config), "debug"])

        assert result.exit_code == 0
        assert result.output == "debug\n"
        load_config.assert_called_once_with(config)


class ContextualTest:
    """Helper class for mocking contexts."""

    def create_context(self, mocker: MockerFixture) -> Mock:
        """Create a mocked `Context`."""
        context = mocker.Mock(spec=Context)
        context.client = mocker.Mock(spec=Spotify)
        context.config = mocker.Mock(spec=Config)
        mocker.patch("stlt.cli.Context", return_value=context)
        return context


class TestSaved(ContextualTest):
    """Tests for the `saved` command group."""

    def test_saved_albums(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test the `albums` subcommand."""
        context = self.create_context(mocker)

        result = runner.invoke(stlt, ["saved", "albums"])

        assert result.exit_code == 0
        assert result.stdout == ""
        context.saved_albums.assert_called_once()

    def test_saved_tracks(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test the `tracks` subcommand."""
        context = self.create_context(mocker)

        result = runner.invoke(stlt, ["saved", "tracks"])

        assert result.exit_code == 0
        assert result.stdout == ""
        context.saved_tracks.assert_called_once()


class TestLogin(ContextualTest):
    """Tests for auth-related commands."""

    def test_login(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test the `login` command."""
        self.create_context(mocker)

        result = runner.invoke(stlt, ["login"])

        assert result.exit_code == 0
        assert result.output == ""
