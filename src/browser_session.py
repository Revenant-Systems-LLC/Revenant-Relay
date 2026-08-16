"""Persistent browser sessions for adapters that drive a page instead of an API.

The existing Playwright adapters each open a blank browser and then type a
stored username and password into the login form. That is the worst available
shape: a fresh profile with no history is what bot detection is built to catch,
the login step breaks the moment a site shows a captcha or a 2FA prompt, and it
requires keeping the password where the code can read it.

This replaces all of that with a profile directory that persists between runs.
A human logs in once (`relay_login.py`), the cookies land on disk, and every
run afterwards is already authenticated. No password in the vault, no login
code to break, no captcha for a bot to fail.

Deliberately not Dave's real Opera GX profile. Playwright takes a lock on the
profile directory it opens, so aiming it at a live browser profile means a run
at 3am either fails or corrupts the profile he uses every day. A separate
directory costs one manual login and removes that entire class of accident.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from .paths import BROWSER_PROFILES_DIR

# Chromium is Playwright's own bundled build. Opera GX would also work (it is
# Chromium 133 underneath) but its executable path carries the version number
# and changes on every auto-update, which would break the adapter silently.
# Since this is a dedicated profile either way, nothing is gained by using it.
#
# No launch args and no user_agent override. The browser sends whatever Chromium
# sends. --disable-blink-features=AutomationControlled was in here briefly out of
# habit; its only function is hiding the automation marker from the page, which
# is exactly the thing this project does not do.
_LAUNCH_ARGS: list[str] = []


def profile_dir(platform: str) -> Path:
    """Return the persistent profile directory for a platform, creating it."""
    path = BROWSER_PROFILES_DIR / platform
    path.mkdir(parents=True, exist_ok=True)
    return path


def has_profile(platform: str) -> bool:
    """True if a login has ever been performed for this platform.

    Chromium writes a 'Default' subdirectory the first time it runs, so its
    presence is a reliable marker that the profile was actually opened rather
    than just created by profile_dir().
    """
    return (BROWSER_PROFILES_DIR / platform / "Default").is_dir()


def clear_profile(platform: str) -> None:
    """Delete a platform's profile so the next login starts clean."""
    path = BROWSER_PROFILES_DIR / platform
    if path.exists():
        shutil.rmtree(path)


def launch_persistent(playwright, platform: str, headless: bool, timeout_ms: int = 60000):
    """Open the platform's persistent profile and return a BrowserContext.

    Caller owns the context and must close it. There is no separate Browser
    object with launch_persistent_context; the context *is* the browser.
    """
    context = playwright.chromium.launch_persistent_context(
        user_data_dir=str(profile_dir(platform)),
        headless=headless,
        args=_LAUNCH_ARGS,
        viewport={"width": 1440, "height": 900},
    )
    context.set_default_timeout(timeout_ms)
    return context
