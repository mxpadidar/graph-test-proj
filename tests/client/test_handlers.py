import json

import pytest

from client import handlers


@pytest.fixture
def resp() -> bytes:
    payload = {"status": "success"}
    json_payload = json.dumps(payload)
    return json_payload.encode()


@pytest.mark.asyncio
async def test_default_cmds_handler(skt) -> None:
    skt.recv.return_value = "response".encode()

    cmds = [{"type": "compute", "expression": "1 + 1"}, {"type": "os", "cmd": "echo", "params": "hello"}]
    results = await handlers.default_cmds_handler(skt=skt, cmds=cmds)
    assert results == ["response", "response"]
    assert skt.send.call_count == 2


@pytest.mark.asyncio
async def test_os_cmd_handler(skt, resp) -> None:
    skt.recv.return_value = resp
    cmd = "echo hello world"
    result = await handlers.os_cmd_handler(skt, cmd)
    assert result == json.loads(resp)


@pytest.mark.asyncio
async def test_compute_cmd_handler(skt, resp) -> None:
    skt.recv.return_value = resp
    expr = "1 + 2"
    result = await handlers.compute_cmd_handler(skt, expr)
    assert result == json.loads(resp)
