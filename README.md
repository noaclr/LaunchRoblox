# LaunchRoblox

A lightweight, cross-platform Python utility to programmatically authenticate and launch the Roblox client using a `.ROBLOSECURITY` cookie and a specific Place ID.

## Features

- **Automated Auth Flow:** Seamlessly exchanges a `.ROBLOSECURITY` cookie for an official `rbx-authentication-ticket` using the secure Roblox authentication endpoints.
- **Cross-Platform Support:** Native client launching support across **Windows** (`os.startfile`), **macOS** (`open`), and **Linux** (`xdg-open`).
- **Defensive Error Handling:** Built-in validation checks to catch expired, missing, or invalid authentication tokens before launching.
- **Zero Disk Overhead:** Clean, direct execution without bloating your local environment.

## Installation

Install the package directly from PyPI:

```bash
pip install LaunchRoblox

```

## Quick Start

```python
from roblox_launcher import launchRoblox, AuthenticationError

# Replace with your actual .ROBLOSECURITY cookie
cookie = "_|WARNING:-DO-NOT-SHARE-THIS..."
# The Place ID you want to join (e.g., 2753915549 for Blox Fruits)
placeId = 2753915549 

try:
    print("Authenticating and launching client...")
    launchRoblox(placeId, cookie)
    print("Success! Roblox protocol handler triggered.")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

```

## API Reference

### `launchRoblox(placeId, cookie)`

Generates an authentication ticket and fires the platform's native URI scheme (`roblox-player:1+...`) to open the game client.

* `placeId` *(int)*: The unique ID of the Roblox place/experience.
* `cookie` *(str)*: The full `.ROBLOSECURITY` token for the target account.

### `fetchAuthTicket(cookie)`

Handles the underlying backend API handshake to retrieve a valid launch token. This involves retrieving a client assertion, obtaining a valid CSRF token, and exchanging them for the final authentication ticket.

* `cookie` *(str)*: The target account's cookie.
* **Returns:** *(str)* A valid `rbx-authentication-ticket`.
* **Raises:** `AuthenticationError` if the cookie is invalid, missing, or if the API communication fails.

## Requirements

* Python >= 3.7
* `requests` library

## License

This project is licensed under the MIT License - see the LICENSE file for details.