# LaunchRoblox 🚀

A lightweight, robust, and zero-headache utility to programmatically authenticate and launch the Roblox client using Python. 

Built with modern Python standards, `LaunchRoblox` natively handles the complex `roblox-player:` URI protocol, API ticket exchanges, and CSRF token generation so you don't have to.

## Installation

Install the latest version directly from PyPI:
```bash
pip install LaunchRoblox

```

## Features

* **Instant Launching:** Bypass the browser and launch directly into a game.
* **Private Server Support:** Automatically resolves VIP `linkCode` URLs into backend access codes.
* **Instance Targeting:** Follow users into exact server UUIDs (`jobId`).
* **Deployment Channels:** Test your game on specific Roblox bootstrapper channels (e.g., `zCanary`).
* **Built-in Logging:** Fully integrated with Python's native `logging` module for easy debugging.

---

## Usage Examples

### 1. Basic Launch (Public Server)

```python
import os
from LaunchRoblox import launchRoblox

cookie = os.getenv("ROBLOX_COOKIE", "_|WARNING:-DO-NOT-SHARE-THIS...")
placeId = 2753915549

launchRoblox(placeId, cookie)

```

### 2. Private Server Launch

If you have a VIP server link (e.g., `?privateServerLinkCode=12345...`), pass the code directly. The library will safely resolve it into a server access code via the Roblox API before launching.

```python
launchRoblox(
    placeId=2753915549, 
    cookie=cookie, 
    linkCode="your_private_server_link_code"
)

```

### 3. Target a Specific Server (Job ID)

Perfect for multi-account testing or following someone into a specific server block.

```python
launchRoblox(
    placeId=2753915549, 
    cookie=cookie, 
    jobId="01af84de-4bca-413c-8361-ec23bfda85b2"
)

```

### 4. Custom Deployment Channel

Launch into a specific Roblox testing branch. (Note: Using `"LIVE"` or leaving this blank will safely default to the public production client).

```python
launchRoblox(
    placeId=2753915549, 
    cookie=cookie, 
    channel="zCanary"
)

```

---

## Advanced: Debug Logging

`LaunchRoblox` uses Python's standard `logging` module under the hood. If you are experiencing authentication errors or want to see the background API routing in real-time, simply configure your root logger before calling the launch function:

```python
import logging
from LaunchRoblox import launchRoblox

# Enable info/debug logging to your console
logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(name)s: %(message)s")

launchRoblox(2753915549, "YOUR_COOKIE")

```

## License

MIT