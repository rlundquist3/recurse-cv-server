import asyncio
from . import rctogether, osc

async def main () -> None:
    print("Hello from recurse-cv-server!")
    await asyncio.gather(rctogether.listen(), osc.open())