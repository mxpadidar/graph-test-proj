from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def skt() -> AsyncMock:
    skt = AsyncMock()
    skt.send = AsyncMock()
    skt.recv = AsyncMock()
    return skt
