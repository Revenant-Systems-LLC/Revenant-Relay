import json
import urllib.error
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest

from src.platforms.bluesky import BlueskyAdapter, _BLUESKY_MAX_CHARS


def test_bluesky_credentials_missing(monkeypatch):
    monkeypatch.delenv("RR_BLUESKY_HANDLE", raising=False)
    monkeypatch.delenv("RR_BLUESKY_PASSWORD", raising=False)

    with pytest.raises(RuntimeError) as exc_info:
        BlueskyAdapter({})
    assert "Bluesky credentials missing" in str(exc_info.value)


def test_bluesky_init_successful(monkeypatch):
    monkeypatch.setenv("RR_BLUESKY_HANDLE", "test.bsky.social")
    monkeypatch.setenv("RR_BLUESKY_PASSWORD", "app-pass")

    adapter = BlueskyAdapter({})
    assert adapter.handle == "test.bsky.social"
    assert adapter.password == "app-pass"


def test_bluesky_truncation_without_url():
    long_caption = "A" * 400
    ad = {"id": "RTS-001"}
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("RR_BLUESKY_HANDLE", "test.bsky.social")
    monkeypatch.setenv("RR_BLUESKY_PASSWORD", "app-pass")

    adapter = BlueskyAdapter({})

    # Mock the internal session and createRecord calls
    adapter._create_session = MagicMock(return_value={"accessJwt": "token", "did": "did"})
    adapter._create_record = MagicMock(return_value="https://bsky.app/profile/did/post/post1")

    res = adapter.post_ad(ad, long_caption)
    assert res["success"] is True
    # The truncated text should be exactly 300 chars, ending in "..."
    text_posted = adapter._create_record.call_args[0][2]
    assert len(text_posted) == 300
    assert text_posted.endswith("...")


def test_bluesky_truncation_preserves_url():
    long_caption = "A" * 400
    url = "https://revenantsystems.net"
    ad = {"id": "RTS-001", "url": url}
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setenv("RR_BLUESKY_HANDLE", "test.bsky.social")
    monkeypatch.setenv("RR_BLUESKY_PASSWORD", "app-pass")

    adapter = BlueskyAdapter({})

    adapter._create_session = MagicMock(return_value={"accessJwt": "token", "did": "did"})
    adapter._create_record = MagicMock(return_value="https://bsky.app/profile/did/post/post1")

    res = adapter.post_ad(ad, long_caption)
    assert res["success"] is True

    text_posted = adapter._create_record.call_args[0][2]
    assert len(text_posted) == 300
    assert url in text_posted
    assert text_posted.endswith(url)


def test_bluesky_missing_media_file(monkeypatch):
    monkeypatch.setenv("RR_BLUESKY_HANDLE", "test.bsky.social")
    monkeypatch.setenv("RR_BLUESKY_PASSWORD", "app-pass")

    adapter = BlueskyAdapter({})
    ad = {"id": "RTS-001", "media_path": "non-existent-image-path.png"}
    res = adapter.post_ad(ad, "Caption")
    assert res["success"] is False
    assert res["error_type"] == "MEDIA_ERROR"
    assert "Media file not found" in res["detected_issue"]


@pytest.mark.parametrize("status, body_text, expected_err", [
    (401, "Invalid password", "AUTH_ERROR"),
    (403, "Access denied", "AUTH_ERROR"),
    (429, "Too many requests", "RATE_LIMIT_ERROR"),
    (400, "post is too long", "CONTENT_ERROR"),
    (400, "blob size is too big", "MEDIA_ERROR"),
    (500, "Server error", "PLATFORM_AUTOMATION_ERROR"),
])
def test_bluesky_http_error_classification(monkeypatch, status, body_text, expected_err):
    monkeypatch.setenv("RR_BLUESKY_HANDLE", "test.bsky.social")
    monkeypatch.setenv("RR_BLUESKY_PASSWORD", "app-pass")

    adapter = BlueskyAdapter({})

    # Mock urllib.request.urlopen to throw HTTPError
    fp = MagicMock()
    fp.read.return_value = body_text.encode("utf-8")
    exc = urllib.error.HTTPError("url", status, "msg", {}, fp)

    adapter._create_session = MagicMock(side_effect=exc)

    res = adapter.post_ad({"id": "RTS-001"}, "Test")
    assert res["success"] is False
    assert res["error_type"] == expected_err
