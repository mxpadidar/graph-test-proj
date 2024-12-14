import zmq
from zmq.asyncio import Context

from client import handlers, utils
from logger import get_logger

SERVER_ADDR = "tcp://localhost:5555"

logger = get_logger("client")


async def start_client() -> None:
    """Start the client application,
    and handle the user input to send the messages to the server."""
    try:
        ctx = Context()  # type: ignore
        skt = ctx.socket(zmq.REQ)
        skt.connect(SERVER_ADDR)

        while True:
            choice = utils.menu()
            match choice:
                case "quit":
                    break
                case "default":
                    replays = await handlers.default_cmds_handler(skt)
                    for replay in replays:
                        print(replay)
                case "os":
                    cmd = utils.read_user("enter the command")
                    replay = await handlers.os_cmd_handler(skt, cmd)
                    print(replay)
                case "compute":
                    expr = utils.read_user("enter the expression")
                    replay = await handlers.compute_cmd_handler(skt, expr)
                    print(replay)

    except Exception as e:
        logger.exception(e)
    finally:
        skt.close()
        ctx.term()
