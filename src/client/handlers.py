import json

from zmq.asyncio import Socket

default_cmds = [
    {"type": "os", "cmd": "ls", "params": ["-l"]},
    {"type": "os", "cmd": "pwd", "params": None},
    {"type": "compute", "expression": "1 + 2"},
    {"type": "compute", "expression": "2 * 3"},
    {"type": "compute", "expression": "3 - 4"},
]


async def default_cmds_handler(skt: Socket, cmds: list[dict] = default_cmds) -> list[dict]:
    """sends a list of default commands to the server"""
    results = []
    for payload in cmds:
        msg = json.dumps(payload)
        await skt.send(msg.encode())
        replay = await skt.recv()
        results.append(replay.decode())
    return results


async def os_cmd_handler(skt: Socket, cmd: str) -> dict:
    """executes an OS command"""
    command, *params = cmd.split()
    payload = {"type": "os", "cmd": command, "params": params}
    msg = json.dumps(payload)
    await skt.send(msg.encode())
    replay = await skt.recv()
    return json.loads(replay.decode())


async def compute_cmd_handler(skt: Socket, expr: str) -> dict:
    """evaluates a mathematical expression"""
    payload = {"type": "compute", "expression": expr}
    msg = json.dumps(payload)
    await skt.send(msg.encode())
    replay = await skt.recv()
    return json.loads(replay.decode())
