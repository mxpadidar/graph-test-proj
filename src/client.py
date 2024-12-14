import asyncio

from client.main import start_client

if __name__ == "__main__":
    try:
        asyncio.run(start_client())
    except KeyboardInterrupt:
        print("client stopped.")
