"""Tests for the `rich` rendering functions."""

from pytest_mock import MockerFixture
from rich.align import Align
from rich.columns import Columns

from stlt.config import Config, DEFAULT_CONFIG_FILE
from stlt.view import create_album_view, create_track_view


def test_create_album_view(mocker: MockerFixture) -> None:
    """Test album view creation."""
    items = [
        mocker.MagicMock(),
        mocker.MagicMock(),
    ]
    style = Config.from_dict(DEFAULT_CONFIG_FILE).style

    result = create_album_view(items, style)

    assert isinstance(result, Align)
    assert result.align == "center"
    assert isinstance(result.renderable, Columns)
    assert len(result.renderable.renderables) == len(items)


def test_create_track_view(mocker: MockerFixture) -> None:
    """Test track view creation."""
    # `timedelta` doesn't like `MagicMock`
    mocker.patch("stlt.view.timedelta")

    items = [
        mocker.MagicMock(),
        mocker.MagicMock(),
    ]
    style = Config.from_dict(DEFAULT_CONFIG_FILE).style

    result = create_track_view(items, style)

    assert isinstance(result, Align)
    assert result.align == "center"
    assert isinstance(result.renderable, Columns)
    assert len(result.renderable.renderables) == len(items)
