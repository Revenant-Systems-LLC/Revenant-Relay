import os
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False

from ..paths import ROOT

_ERROR_CAUSE = {
    "AUTH_ERROR": "TikTok credentials are missing or invalid.",
    "MEDIA_ERROR": "Approved media file is missing or unreadable.",
    "PLATFORM_AUTOMATION_ERROR": "TikTok posting automation is intentionally disabled for safety and reliability.",
}

_ERROR_FIX = {
    "AUTH_ERROR": "Set RR_TIKTOK_USERNAME and RR_TIKTOK_PASSWORD to valid account credentials.",
    "MEDIA_ERROR": "Provide a valid approved media file path in the ad library.",
    "PLATFORM_AUTOMATION_ERROR": "Keep TikTok on simulator mode or implement/update a vetted UI flow before enabling automation.",
}


def _resolve_media(media_path):
    p = Path(media_path)
    if p.is_absolute():
        return p
    return ROOT / p


def _result(success, post_url=None, error_type=None, detected=None, raw=None, screenshot_path=None):
    return {
        "success": success,
        "error_type": error_type,
        "detected_issue": detected,
        "likely_cause": _ERROR_CAUSE.get(error_type) if error_type else None,
        "suggested_fix": _ERROR_FIX.get(error_type) if error_type else None,
        "raw_error": raw,
        "post_url": post_url,
        "screenshot_path": screenshot_path,
        "transient": False,
    }


class TikTokAdapter:
    def __init__(self, tiktok_config, settings):
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("playwright is not installed. Run: pip install playwright")

        cfg = tiktok_config or {}
        self.username_env = cfg.get("username_env_var", "RR_TIKTOK_USERNAME")
        self.password_env = cfg.get("password_env_var", "RR_TIKTOK_PASSWORD")
        self.enable_automation_env = cfg.get("enable_automation_env_var", "RR_TIKTOK_ENABLE_AUTOMATION")

        self.username = os.getenv(self.username_env, "")
        self.password = os.getenv(self.password_env, "")
        self.enable_automation = os.getenv(self.enable_automation_env, "").lower() == "true"

        if not self.username or not self.password:
            raise RuntimeError(
                "TikTok credentials missing. Set env vars: "
                f"{self.username_env}, {self.password_env}"
            )

        mode = (settings or {}).get("mode", "dev")
        mode_settings = (settings or {}).get(f"{mode}_mode", {})
        self.headless = mode_settings.get("headless", mode == "scheduled")

    def post_ad(self, ad, caption):
        media_path = ad.get("media_path")
        if not media_path:
            return _result(False, error_type="MEDIA_ERROR", detected="Ad missing media_path", raw="missing_media_path")

        resolved = _resolve_media(media_path)
        if not resolved.exists():
            return _result(False, error_type="MEDIA_ERROR", detected=f"Media file not found: {media_path}", raw=str(resolved))

        _ = caption  # Must be passed through unchanged by caller contract.

        if not self.enable_automation:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected="TikTok adapter is a safe stub; real posting is disabled unless RR_TIKTOK_ENABLE_AUTOMATION=true.",
                raw="automation_disabled",
                screenshot_path=None,
            )

        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()
                page.goto("https://www.tiktok.com/login", wait_until="domcontentloaded", timeout=30000)
                context.close()
                browser.close()
        except Exception as e:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected="TikTok browser automation failed before a stable posting flow could be executed.",
                raw=repr(e),
                screenshot_path=None,
            )

        return _result(
            False,
            error_type="PLATFORM_AUTOMATION_ERROR",
            detected="TikTok posting flow is not implemented in this build.",
            raw="not_implemented",
            screenshot_path=None,
        )
