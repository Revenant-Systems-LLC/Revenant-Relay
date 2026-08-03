import logging
import os
import time
from pathlib import Path
from urllib.parse import quote

logger = logging.getLogger(__name__)

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

from ..paths import ROOT

GRAPH_VERSION = "v21.0"
GRAPH_BASE = f"https://graph.facebook.com/{GRAPH_VERSION}"

# Instagram will only fetch JPEG for image containers. PNG is rejected, and the
# error it returns is unhelpful, so we check locally and fail with a real reason.
_ACCEPTED_SUFFIXES = {".jpg", ".jpeg"}

_ERROR_CAUSE = {
    "AUTH_ERROR": "Instagram token is invalid or expired, or the account is not a Business account linked to the Page.",
    "MEDIA_ERROR": "Image missing locally, not reachable at its public URL, wrong format, or rejected by Instagram.",
    "CONTENT_ERROR": "Caption exceeded limits or Instagram rejected the content.",
    "RATE_LIMIT_ERROR": "Instagram publishing limit reached (50 posts per rolling 24 hours) or the app is throttled.",
    "PLATFORM_AUTOMATION_ERROR": "Container was created but never reached FINISHED, or the publish response had no media id.",
    "NETWORK_ERROR": "Transient network failure while calling the Graph API.",
    "UNKNOWN_ERROR": "Could not classify failure reliably.",
}

_ERROR_FIX = {
    "AUTH_ERROR": (
        "Confirm the Instagram account is a Business account linked to the Revenant Systems Page, "
        "then regenerate the Page token with instagram_basic and instagram_content_publish and "
        "update RR_INSTAGRAM_TOKEN."
    ),
    "MEDIA_ERROR": (
        "Instagram fetches the image over HTTPS and only accepts JPEG. Publish a .jpg to the public "
        "media folder and confirm RR_INSTAGRAM_MEDIA_BASE_URL returns HTTP 200 for it."
    ),
    "CONTENT_ERROR": "Trim the caption below 2200 characters and keep hashtags under 30.",
    "RATE_LIMIT_ERROR": "Stop Instagram attempts for 24 hours. Check GET /{ig-user-id}/content_publishing_limit.",
    "PLATFORM_AUTOMATION_ERROR": "Inspect raw_error. Re-running creates a fresh container; stale ones expire after 24 hours.",
    "NETWORK_ERROR": "Retry once; likely transient connectivity issue.",
    "UNKNOWN_ERROR": "Inspect raw_error for the Graph API error payload.",
}

_TRANSIENT_TYPES = {"NETWORK_ERROR"}

_AUTH_CODES = {102, 190, 200, 210, 2500}
_RATE_CODES = {4, 17, 25, 32, 341, 613}
_CONTENT_CODES = {100, 352}
_MEDIA_CODES = {9004, 2207003, 2207004, 2207020, 2207026, 2207027, 2207028, 2207032, 2207052}

# Caption ceiling Instagram enforces.
_CAPTION_MAX = 2200


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


