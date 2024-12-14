import json

import pytest

from server.errors import InvalidCmdTypeError, InvalidMsgError, MissingCmdError
from server.handlers import process_message


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "payload, expected_result",
    [
        ({"type": "os", "cmd": "echo", "params": ["hello world"]}, "hello world"),
        ({"type": "compute", "expression": "1 + 2"}, "3"),
    ],
)
async def test_handle_message_valid(payload: dict, expected_result: str) -> None:
    msg = json.dumps(payload)
    result = await process_message(msg)
    assert isinstance(result, str)
    assert result == expected_result


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "msg",
    ['{"type": "os", "params": None}', '{"type": "compute"}', '{"type": "invalid"}', "invalid json"],
)
async def test_handle_message_invalid(msg: str) -> None:
    with pytest.raises((InvalidMsgError, MissingCmdError, InvalidCmdTypeError)):
        await process_message(msg)
