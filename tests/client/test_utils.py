import pytest

from client.custom_types import Reader, Writer
from client.utils import menu


@pytest.fixture
def writer() -> Writer:
    """mocked writer"""
    return lambda x: None


@pytest.fixture
def reader() -> Reader:
    """mocked reader"""
    return lambda x: "1"


def test_menu(reader, writer) -> None:
    choice = menu(reader, writer)
    assert choice == "os"
