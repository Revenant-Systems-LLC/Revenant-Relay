import os
from datetime import datetime
from pathlib import Path

try:
    from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
    from playwright.sync_api import sync_playwright

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    PlaywrightTimeoutError = Exception

from ..paths import LOGS_DIR, ROOT

_ERROR_CAUSE = {
    "AUTH_ERROR": "LinkedIn authentication failed or account access is blocked by a challenge.",
    "MEDIA_ERROR": "Media file was missing, unsupported, or rejected by LinkedIn.",
    "PLATFORM_AUTOMATION_ERROR": "LinkedIn compose/publish UI flow was not reliably automatable.",
    "NETWORK_ERROR": "Transient timeout or connectivity issue while using LinkedIn.",
    "RATE_LIMIT_ERROR": "LinkedIn temporarily blocked or throttled posting actions.",
    "CONTENT_ERROR": "LinkedIn rejected the post content.",
}

_ERROR_FIX = {
    "AUTH_ERROR": "Verify LinkedIn credentials and ensure the account can pass any manual verification steps.",
    "MEDIA_ERROR": "Confirm ad.media_path exists and uses a supported image/video format.",
    "PLATFORM_AUTOMATION_ERROR": "Re-validate selectors and posting flow in the LinkedIn adapter.",
    "NETWORK_ERROR": "Retry the run; if persistent, validate local network and LinkedIn availability.",
    "RATE_LIMIT_ERROR": "Wait before retrying and reduce posting frequency.",
    "CONTENT_ERROR": "Adjust approved caption/media to comply with LinkedIn posting rules.",
}

_TRANSIENT_TYPES = {"NETWORK_ERROR", "RATE_LIMIT_ERROR"}



def _result(success, post_url=None, error_type=None, detected=None, raw=None, screenshot_path=None):
    return {
        "success": success,
        "error_type": error_type,
        "detected_issue": detected,
        "likely_cause": _ERROR_CAUSE.get(error_type) if error_type else None,
        "suggested_fix": _ERROR_FIX.get(error_type) if error_type else None,
        "raw_error": raw,
        "post_url": post_url,
        "screenshot_path": str(screenshot_path) if screenshot_path else None,
        "transient": error_type in _TRANSIENT_TYPES if error_type else False,
    }


def _resolve_media(media_path):
    p = Path(media_path)
    if p.is_absolute():
        return p
    return ROOT / p


