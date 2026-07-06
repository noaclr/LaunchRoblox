import os
import sys
import time
import requests
from urllib.parse import urlencode, quote

class AuthenticationError(Exception):
    pass

def fetchAuthTicket(cookie):
    cookies = {".ROBLOSECURITY": cookie}
    
    try:
        r = requests.get("https://auth.roblox.com/v1/client-assertion", cookies=cookies)
        rJson = r.json()
    except (requests.RequestException, ValueError):
        raise AuthenticationError("Failed to communicate with the Roblox auth API.")

    if "clientAssertion" not in rJson:
        errorMsg = rJson.get("errors", [{}])[0].get("message", r.text)
        if "Authentication token is missing" in errorMsg:
            raise AuthenticationError("You forgot to provide a valid .ROBLOSECURITY cookie.")
        elif "User is not authenticated" in errorMsg:
            raise AuthenticationError("You provided an invalid .ROBLOSECURITY cookie.")
        raise AuthenticationError(f"API Error: {errorMsg}")
    
    clientAssertion = rJson["clientAssertion"]
    
    r = requests.post("https://auth.roblox.com/v2/logout", cookies=cookies)
    csrfToken = r.headers.get("x-csrf-token")
    if not csrfToken:
        raise AuthenticationError("Could not retrieve x-csrf-token header.")
    
    payload = {"clientAssertion": clientAssertion}
    headers = {"x-csrf-token": csrfToken, "Referer": "https://www.roblox.com/"}
    
    r = requests.post(
        "https://auth.roblox.com/v1/authentication-ticket", 
        data=payload, 
        cookies=cookies, 
        headers=headers
    )
    
    authTicket = r.headers.get("rbx-authentication-ticket")
    if not authTicket:
        raise AuthenticationError("Failed to obtain rbx-authentication-ticket from response headers.")

    return authTicket

def launchRoblox(placeId, cookie):
    query = urlencode({
        "request": "RequestGame",
        "browserTrackerId": "0",
        "placeId": placeId,
        "isPlayTogetherGame": "false",
        "referredByPlayerId": 0,
        "joinAttemptId": "",
        "joinAttemptOrigin": "PlayButton",
    })
    
    encodedPlaceUrl = quote(f"https://www.roblox.com/Game/PlaceLauncher.ashx?{query}", safe="")
    launchTime = int(time.time() * 1000)
    
    robloxURI = (
        "roblox-player:1"
        + "+launchmode:play"
        + f"+gameinfo:{fetchAuthTicket(cookie)}"
        + f"+launchtime:{launchTime}"
        + f"+placelauncherurl:{encodedPlaceUrl}"
        + f"+browsertrackerid:0"
        + "+robloxLocale:en_us"
        + "+gameLocale:en_us"
        + "+channel:"
        + "+LaunchExp:InApp"
    )

    if sys.platform == "win32":
        os.startfile(robloxURI)
    elif sys.platform == "darwin":
        os.system(f"open '{robloxURI}'")
    else:
        os.system(f"xdg-open '{robloxURI}'")