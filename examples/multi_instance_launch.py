import os
import time
import logging
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    cookie1 = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    cookie2 = os.getenv(".ROBLOSECURITY2", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example

    try:
        print("Launching first account instance...")
        launchRoblox(placeId, cookie1, multiInstance=True)

        print("Waiting for first client setup to stabilize...")
        time.sleep(3)

        print("Launching second account instance concurrently...")
        launchRoblox(placeId, cookie2, multiInstance=True)

        print("\n[Success] Both clients triggered concurrently utilizing native mutex overrides.")

    except AuthenticationError as e:
        print(f"[Auth Error] Multi-launch sequence blocked: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()