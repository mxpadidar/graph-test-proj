import asyncio
import json

import zmq
from zmq.asyncio import Context, Socket

from logger import get_logger
from server.errors import BaseErr
from server.handlers import process_message

SERVER_ADDR = "tcp://localhost:5555"

logger = get_logger("server")


async def proceed_requests(skt: Socket) -> None:
    """Receives and processes messages over a ZMQ socket."""
    while True:
        msg = await skt.recv()
        try:
            cmd_result = await process_message(msg.decode())
            replay = {"status": "success", "result": cmd_result}
        except BaseErr as err:
            replay = {"status": "error", "detail": err.msg}
        except Exception as err:
            replay = {"status": "error", "detail": "something went wrong"}
            logger.error("unexpected error. msg: %s. error: %s", msg, err)

        replay = json.dumps(replay).encode()
        await skt.send(replay)
        logger.info("msg: %s, response: %s", msg, replay)


async def start_server() -> None:
    while True:
        try:
            ctx = Context()  # type: ignore
            skt = ctx.socket(zmq.REP)
            skt.bind(SERVER_ADDR)
            await proceed_requests(skt)
        except Exception as err:
            logger.critical(f"Server crashed: {err}")
            logger.info("Restarting server in 1 second.")
            await asyncio.sleep(1)
        finally:
            skt.close()
            ctx.term()
