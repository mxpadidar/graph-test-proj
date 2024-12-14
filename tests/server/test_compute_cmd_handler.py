import pytest

from server.errors import InvalidExpressionError, MissingCmdError
from server.handlers import compute_cmd_handler


@pytest.mark.parametrize(
    "payload, expected_result",
    [
        ({"type": "compute", "expression": "1 + 1"}, str(1 + 1)),
        ({"type": "compute", "expression": "2 * 3"}, str(2 * 3)),
        ({"type": "compute", "expression": "(4 / 2) + 3"}, str(4 / 2 + 3)),
    ],
)
def test_compute_cmd_handler(payload: dict, expected_result: int) -> None:
    result = compute_cmd_handler(payload)
    assert result == expected_result


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "compute", "expression": None},
        {"type": "compute"},
    ],
)
def test_compute_cmd_handler_missing_expression(payload: dict) -> None:
    with pytest.raises(MissingCmdError):
        compute_cmd_handler(payload)


@pytest.mark.parametrize(
    "payload",
    [
        {"type": "compute", "expression": "1 + 1; import os"},
        {"type": "compute", "expression": "2 * 3; os.system('ls')"},
        {"type": "compute", "expression": "4 / 2 + 'a'"},
    ],
)
def test_compute_cmd_handler_invalid_expression(payload: dict) -> None:
    with pytest.raises(InvalidExpressionError):
        compute_cmd_handler(payload)
