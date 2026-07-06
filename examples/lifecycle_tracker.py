import os
import time
import logging
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example

    print("Launching Roblox client and initiating lifecycle tracker...")

    try:
        gameProcess = launchRoblox(placeId, cookie)

        if gameProcess:
            print(f"\n[Success] Tracked Roblox Client running on PID: {gameProcess.pid}")
            print("Python script will now wait until the game window is closed...\n")

            gameProcess.wait()

            print("[Finished] Roblox process terminated. Resuming Python execution.")
        else:
            print("[Warning] Client launched, but tracking poll timed out.")
    
    except AuthenticationError as e:
        print(f"[Auth Error] Launch sequence blocked: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()