class LinkedInAdapter:
    def __init__(self, linkedin_config, settings):
        if not PLAYWRIGHT_AVAILABLE:
            raise RuntimeError("playwright is not installed. Run: pip install playwright")

        cfg = linkedin_config or {}
        self.username_env = cfg.get("username_env_var", "RR_LINKEDIN_USERNAME")
        self.password_env = cfg.get("password_env_var", "RR_LINKEDIN_PASSWORD")
        self.post_target_env = cfg.get("post_target_env_var", "RR_LINKEDIN_POST_TARGET")
        self.company_page_url_env = cfg.get("company_page_url_env_var", "RR_LINKEDIN_COMPANY_PAGE_URL")

        self.username = os.getenv(self.username_env, "").strip()
        self.password = os.getenv(self.password_env, "").strip()
        self.post_target = os.getenv(self.post_target_env, "company").strip().lower()
        self.company_page_url = os.getenv(self.company_page_url_env, "").strip()

        if not self.username or not self.password:
            raise RuntimeError(
                "LinkedIn credentials missing. Set env vars: "
                f"{self.username_env}, {self.password_env}"
            )

        if self.post_target not in {"company", "profile"}:
            raise RuntimeError(
                f"Unsupported LinkedIn post target '{self.post_target}'. "
                "Use 'company' or 'profile'."
            )

        if self.post_target == "company" and not self.company_page_url:
            raise RuntimeError(
                "LinkedIn company target requires company page URL env var: "
                f"{self.company_page_url_env}"
            )

        mode = (settings or {}).get("mode", "dev")
        mode_settings = (settings or {}).get(f"{mode}_mode", {})
        self.headless = mode_settings.get("headless", mode == "scheduled")

    def post_ad(self, ad, caption):
        if caption is None:
            caption = ""

        media_path = ad.get("media_path")
        resolved_media = None
        if media_path:
            resolved_media = _resolve_media(media_path)
            if not resolved_media.exists() or not resolved_media.is_file():
                return _result(
                    False,
                    error_type="MEDIA_ERROR",
                    detected=f"Media file not found: {media_path}",
                    raw=str(resolved_media),
                )

        browser = None
        context = None
        page = None
        try:
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                context = browser.new_context()
                page = context.new_page()

                login_gate = self._ensure_authenticated(page)
                if login_gate:
                    login_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**login_gate)

                nav_gate = self._navigate_to_post_surface(page)
                if nav_gate:
                    nav_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**nav_gate)

                compose_gate = self._open_composer(page)
                if compose_gate:
                    compose_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**compose_gate)

                caption_gate = self._fill_caption(page, caption)
                if caption_gate:
                    caption_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**caption_gate)

                media_gate = self._attach_media_if_any(page, resolved_media)
                if media_gate:
                    media_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**media_gate)

                publish_gate = self._publish_if_clear(page)
                if publish_gate:
                    publish_gate["screenshot_path"] = self._capture_screenshot(page)
                    return _result(**publish_gate)

                return self._confirm_publish(page)

        except PlaywrightTimeoutError as e:
            return _result(
                False,
                error_type="NETWORK_ERROR",
                detected="Timeout while navigating LinkedIn pages.",
                raw=repr(e),
                screenshot_path=self._capture_screenshot(page),
            )
        except Exception as e:
            error_type = self._classify_error(str(e))
            return _result(
                False,
                error_type=error_type,
                detected=str(e),
                raw=repr(e),
                screenshot_path=self._capture_screenshot(page),
            )
        finally:
            if context is not None:
                try:
                    context.close()
                except Exception:
                    pass
            if browser is not None:
                try:
                    browser.close()
                except Exception:
                    pass

    def _ensure_authenticated(self, page):
        page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(1500)

        if self._is_logged_in(page):
            return None

        page.goto("https://www.linkedin.com/login", wait_until="domcontentloaded", timeout=60000)
        page.locator('input[name="session_key"]').first.fill(self.username)
        page.locator('input[name="session_password"]').first.fill(self.password)
        page.get_by_role("button", name="Sign in").first.click()
        page.wait_for_timeout(3500)

        blocker = self._detect_auth_blocker(page)
        if blocker:
            return blocker

        if not self._is_logged_in(page):
            return {
                "success": False,
                "error_type": "AUTH_ERROR",
                "detected": "Unable to establish logged-in LinkedIn session.",
                "raw": f"still_unauthenticated:{page.url}",
                "post_url": None,
            }

        return None

    def _is_logged_in(self, page):
        url = page.url.lower()
        if "/feed" in url and "linkedin.com" in url and "/login" not in url:
            return True
        if page.locator('button[aria-label*="Start a post"]').count() > 0:
            return True
        if page.locator('a[href*="/mynetwork/"]').count() > 0:
            return True
        return False

    def _detect_auth_blocker(self, page):
        body = page.content().lower()
        url = page.url.lower()
        if "invalid" in body and "password" in body:
            return {"success": False, "error_type": "AUTH_ERROR", "detected": "Invalid LinkedIn credentials.", "raw": "invalid_credentials", "post_url": None}
        if "checkpoint" in url or "checkpoint" in body:
            return {"success": False, "error_type": "AUTH_ERROR", "detected": "LinkedIn checkpoint challenge detected.", "raw": "checkpoint", "post_url": None}
        if "captcha" in body:
            return {"success": False, "error_type": "AUTH_ERROR", "detected": "LinkedIn captcha challenge detected.", "raw": "captcha", "post_url": None}
        if "two-step" in body or "verification code" in body or "2fa" in body:
            return {"success": False, "error_type": "AUTH_ERROR", "detected": "LinkedIn 2FA challenge detected.", "raw": "2fa", "post_url": None}
        if "security challenge" in body:
            return {"success": False, "error_type": "AUTH_ERROR", "detected": "LinkedIn security challenge detected.", "raw": "security_challenge", "post_url": None}
        return None

    def _navigate_to_post_surface(self, page):
        if self.post_target == "company":
            page.goto(self.company_page_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2500)
            body = page.content().lower()
            if "you don't have access" in body or "request admin access" in body:
                return {
                    "success": False,
                    "error_type": "AUTH_ERROR",
                    "detected": "Missing LinkedIn company page admin access.",
                    "raw": "missing_company_admin_access",
                    "post_url": None,
                }
        else:
            page.goto("https://www.linkedin.com/feed/", wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(1500)
        return None

    def _open_composer(self, page):
        selectors = [
            'button[aria-label*="Start a post"]',
            'button:has-text("Start a post")',
            'span:has-text("Start a post")',
            'button:has-text("Create")',
        ]
        for sel in selectors:
            loc = page.locator(sel).first
            if loc.count() > 0:
                loc.click(timeout=5000)
                page.wait_for_timeout(1500)
                if page.locator('[role="dialog"]').count() > 0 or page.locator('div[contenteditable="true"]').count() > 0:
                    return None
        return {
            "success": False,
            "error_type": "PLATFORM_AUTOMATION_ERROR",
            "detected": "LinkedIn post composer could not be opened.",
            "raw": "composer_open_failed",
            "post_url": None,
        }

    def _fill_caption(self, page, caption):
        textbox = page.locator('div[role="textbox"][contenteditable="true"]').first
        if textbox.count() == 0:
            textbox = page.locator('div[contenteditable="true"]').first
        if textbox.count() == 0:
            return {
                "success": False,
                "error_type": "PLATFORM_AUTOMATION_ERROR",
                "detected": "LinkedIn caption textbox not found.",
                "raw": "missing_caption_textbox",
                "post_url": None,
            }
        textbox.click(timeout=5000)
        textbox.fill(caption)
        return None

    def _attach_media_if_any(self, page, resolved_media):
        if not resolved_media:
            return None
        file_input = page.locator('input[type="file"]').first
        if file_input.count() == 0:
            button = page.get_by_role("button", name="Add a photo")
            if button.count() == 0:
                button = page.get_by_role("button", name="Add a video")
            if button.count() > 0:
                button.first.click()
                page.wait_for_timeout(1000)
            file_input = page.locator('input[type="file"]').first

        if file_input.count() == 0:
            return {
                "success": False,
                "error_type": "MEDIA_ERROR",
                "detected": "LinkedIn media input not available in composer.",
                "raw": "missing_media_file_input",
                "post_url": None,
            }

        file_input.set_input_files(str(resolved_media))
        page.wait_for_timeout(4000)
        body = page.content().lower()
        if "couldn't upload" in body or "failed to upload" in body or "unsupported" in body:
            return {
                "success": False,
                "error_type": "MEDIA_ERROR",
                "detected": "LinkedIn rejected media upload.",
                "raw": "upload_rejected",
                "post_url": None,
            }
        return None

    def _publish_if_clear(self, page):
        publish = page.get_by_role("button", name="Post").first
        if publish.count() == 0:
            publish = page.get_by_role("button", name="Publish").first
        if publish.count() == 0:
            return {
                "success": False,
                "error_type": "PLATFORM_AUTOMATION_ERROR",
                "detected": "Publish button was not found in LinkedIn composer.",
                "raw": "missing_publish_button",
                "post_url": None,
            }
        if publish.is_disabled():
            return {
                "success": False,
                "error_type": "CONTENT_ERROR",
                "detected": "LinkedIn publish button is disabled; content may be invalid.",
                "raw": "publish_disabled",
                "post_url": None,
            }
        publish.click(timeout=5000)
        page.wait_for_timeout(3000)
        return None

    def _confirm_publish(self, page):
        url_now = page.url
        body = page.content().lower()
        post_url = None

        if "/posts/" in url_now or "/feed/update/" in url_now:
            post_url = url_now

        if not post_url:
            anchors = page.locator('a[href*="/feed/update/"]')
            if anchors.count() > 0:
                href = anchors.first.get_attribute("href")
                if href:
                    post_url = href if href.startswith("http") else f"https://www.linkedin.com{href}"

        if post_url:
            return _result(True, post_url=post_url)

        if "post successful" in body or "your post is now live" in body or "shared" in body:
            return _result(
                True,
                post_url=None,
                error_type=None,
                detected="LinkedIn UI confirmed posting, but a post URL was not obtainable.",
                raw="ui_confirmed_without_url",
            )

        if "temporarily restricted" in body or "try again later" in body:
            return _result(False, error_type="RATE_LIMIT_ERROR", detected="LinkedIn temporarily restricted posting.", raw="rate_limited")

        return _result(
            False,
            error_type="PLATFORM_AUTOMATION_ERROR",
            detected="Publish confirmation was uncertain; no reliable success signal found.",
            raw="publish_confirmation_uncertain",
            screenshot_path=self._capture_screenshot(page),
        )

    def _capture_screenshot(self, page):
        if page is None:
            return None
        stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        out_dir = LOGS_DIR / datetime.now().date().isoformat() / "failures"
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"linkedin-{stamp}.png"
        try:
            page.screenshot(path=str(path), full_page=True)
            return path
        except Exception:
            return None

    def _classify_error(self, message):
        msg = message.lower()
        if "timeout" in msg or "net::" in msg or "connection" in msg:
            return "NETWORK_ERROR"
        if "rate" in msg or "too many" in msg or "try again later" in msg:
            return "RATE_LIMIT_ERROR"
        if "upload" in msg or "media" in msg or "file" in msg:
            return "MEDIA_ERROR"
        if "auth" in msg or "login" in msg or "password" in msg:
            return "AUTH_ERROR"
        if "content" in msg or "disabled" in msg:
            return "CONTENT_ERROR"
        return "PLATFORM_AUTOMATION_ERROR"
