"""Tests for the top-level `stlt` package."""
from stlt import __version__


def test_stlt() -> None:
    """Test the `__version__` constant."""
    assert __version__ == "0.1.0"
