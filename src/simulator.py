import json
import random
from .paths import PLATFORMS_FILE


_TEMP_FAILURE_TYPES = ["NETWORK_ERROR"]
_PERMANENT_FAILURE_TYPES = [
    "AUTH_ERROR",
    "MEDIA_ERROR",
    "CONTENT_ERROR",
    "PLATFORM_AUTOMATION_ERROR",
    "RATE_LIMIT_ERROR",
]


def _success_rate(platform):
    with PLATFORMS_FILE.open("r", encoding="utf-8") as f:
        cfg = json.load(f).get("platforms", {})
    return cfg.get(platform, {}).get("simulated_success_rate", 0.5)


def simulate_post(platform, ad):
    """
    Pretend to post. Returns a dict matching the real adapter contract:
      success: bool
      error_type: str | None
      detected_issue: str | None
      likely_cause: str | None
      suggested_fix: str | None
      raw_error: str | None
      post_url: str | None
      screenshot_path: str | None
      transient: bool
    """
    rate = _success_rate(platform)
    if random.random() < rate:
        return {
            "success": True,
            "error_type": None,
            "detected_issue": None,
            "likely_cause": None,
            "suggested_fix": None,
            "raw_error": None,
            "post_url": f"https://{platform}.example/simulated/{ad['id']}",
            "screenshot_path": None,
            "transient": False,
            "simulated": True,
        }

    transient = random.random() < 0.25
    pool = _TEMP_FAILURE_TYPES if transient else _PERMANENT_FAILURE_TYPES
    err = random.choice(pool)
    return {
        "success": False,
        "error_type": err,
        "detected_issue": f"Simulated {err} on {platform}",
        "likely_cause": _likely_cause(err),
        "suggested_fix": _suggested_fix(err),
        "raw_error": f"SIMULATED::{err}::{platform}::{ad['id']}",
        "post_url": None,
        "screenshot_path": None,
        "transient": transient,
        "simulated": True,
    }


def _likely_cause(err):
    return {
        "AUTH_ERROR": "Session cookie expired or account flagged.",
        "MEDIA_ERROR": "Media rejected by platform (size, type, or dimensions).",
        "CONTENT_ERROR": "Caption flagged or duplicate detected.",
        "PLATFORM_AUTOMATION_ERROR": "Selector or page layout changed.",
        "RATE_LIMIT_ERROR": "Platform temporarily throttling actions.",
        "NETWORK_ERROR": "Transient network or upstream failure.",
    }.get(err, "Unknown.")


def _suggested_fix(err):
    return {
        "AUTH_ERROR": "Re-authenticate the platform session.",
        "MEDIA_ERROR": "Replace media with a compliant file.",
        "CONTENT_ERROR": "Adjust caption or check for duplicates.",
        "PLATFORM_AUTOMATION_ERROR": "Update adapter selectors.",
        "RATE_LIMIT_ERROR": "Skip this platform for the day.",
        "NETWORK_ERROR": "Retry once; may be transient.",
    }.get(err, "Investigate manually.")
