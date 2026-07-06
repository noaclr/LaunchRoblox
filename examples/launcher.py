import os
import sys
import time
import psutil
import ctypes
import logging
import requests
from typing import Optional, Set
from urllib.parse import urlencode, quote

logger = logging.getLogger("LaunchRoblox")
_mutex_handle = None

class AuthenticationError(Exception):
    pass

class RobloxProcess:
    """Tracks the lifecycle of a spawned Roblox client instance."""
    def __init__(self, proc: psutil.Process):
        self._proc = proc
        self.pid: int = proc.pid

    def isRunning(self) -> bool:
        """Checks if the tracked Roblox client instance is still active."""
        return self._proc.is_running()
    
    def wait(self) -> None:
        """Blocks execution until the tracked Roblox client instance terminates."""
        try:
            self._proc.wait()
        except psutil.NoSuchProcess:
            pass
    
    def kill(self) -> None:
        """Forcibly terminates the tracked Roblox client instance."""
        try:
            self._proc.kill()
        except psutil.NoSuchProcess:
            pass

def maintainMultiInstance() -> None:
    """Claims the system mutex handle to allow launching multiple Roblox instances concurrently on Windows."""
    global _mutex_handle
    if sys.platform == "win32" and _mutex_handle is None:
        _mutex_handle = ctypes.windll.kernel32.CreateMutexW(None, True, "ROBLOX_singletonEvent")
        logger.info("Native multi-instance handle (ROBLOX_singletonEvent) successfully claimed and held open.")

def fetchAuthTicket(cookie: str) -> str:
    """Authenticates with the Roblox API and returns a hardware launch ticket."""
    cookies = {".ROBLOSECURITY": cookie}
    
    logger.debug("Requesting client assertion token from auth API...")
    try:
        r = requests.get("https://auth.roblox.com/v1/client-assertion", cookies=cookies)
        rJson = r.json()
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Network failure during client assertion request: {e}")
        raise AuthenticationError("Failed to communicate with the Roblox auth API.")

    if "clientAssertion" not in rJson:
        errorMsg = rJson.get("errors", [{}])[0].get("message", r.text)
        logger.warning(f"Client assertion failed validation: {errorMsg}")
        if "Authentication token is missing" in errorMsg:
            raise AuthenticationError("You forgot to provide a valid .ROBLOSECURITY cookie.")
        elif "User is not authenticated" in errorMsg:
            raise AuthenticationError("You provided an invalid .ROBLOSECURITY cookie.")
        raise AuthenticationError(f"API Error: {errorMsg}")
    
    clientAssertion = rJson["clientAssertion"]
    
    logger.debug("Generating fresh X-CSRF token...")
    r = requests.post("https://auth.roblox.com/v2/logout", cookies=cookies)
    csrfToken = r.headers.get("x-csrf-token")
    if not csrfToken:
        logger.error("Failed to extract x-csrf-token from response headers.")
        raise AuthenticationError("Could not retrieve x-csrf-token header.")
    
    payload = {"clientAssertion": clientAssertion}
    headers = {"x-csrf-token": csrfToken, "Referer": "https://www.roblox.com/"}
    
    logger.debug("Submitting token exchange for authentication ticket...")
    r = requests.post(
        "https://auth.roblox.com/v1/authentication-ticket", 
        data=payload, 
        cookies=cookies, 
        headers=headers
    )
    
    authTicket = r.headers.get("rbx-authentication-ticket")
    if not authTicket:
        logger.error("Authentication handshake completed but rbx-authentication-ticket header was missing.")
        raise AuthenticationError("Failed to obtain rbx-authentication-ticket from response headers.")

    logger.debug("Authentication ticket successfully retrieved.")
    return authTicket

