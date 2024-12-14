import pytest

from server.errors import InvalidCmdError, MissingCmdError
from server.handlers import os_cmd_handler


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"type": "os", "cmd": "pwd", "params": None},
        {"type": "os", "cmd": "ls", "params": ["-l"]},
        {"type": "os", "cmd": "echo", "params": "hello world"},
    ],
)
async def test_os_cmd_handler(payload: dict) -> None:
    result = await os_cmd_handler(payload)
    assert result
    assert isinstance(result, str)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"type": "os", "params": None},
        {"type": "os", "cmd": None, "params": []},
        {"type": "os"},
    ],
)
async def test_os_cmd_handler_missing_cmd(payload: dict) -> None:
    with pytest.raises(MissingCmdError):
        await os_cmd_handler(payload)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload",
    [
        {"type": "os", "cmd": "invalid", "params": None},
        {"type": "os", "cmd": "ls", "params": "invalid"},
    ],
)
async def test_os_cmd_handler_invalid_cmd(payload: dict) -> None:
    with pytest.raises(InvalidCmdError):
        await os_cmd_handler(payload)
