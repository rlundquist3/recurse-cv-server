import asyncio
from . import app

def main() -> None:
    try:
        asyncio.run(app.main())
    except KeyboardInterrupt:
        print("\n\nAPI shut down")
