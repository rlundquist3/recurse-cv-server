import asyncio
# from oscpy.client import OSCClient
from websockets.asyncio.server import broadcast, serve
from . import rctogether

# address = "127.0.0.1"
# port = 8000
# osc = OSCClient(address, port)

loop: asyncio.AbstractEventLoop | None = None
message_queue: asyncio.Queue[bytes] = asyncio.Queue()

def send_message(input_number, value):
    # osc.send_message(b'/cv', [input_number, value])
    message = f"/cv/{input_number}/value/{value}".encode(encoding='utf-8')
    loop.call_soon_threadsafe(message_queue.put_nowait, message)

async def websocket_handler(websocket):
    await websocket.wait_closed()

async def broadcaster(server):
    while True:
        message = await message_queue.get()
        if (server.connections):
            print(f"sending OSC message: {message}")
            broadcast(server.connections, message)
        else:
            print("no client; dropping message")

async def open():
    global loop
    loop = asyncio.get_running_loop()
    print("starting up")
    async with serve(websocket_handler, "localhost", 8001) as server:
        await asyncio.gather(server.serve_forever(), broadcaster(server))