class InstagramAdapter:
    """
    Publishes an approved ad to an Instagram Business account via the official
    Content Publishing API. No browser, no stored password.

    THE CONSTRAINT THAT SHAPES THIS ADAPTER:
    Instagram does not accept a file upload. The container endpoint takes an
    `image_url` and Instagram's servers fetch it. So every ad image must already
    be published somewhere publicly reachable over HTTPS before this runs.
    Relay's ads are local PNG files, so two things must happen outside this code:
      1. The image is uploaded to a public folder on revenantsystems.net
      2. It is a JPEG, because Instagram rejects PNG for image containers
    This adapter checks both locally and returns a real MEDIA_ERROR rather than
    letting Instagram answer with something cryptic.

    Env vars:
      RR_INSTAGRAM_USER_ID         Instagram Business account id (not the Page id)
      RR_INSTAGRAM_TOKEN           Page access token with instagram_content_publish
      RR_INSTAGRAM_MEDIA_BASE_URL  public HTTPS base, e.g. https://revenantsystems.net/ad-media/

    Publishing is two calls: create a container, then publish it. Containers are
    polled until FINISHED because Instagram processes them asynchronously.
    """

    def __init__(self, instagram_config, settings):
        if not REQUESTS_AVAILABLE:
            raise RuntimeError("requests is not installed. Run: pip install requests")

        cfg = instagram_config or {}
        self.user_id_env = cfg.get("user_id_env_var", "RR_INSTAGRAM_USER_ID")
        self.token_env = cfg.get("token_env_var", "RR_INSTAGRAM_TOKEN")
        self.base_url_env = cfg.get("media_base_url_env_var", "RR_INSTAGRAM_MEDIA_BASE_URL")

        self.user_id = os.getenv(self.user_id_env, "").strip()
        self.token = os.getenv(self.token_env, "").strip()
        self.media_base_url = os.getenv(self.base_url_env, "").strip()

        if not self.user_id or not self.token:
            raise RuntimeError(
                "Instagram credentials missing. Set env vars: "
                f"{self.user_id_env}, {self.token_env}"
            )
        if not self.media_base_url:
            raise RuntimeError(
                f"Instagram needs a public image host. Set {self.base_url_env} to the HTTPS base URL "
                "of a folder where ad images are published, e.g. https://revenantsystems.net/ad-media/"
            )
        if not self.media_base_url.startswith("https://"):
            raise RuntimeError(
                f"{self.base_url_env} must be HTTPS. Instagram will not fetch over plain HTTP."
            )

        self.timeout = int(cfg.get("timeout_seconds", 60))
        self.poll_attempts = int(cfg.get("container_poll_attempts", 10))
        self.poll_delay = int(cfg.get("container_poll_seconds", 3))
        self.dev_mode = (settings or {}).get("mode", "dev") == "dev"

    def post_ad(self, ad, caption):
        caption_text = (caption or "").strip()
        destination_url = (ad.get("url") or "").strip()

        if not caption_text:
            return _result(
                False,
                error_type="CONTENT_ERROR",
                detected="Missing caption for Instagram post",
                raw="missing_caption",
            )

        # Instagram captions are not clickable. The link is appended as plain text
        # so the ad still names its destination, but nobody can tap it.
        if destination_url and destination_url not in caption_text:
            caption_text = f"{caption_text}\n\n{destination_url}".strip()

        if len(caption_text) > _CAPTION_MAX:
            return _result(
                False,
                error_type="CONTENT_ERROR",
                detected=f"Caption is {len(caption_text)} characters; Instagram allows {_CAPTION_MAX}.",
                raw="caption_too_long",
            )

        paths = list(ad.get("media_paths", []))
        if ad.get("media_path"):
            paths.insert(0, ad["media_path"])

        if not paths:
            return _result(
                False,
                error_type="MEDIA_ERROR",
                detected="Instagram requires an image; this ad declares none.",
                raw="missing_media_path",
            )
        if len(paths) > 1:
            logger.info(
                "Instagram adapter publishes a single image; ignoring %d extra media file(s).",
                len(paths) - 1,
            )

        local_file = _resolve_media(paths[0])
        if not local_file.exists() or not local_file.is_file():
            return _result(
                False,
                error_type="MEDIA_ERROR",
                detected=f"Media file not found: {paths[0]}",
                raw=str(local_file),
            )

        if local_file.suffix.lower() not in _ACCEPTED_SUFFIXES:
            return _result(
                False,
                error_type="MEDIA_ERROR",
                detected=(
                    f"Instagram only accepts JPEG for image posts; this ad supplies "
                    f"{local_file.suffix or 'no extension'}."
                ),
                raw=str(local_file),
            )

        image_url = self.media_base_url.rstrip("/") + "/" + quote(local_file.name)

        reachable, reach_detail = self._check_public_url(image_url)
        if not reachable:
            return _result(
                False,
                error_type="MEDIA_ERROR",
                detected=(
                    f"Image is not publicly reachable at {image_url}. Instagram fetches the file "
                    f"itself, so it must be uploaded before posting. {reach_detail}"
                ),
                raw=reach_detail,
            )

        if self.dev_mode:
            print(f"[InstagramAdapter] Publishing {image_url} to IG user {self.user_id}.")

        # Step 1: container
        try:
            container = self._create_container(image_url, caption_text)
        except requests.exceptions.RequestException as e:
            return _result(False, error_type="NETWORK_ERROR", detected=str(e), raw=repr(e))

        err = container.get("error")
        if err:
            return _result(
                False,
                error_type=self._classify_graph_error(err),
                detected=err.get("message", "Container creation failed."),
                raw=repr(err),
            )

        creation_id = container.get("id")
        if not creation_id:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected="Container response contained no id.",
                raw=repr(container),
            )

        # Step 2: wait for Instagram to finish fetching and processing the image
        ready, status_detail = self._await_container(creation_id)
        if not ready:
            return _result(
                False,
                error_type="MEDIA_ERROR" if "ERROR" in status_detail else "PLATFORM_AUTOMATION_ERROR",
                detected=f"Container {creation_id} did not become publishable. {status_detail}",
                raw=status_detail,
            )

        # Step 3: publish
        try:
            published = self._publish_container(creation_id)
        except requests.exceptions.RequestException as e:
            return _result(False, error_type="NETWORK_ERROR", detected=str(e), raw=repr(e))

        err = published.get("error")
        if err:
            return _result(
                False,
                error_type=self._classify_graph_error(err),
                detected=err.get("message", "Publish failed."),
                raw=repr(err),
            )

        media_id = published.get("id")
        if not media_id:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected="Publish response contained no media id.",
                raw=repr(published),
            )

        permalink = self._fetch_permalink(media_id)
        return _result(True, post_url=permalink or f"https://www.instagram.com/p/{media_id}")

    # ------------------------------------------------------------------ calls

    def _create_container(self, image_url, caption):
        return self._decode(requests.post(
            f"{GRAPH_BASE}/{self.user_id}/media",
            data={"image_url": image_url, "caption": caption, "access_token": self.token},
            timeout=self.timeout,
        ))

    def _publish_container(self, creation_id):
        return self._decode(requests.post(
            f"{GRAPH_BASE}/{self.user_id}/media_publish",
            data={"creation_id": creation_id, "access_token": self.token},
            timeout=self.timeout,
        ))

    def _await_container(self, creation_id):
        """Poll status_code until FINISHED. Returns (ready, detail)."""
        last = "no status returned"
        for attempt in range(self.poll_attempts):
            try:
                payload = self._decode(requests.get(
                    f"{GRAPH_BASE}/{creation_id}",
                    params={"fields": "status_code,status", "access_token": self.token},
                    timeout=self.timeout,
                ))
            except requests.exceptions.RequestException as e:
                return False, f"network failure while polling container: {e}"

            if payload.get("error"):
                return False, f"ERROR from Graph while polling: {payload['error'].get('message')}"

            status = payload.get("status_code") or ""
            last = payload.get("status") or status or last

            if status == "FINISHED":
                return True, "FINISHED"
            if status in ("ERROR", "EXPIRED"):
                return False, f"container status {status}: {last}"

            if attempt < self.poll_attempts - 1:
                time.sleep(self.poll_delay)

        return False, f"still {last} after {self.poll_attempts} polls"

    def _fetch_permalink(self, media_id):
        try:
            payload = self._decode(requests.get(
                f"{GRAPH_BASE}/{media_id}",
                params={"fields": "permalink", "access_token": self.token},
                timeout=self.timeout,
            ))
            return payload.get("permalink")
        except Exception:
            logger.debug("Could not fetch permalink for %s", media_id, exc_info=True)
            return None

    def _check_public_url(self, url):
        """Confirm Instagram will be able to fetch the image before we ask it to."""
        try:
            r = requests.head(url, timeout=20, allow_redirects=True)
            if r.status_code == 405:
                r = requests.get(url, timeout=20, stream=True)
            if r.status_code != 200:
                return False, f"HTTP {r.status_code}"
            ctype = (r.headers.get("Content-Type") or "").lower()
            if "jpeg" not in ctype and "jpg" not in ctype:
                return False, f"served as Content-Type '{ctype}', Instagram needs image/jpeg"
            return True, "HTTP 200"
        except requests.exceptions.RequestException as e:
            return False, f"unreachable: {e}"

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

        subcode = error.get("error_subcode")
        try:
            subcode = int(subcode)
        except (TypeError, ValueError):
            subcode = None

        for candidate in (code, subcode):
            if candidate is None:
                continue
            if candidate in _AUTH_CODES:
                return "AUTH_ERROR"
            if candidate in _RATE_CODES:
                return "RATE_LIMIT_ERROR"
            if candidate in _MEDIA_CODES:
                return "MEDIA_ERROR"
            if candidate in _CONTENT_CODES:
                return "CONTENT_ERROR"

        msg = (error.get("message") or "").lower()
        if any(k in msg for k in ("token", "permission", "oauth", "expired", "business account")):
            return "AUTH_ERROR"
        if any(k in msg for k in ("rate", "too many", "limit reached", "throttl")):
            return "RATE_LIMIT_ERROR"
        if any(k in msg for k in ("media", "image", "aspect", "download", "format", "unsupported")):
            return "MEDIA_ERROR"
        if any(k in msg for k in ("caption", "content", "duplicate")):
            return "CONTENT_ERROR"
        return "UNKNOWN_ERROR"
