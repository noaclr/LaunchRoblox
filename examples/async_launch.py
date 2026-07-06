import os
import asyncio
import logging
from LaunchRoblox import launchRobloxAsync, AuthenticationError

async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example

    try:
        print("Starting async launch...")
        game_process = await launchRobloxAsync(placeId, cookie)
        
        if game_process:
            print(f"Async launch success! Tracking active game on PID: {game_process.pid}")
        else:
            print("Async launch triggered but tracking sequence timed out.")
    
    except AuthenticationError as e:
        print(f"Authentication failed: {e}")

if __name__ == "__main__":
    asyncio.run(main())