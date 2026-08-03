import logging
import os
from pathlib import Path

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from ..paths import ROOT

GRAPH_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"

_ERROR_CAUSE = {
    "AUTH_ERROR": "Page access token is invalid, expired, or missing the pages_manage_posts permission.",
    "MEDIA_ERROR": "Image file missing, unreadable, or rejected by Facebook.",
    "CONTENT_ERROR": "Facebook rejected the message or link, or flagged it as a duplicate.",
    "RATE_LIMIT_ERROR": "Facebook is throttling this Page or has temporarily blocked publishing.",
    "PLATFORM_AUTOMATION_ERROR": "Graph API returned an unexpected response shape.",
    "NETWORK_ERROR": "Transient network failure while calling the Graph API.",
    "UNKNOWN_ERROR": "Could not classify failure reliably.",
}

_ERROR_FIX = {
    "AUTH_ERROR": (
        "Regenerate a long-lived Page access token in Graph API Explorer with pages_manage_posts "
        "and pages_read_engagement, then update RR_FACEBOOK_PAGE_TOKEN."
    ),
    "MEDIA_ERROR": "Verify the ad's media_path points at a readable JPEG or PNG under 4 MB.",
    "CONTENT_ERROR": "Reword the caption or change the link. Facebook rejects identical repeat posts.",
    "RATE_LIMIT_ERROR": "Stop Facebook attempts for at least 24 hours before retrying.",
    "PLATFORM_AUTOMATION_ERROR": "Inspect raw_error; the Graph response did not contain a post id.",
    "NETWORK_ERROR": "Retry once; likely transient connectivity issue.",
    "UNKNOWN_ERROR": "Inspect raw_error for the Graph API error payload.",
}

_TRANSIENT_TYPES = {"NETWORK_ERROR"}

# Graph API error codes worth classifying precisely.
_AUTH_CODES = {102, 190, 200, 210, 2500}
_RATE_CODES = {4, 17, 32, 341, 368, 613}
_CONTENT_CODES = {100, 506, 1404006}


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
        "screenshot_path": str(screenshot_path) if screenshot_path else None,
        "transient": error_type in _TRANSIENT_TYPES if error_type else False,
    }


class FacebookAdapter:
    """
    Publishes an approved ad to a Facebook Page via the Graph API.

    This is the sanctioned path. Posting to a Page you administer does not require
    App Review; an app in development mode can publish to Pages where you are an
    admin. No browser, no stored password, nothing for Facebook's automation
    detection to object to.

    Env vars:
      RR_FACEBOOK_PAGE_ID     numeric Page id
      RR_FACEBOOK_PAGE_TOKEN  long-lived Page access token (pages_manage_posts)

    v1 posts a single image with a caption, or a text+link post when the ad has
    no media. Multi-photo albums need the unpublished-upload-then-attach flow and
    are deliberately not implemented yet; only the first image is used.
    """

    def __init__(self, facebook_config, settings):
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests is not installed. Run: pip install requests")

        cfg = facebook_config or {}
        self.page_id_env = cfg.get("page_id_env_var", "RR_FACEBOOK_PAGE_ID")
        self.token_env = cfg.get("page_token_env_var", "RR_FACEBOOK_PAGE_TOKEN")

        self.page_id = os.getenv(self.page_id_env, "").strip()
        self.token = os.getenv(self.token_env, "").strip()

        if not self.page_id or not self.token:
            raise RuntimeError(
                "Facebook Page credentials missing. Set env vars: "
                f"{self.page_id_env}, {self.token_env}"
            )

        self.timeout = int(cfg.get("timeout_seconds", 60))
        self.dev_mode = (settings or {}).get("mode", "dev") == "dev"

    def post_ad(self, ad, caption):
        message = (caption or "").strip()
        destination_url = (ad.get("url") or "").strip()

        if not message:
            return _result(
                False,
                error_type="CONTENT_ERROR",
                detected="Missing caption for Facebook post",
                raw="missing_caption",
            )

        paths = list(ad.get("media_paths", []))
        if ad.get("media_path"):
            paths.insert(0, ad["media_path"])

        media_file = None
        if paths:
            candidate = _resolve_media(paths[0])
            if not candidate.exists() or not candidate.is_file():
                return _result(
                    False,
                    error_type="MEDIA_ERROR",
                    detected=f"Media file not found: {paths[0]}",
                    raw=str(candidate),
                )
            media_file = candidate
            if len(paths) > 1:
                logger.info(
                    "Facebook adapter posts a single image; ignoring %d extra media file(s).",
                    len(paths) - 1,
                )

        if self.dev_mode:
            target = "photo post" if media_file else "text post"
            print(f"[FacebookAdapter] Publishing {target} to Page {self.page_id} via Graph API.")

        try:
            if media_file:
                payload = self._post_photo(media_file, message, destination_url)
            else:
                payload = self._post_feed(message, destination_url)
        except requests.exceptions.RequestException as e:
            return _result(False, error_type="NETWORK_ERROR", detected=str(e), raw=repr(e))

        error = payload.get("error")
        if error:
            kind = self._classify_graph_error(error)
            return _result(
                False,
                error_type=kind,
                detected=error.get("message", "Graph API returned an error."),
                raw=repr(error),
            )

        post_id = payload.get("post_id") or payload.get("id")
        if not post_id:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected="Graph API response contained no post id.",
                raw=repr(payload),
            )

        return _result(True, post_url=f"https://www.facebook.com/{post_id}")

    # ------------------------------------------------------------------ calls

    def _post_photo(self, media_file, message, destination_url):
        caption = message
        if destination_url and destination_url not in caption:
            caption = f"{caption}\n\n{destination_url}".strip()

        url = f"{GRAPH_BASE}/{self.page_id}/photos"
        with open(media_file, "rb") as fh:
            response = requests.post(
                url,
                data={"caption": caption, "published": "true", "access_token": self.token},
                files={"source": (media_file.name, fh)},
                timeout=self.timeout,
            )
        return self._decode(response)

    def _post_feed(self, message, destination_url):
        data = {"message": message, "access_token": self.token}
        if destination_url:
            data["link"] = destination_url

        response = requests.post(f"{GRAPH_BASE}/{self.page_id}/feed", data=data, timeout=self.timeout)
        return self._decode(response)

    @staticmethod
    def _decode(response):
        try:
            return response.json()
        except ValueError:
            return {
                "error": {
                    "message": f"Non-JSON response (HTTP {response.status_code})",
                    "code": -1,
                    "body": response.text[:500],
                }
            }

    # --------------------------------------------------------------- plumbing

    def _classify_graph_error(self, error):
        code = error.get("code")
        try:
            code = int(code)
        except (TypeError, ValueError):
            code = None

        if code in _AUTH_CODES:
            return "AUTH_ERROR"
        if code in _RATE_CODES:
            return "RATE_LIMIT_ERROR"
        if code in _CONTENT_CODES:
            return "CONTENT_ERROR"

        msg = (error.get("message") or "").lower()
        if any(k in msg for k in ("token", "permission", "oauth", "expired")):
            return "AUTH_ERROR"
        if any(k in msg for k in ("rate", "too many", "temporarily blocked", "limit")):
            return "RATE_LIMIT_ERROR"
        if any(k in msg for k in ("duplicate", "invalid parameter", "not allowed")):
            return "CONTENT_ERROR"
        if "photo" in msg or "image" in msg or "upload" in msg:
            return "MEDIA_ERROR"
        return "UNKNOWN_ERROR"
