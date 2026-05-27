import os
import json
import mimetypes
import urllib.request
import urllib.error
from datetime import datetime, timezone
from pathlib import Path

_BLUESKY_MAX_CHARS = 300

_ERROR_CAUSE = {
    "AUTH_ERROR": "Bluesky authentication failed. Invalid handle or App Password.",
    "MEDIA_ERROR": "Media file missing or Bluesky rejected the blob upload.",
    "CONTENT_ERROR": "Required content was missing or exceeded length constraints.",
    "RATE_LIMIT_ERROR": "Bluesky is temporarily throttling account actions (429).",
    "PLATFORM_AUTOMATION_ERROR": "AT Protocol server returned a bad or unparsable response.",
    "NETWORK_ERROR": "Transient network failure while contacting bsky.social.",
    "UNKNOWN_ERROR": "Could not classify failure reliably.",
}

_ERROR_FIX = {
    "AUTH_ERROR": "Verify RR_BLUESKY_HANDLE and RR_BLUESKY_PASSWORD (must use a secure App Password).",
    "MEDIA_ERROR": "Ensure image is under size limits (max 1MB for standard AT Protocol blobs) and try again.",
    "CONTENT_ERROR": "Shorten the caption copy to fit within Bluesky's 300 character limit.",
    "RATE_LIMIT_ERROR": "Skip Bluesky for this daily run; back off and retry tomorrow.",
    "PLATFORM_AUTOMATION_ERROR": "Investigate protocol schema adjustments or API updates.",
    "NETWORK_ERROR": "Retry once after connection stabilizes.",
    "UNKNOWN_ERROR": "Inspect log error envelope and manually diagnose.",
}

_TRANSIENT_TYPES = {"NETWORK_ERROR"}


def _resolve_media(media_path):
    p = Path(media_path)
    if p.is_absolute():
        return p
    from ..paths import ROOT
    return ROOT / p


def _result(success, post_url=None, error_type=None, detected=None, raw=None):
    return {
        "success": success,
        "error_type": error_type,
        "detected_issue": detected,
        "likely_cause": _ERROR_CAUSE.get(error_type) if error_type else None,
        "suggested_fix": _ERROR_FIX.get(error_type) if error_type else None,
        "raw_error": raw,
        "post_url": post_url,
        "screenshot_path": None,
        "transient": error_type in _TRANSIENT_TYPES if error_type else False,
    }


