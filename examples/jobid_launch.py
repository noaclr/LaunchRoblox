import os
import logging
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")
    
    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example
    
    jobId = "aee8c3a1-0c96-4840-aa8a-a702f880df09" # jobId of the specific server you want to join

    print(f"Launching Roblox to Specific Server Instance...")
    print(f"Place ID: {placeId} | Job ID: {jobId}")

    try:
        launchRoblox(placeId, cookie, jobId=jobId)
        print("[Success] Roblox client launch triggered successfully!")
    except AuthenticationError as e:
        print(f"[Auth Error] Failed to launch: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()