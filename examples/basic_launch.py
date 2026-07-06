import os
from LaunchRoblox import launchRoblox, AuthenticationError

def main():
    cookie = os.getenv(".ROBLOSECURITY", "_|WARNING:-DO-NOT-SHARE-THIS...")
    placeId = 2753915549 # Blox Fruits example

    print(f"Launching Roblox to Place ID: {placeId}...")

    try:
        launchRoblox(placeId, cookie)
        print("[Success] Roblox client launch triggered successfully!")
    except AuthenticationError as e:
        print(f"[Auth Error] Failed to launch: {e}")
    except Exception as e:
        print(f"[Unexpected Error] {e}")

if __name__ == "__main__":
    main()