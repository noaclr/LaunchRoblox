import os
import logging
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    
    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example
    
    channel = "LIVE" # Deployment channel to launch into (e.g., "LIVE", "zCanary", etc.). Most won't work unless you have access to that channel. Leaving it on "LIVE" will do nothing, so if you are just setting it to that you might as well not use this argument at all.

    print(f"Launching Roblox into a specific deployment channel...")
    print(f"Place ID: {placeId} | Channel: {channel}")

    try:
        launchRoblox(placeId, cookie, channel=channel)
        print("[Success] Roblox client launch triggered successfully!")
    except AuthenticationError as e:
        print(f"[Auth Error] Failed to launch: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()