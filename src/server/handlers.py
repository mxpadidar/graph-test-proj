import asyncio
import json
import re

from server import errors


async def os_cmd_handler(payload: dict) -> str:
    """executes an OS command and returns the output."""

    cmd = payload.get("cmd")

    if not cmd:
        raise errors.MissingCmdError

    params = payload.get("params") or []

    try:
        process = await asyncio.create_subprocess_exec(
            cmd, *params, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
    except Exception:
        raise errors.InvalidCmdError

    if stderr:
        raise errors.InvalidCmdError

    return stdout.decode().strip()


def compute_cmd_handler(payload: dict) -> str:
    """evaluates a mathematical expression and returns the result."""

    if (expression := payload.get("expression")) is None:
        raise errors.MissingCmdError

    if re.search(r"[^0-9\+\-\*\/\(\)\s]", expression):
        raise errors.InvalidExpressionError

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        raise errors.InvalidExpressionError


async def process_message(msg: str) -> str:
    """processes a message based on its type
    and returns the response."""

    try:
        payload: dict = json.loads(msg)
    except json.JSONDecodeError:
        raise errors.InvalidMsgError

    match payload.get("type"):
        case "os":
            return await os_cmd_handler(payload)
        case "compute":
            return compute_cmd_handler(payload)
        case _:
            raise errors.InvalidCmdTypeError
