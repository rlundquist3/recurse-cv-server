import asyncio
import os
from dotenv import load_dotenv
from pythonosc.tcp_client import SimpleTCPClient

loop: asyncio.AbstractEventLoop | None = None
message_queue: asyncio.Queue[bytes] = asyncio.Queue()

def send_message(input_number, value):
    address = f"/cv/{input_number}/value"
    loop.call_soon_threadsafe(message_queue.put_nowait, (address, value))

async def open():
    load_dotenv()
    global loop
    loop = asyncio.get_running_loop()

    osc_server_host = os.getenv('OSC_SERVER_HOST')
    osc_server_port = int(os.getenv('OSC_SERVER_PORT'))

    client = SimpleTCPClient(osc_server_host, osc_server_port)
    while True:
        (address, value) = await message_queue.get()
        try:
            print(f"sending to {address}")
            client.send_message(address, value)
        except:
            print(f"send failed; attempting to reconnect")
            client = SimpleTCPClient(osc_server_host, osc_server_port)
            client.send_message(address, value)
