"""Tests for the command-line interface."""

from pathlib import Path
from typing import Optional

from click.testing import CliRunner
import pytest
from pytest_mock import MockerFixture
from spotipy import Spotify  # type: ignore
import toml

from stlt.cli import stlt
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


class TestStlt:
    """Tests for the top-level command."""

    def test_no_side_effects_run(
        self, mocker: MockerFixture, runner: CliRunner
    ) -> None:
        """Test side effects if present."""
        fake_config = mocker.Mock(spec=Config)
        fake_load_config = mocker.patch(
            "stlt.cli.load_config", return_value=fake_config
        )

        result = runner.invoke(stlt)

        assert result.exit_code == 0
        assert result.output != ""
        fake_load_config.assert_not_called()

    def test_overrides_default_config_file(
        self, mocker: MockerFixture, runner: CliRunner, config: Path
    ) -> None:
        """Test override for default config file."""
        fake_config = Config.from_dict(DEFAULT_CONFIG_FILE)
        fake_load_config = mocker.patch("stlt.cli.load_config")
        fake_load_config.return_value = fake_config

        @stlt.command()
        def debug() -> None:
            """Force a command group to be executed."""
            print("debug")

        result = runner.invoke(stlt, ["--config-file", str(config), "debug"])

        assert result.exit_code == 0
        assert result.output == "debug\n"
        fake_load_config.assert_called_once_with(config)


class TestSaved:
    """Tests for the `saved` command group."""

    def create_client(self, mocker: MockerFixture) -> Spotify:
        """Create a mocked client."""
        client = mocker.Mock(spec=Spotify)
        mocker.patch("stlt.cli.Spotify", return_value=client)
        return client

    def test_saved_albums(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test query for saved albums."""
        client = self.create_client(mocker)
        client.current_user_saved_albums.return_value = mocker.MagicMock(spec=dict)
        mocker.patch("stlt.cli.create_album_view", return_value="debug")
        mocker.patch(
            "stlt.cli.load_config", return_value=Config.from_dict(DEFAULT_CONFIG_FILE)
        )

        result = runner.invoke(stlt, ["saved", "albums"])

        assert result.exit_code == 0
        assert result.stdout == "debug\n"

    def test_saved_tracks(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test query for saved tracks."""
        client = self.create_client(mocker)
        client.current_user_saved_tracks = mocker.MagicMock(spec=dict)
        mocker.patch("stlt.cli.create_track_view", return_value="debug")
        mocker.patch(
            "stlt.cli.load_config", return_value=Config.from_dict(DEFAULT_CONFIG_FILE)
        )

        result = runner.invoke(stlt, ["saved", "tracks"])

        assert result.exit_code == 0
        assert result.stdout == "debug\n"


class TestLogin:
    """Tests for auth-related commands."""

    def create_client(self, mocker: MockerFixture, token: Optional[str]) -> Spotify:
        """Create a mocked client."""
        client = mocker.Mock(spec=Spotify)
        mocker.patch("stlt.cli.Spotify", return_value=client)
        client.auth_manager.cache_handler.get_cached_token.return_value = token
        return client

    def test_login_fresh(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test fresh logins."""
        client = self.create_client(mocker, None)
        mocker.patch(
            "stlt.cli.load_config", return_value=Config.from_dict(DEFAULT_CONFIG_FILE)
        )

        result = runner.invoke(stlt, ["login"])

        assert result.exit_code == 0
        assert result.output != ""
        client.auth_manager.get_access_token.assert_called_once()

    def test_login_cached(self, mocker: MockerFixture, runner: CliRunner) -> None:
        """Test cached logins."""
        self.create_client(mocker, "token")
        mocker.patch(
            "stlt.cli.load_config", return_value=Config.from_dict(DEFAULT_CONFIG_FILE)
        )

        result = runner.invoke(stlt, ["login"])

        assert result.exit_code == 0
        assert result.output != ""