class BlueskyAdapter:
    def __init__(self, bluesky_config):
        cfg = bluesky_config or {}
        self.handle_env = cfg.get("handle_env_var", "RR_BLUESKY_HANDLE")
        self.password_env = cfg.get("password_env_var", "RR_BLUESKY_PASSWORD")

        self.handle = os.getenv(self.handle_env, "").strip()
        self.password = os.getenv(self.password_env, "").strip()

        if not self.handle or not self.password:
            raise RuntimeError(
                "Bluesky credentials missing. Set env vars: "
                f"{self.handle_env}, {self.password_env}"
            )

    def post_ad(self, ad, caption):
        """
        Post ad update to Bluesky. Returns a standard success/failure result dict.
        Supports text/link updates and image uploads.
        """
        url = (ad.get("url") or "").strip()
        text = (caption or "").strip()

        if url and url not in text:
            text = f"{text}\n\n{url}"

        # Truncate cleanly while preserving the URL if present
        if len(text) > _BLUESKY_MAX_CHARS:
            if url and url in text:
                suffix = f"\n\n{url}"
                allowed_prefix_len = _BLUESKY_MAX_CHARS - len(suffix) - 3  # for "..."
                if allowed_prefix_len > 0:
                    text = f"{caption[:allowed_prefix_len]}...{suffix}"
                else:
                    text = url[:_BLUESKY_MAX_CHARS]
            else:
                text = f"{caption[:297]}..."

        if not text:
            return _result(
                False,
                error_type="CONTENT_ERROR",
                detected="Post text content is empty.",
                raw="empty_text"
            )

        media_path = ad.get("media_path")
        resolved = None
        if media_path:
            resolved = _resolve_media(media_path)
            if not resolved.exists() or not resolved.is_file():
                return _result(
                    False,
                    error_type="MEDIA_ERROR",
                    detected=f"Media file not found: {media_path}",
                    raw=str(resolved)
                )

        try:
            # 1. Create AT Protocol Session
            session = self._create_session()
            access_token = session["accessJwt"]
            did = session["did"]

            # 2. Upload image blob if present
            embed = None
            if resolved:
                blob = self._upload_blob(access_token, resolved)
                embed = {
                    "$type": "app.bsky.embed.images",
                    "images": [
                        {
                            "alt": ad.get("title") or "Revenant Systems Ad",
                            "image": blob
                        }
                    ]
                }

            # 3. Create post record
            post_url = self._create_record(access_token, did, text, embed)
            return _result(True, post_url=post_url)

        except urllib.error.HTTPError as e:
            return self._classify_http_error(e)
        except Exception as e:
            return _result(
                False,
                error_type="NETWORK_ERROR",
                detected=f"Network error contacting Bluesky: {e}",
                raw=repr(e)
            )

    def _create_session(self):
        url = "https://bsky.social/xrpc/com.atproto.server.createSession"
        body = json.dumps({
            "identifier": self.handle,
            "password": self.password
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))

    def _upload_blob(self, access_token, filepath):
        url = "https://bsky.social/xrpc/com.atproto.repo.uploadBlob"
        mime_type, _ = mimetypes.guess_type(str(filepath))
        if not mime_type:
            mime_type = "application/octet-stream"

        with open(filepath, "rb") as f:
            data = f.read()

        req = urllib.request.Request(
            url,
            data=data,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": mime_type
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode("utf-8"))["blob"]

    def _create_record(self, access_token, did, text, embed=None):
        url = "https://bsky.social/xrpc/com.atproto.repo.createRecord"
        timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        record = {
            "$type": "app.bsky.feed.post",
            "text": text,
            "createdAt": timestamp
        }
        if embed:
            record["embed"] = embed

        body = json.dumps({
            "repo": did,
            "collection": "app.bsky.feed.post",
            "record": record
        }).encode("utf-8")

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json"
            },
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=30) as response:
            resp_data = json.loads(response.read().decode("utf-8"))
            uri = resp_data.get("uri", "")
            # Canonical post URL format: https://bsky.app/profile/<did>/post/<post_id>
            post_id = uri.split("/")[-1] if uri else ""
            return f"https://bsky.app/profile/{did}/post/{post_id}" if post_id else "https://bsky.app/"

    def _classify_http_error(self, e):
        status = e.code
        err_str = ""
        try:
            err_str = e.read().decode("utf-8", errors="ignore")
        except Exception:
            pass

        # Disambiguate AT Protocol specific codes
        if status in (401, 403):
            return _result(
                False,
                error_type="AUTH_ERROR",
                detected=f"Bluesky authentication rejected ({status}). Details: {err_str}",
                raw=f"HTTPError_{status}::{err_str}"
            )
        elif status == 429:
            return _result(
                False,
                error_type="RATE_LIMIT_ERROR",
                detected="Bluesky rate limit exceeded (429).",
                raw=err_str
            )
        elif status == 400:
            if "invalid" in err_str.lower() or "too long" in err_str.lower():
                return _result(
                    False,
                    error_type="CONTENT_ERROR",
                    detected=f"Content schema rejection from Bluesky: {err_str}",
                    raw=err_str
                )
            elif "blob" in err_str.lower() or "size" in err_str.lower():
                return _result(
                    False,
                    error_type="MEDIA_ERROR",
                    detected=f"Media upload rejected by Bluesky: {err_str}",
                    raw=err_str
                )
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected=f"AT Protocol schema error (400): {err_str}",
                raw=err_str
            )
        else:
            return _result(
                False,
                error_type="PLATFORM_AUTOMATION_ERROR",
                detected=f"Bluesky XRPC error ({status}): {err_str}",
                raw=err_str
            )
