import os
import logging
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 142823291 # Murder Mystery example
    
    linkCode = "c1e0782d977e224f8aa44d15f3b7d39b" # Private Server linkCode (linkCode = "?code=", in private server links) https://www.roblox.com/share?code=c1e0782d977e224f8aa44d15f3b7d39b&type=Server

    print(f"Launching Roblox to Private Server (Place ID: {placeId})...")

    try:
        launchRoblox(placeId, cookie, linkCode=linkCode)
        print("[Success] Roblox client launch triggered successfully!")
    except AuthenticationError as e:
        print(f"[Auth Error] Failed to launch: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()