def getAccessCode(placeId: int, linkCode: str, cookie: str) -> str:
    """Resolves a public private server linkCode into an internal server accessCode GUID."""
    cookies = {".ROBLOSECURITY": cookie}
    logger.info(f"Resolving private server linkCode for Place ID {placeId}...")

    try:
        r = requests.get(f"https://games.roblox.com/v1/games/{placeId}/private-servers?linkCode={linkCode}", cookies=cookies)
        data = r.json()
    except (requests.RequestException, ValueError) as e:
        logger.error(f"Failed to connect to games API for private server validation: {e}")
        raise AuthenticationError("Failed to communicate with the Roblox games API.")

    if "data" in data and len(data["data"]) > 0 and "accessCode" in data["data"][0]:
        accessCode = data["data"][0]["accessCode"]
        logger.debug(f"Successfully resolved accessCode: {accessCode}")
        return accessCode
    else:
        logger.error(f"Private server response structure invalid or unauthorized: {data}")
        raise AuthenticationError(f"Could not resolve linkCode: {data}")

def launchRoblox(placeId: int, cookie: str, linkCode: Optional[str] = None, jobId: Optional[str] = None, channel: str = "", multiInstance: bool = False) -> Optional[RobloxProcess]:
    """Triggers the native system bootstrapper to launch Roblox with the specified game configurations and returns a tracker for the spawned process."""
    if multiInstance:
        maintainMultiInstance()
    
    targetName = "RobloxPlayerBeta.exe" if sys.platform == "win32" else "RobloxPlayer"

    existingPids: Set[int] = set()
    try:
        for proc in psutil.process_iter(["pid", "name"]):
            if proc.info["name"] == targetName:
                existingPids.add(proc.info["pid"])
    except Exception as e:
        logger.warning(f"Failed to index existing processes: {e}")
    
    logger.info(f"Preparing to launch client for Place ID: {placeId}")

    queryData = {
        "request": "RequestGame",
        "browserTrackerId": "0",
        "placeId": placeId,
        "isPlayTogetherGame": "false",
        "referredByPlayerId": 0,
        "joinAttemptId": "",
        "joinAttemptOrigin": "PlayButton",
    }

    if linkCode:
        logger.info("Private server parameters detected. Initiating link resolution...")
        accessCode = getAccessCode(placeId, linkCode, cookie)
        queryData["request"] = "RequestPrivateGame"
        queryData["linkCode"] = linkCode
        queryData["accessCode"] = accessCode
    elif jobId:
        logger.info(f"Targeting explicit server instance Job ID: {jobId}")
        queryData["request"] = "RequestGameJob"
        queryData["gameId"] = jobId
    
    query = urlencode(queryData)
    encodedPlaceUrl = quote(f"https://www.roblox.com/Game/PlaceLauncher.ashx?{query}", safe="")
    launchTime = int(time.time() * 1000)
    
    logger.debug("Requesting platform authentication ticket...")
    authTicket = fetchAuthTicket(cookie)

    robloxURI = (
        "roblox-player:1"
        + "+launchmode:play"
        + f"+gameinfo:{authTicket}"
        + f"+launchtime:{launchTime}"
        + f"+placelauncherurl:{encodedPlaceUrl}"
        + f"+browsertrackerid:0"
        + "+robloxLocale:en_us"
        + "+gameLocale:en_us"
    )

    if channel and channel.upper() != "LIVE":
        logger.info(f"Routing launch through deployment channel branch: {channel}")
        robloxURI += f"+channel:{channel}"
    else:
        logger.debug("Using public production deployment branch.")
    
    robloxURI += "+LaunchExp:InApp"

    logger.info("Passing execution handshake to system protocol handler...")
    if sys.platform == "win32":
        os.startfile(robloxURI)
    elif sys.platform == "darwin":
        os.system(f"open '{robloxURI}'")
    else:
        os.system(f"xdg-open '{robloxURI}'")
    
    logger.info("System protocol triggered. Polling for process creation tracker...")

    startTime = time.time()
    while time.time() - startTime < 15:
        try:
            for proc in psutil.process_iter(["pid", "name"]):
                if proc.info["name"] == targetName and proc.info["pid"] not in existingPids:
                    logger.info(f"Tracked newly spawned Roblox client instance (PID: {proc.info['pid']})")
                    return RobloxProcess(proc)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
        time.sleep(0.25)

    logger.warning("Roblox process launched but tracking polling window timed out.")
    return None