"""Load DPAPI .dpapi secret containers from A:\\env."""

from __future__ import annotations

import base64
import json
from pathlib import Path
from typing import Any

from .dpapi_decrypt import decrypt_bytes

_FORMAT_VERSION = 1
_SCHEME = "windows-dpapi-current-user"


def read_dpapi_env_file(path: Path) -> str:
    payload: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("version") != _FORMAT_VERSION:
        raise ValueError(f"Unsupported DPAPI file version: {payload.get('version')!r}")
    if payload.get("scheme") != _SCHEME:
        raise ValueError(f"Unsupported DPAPI scheme: {payload.get('scheme')!r}")
    encrypted_b64 = payload.get("encrypted")
    if not isinstance(encrypted_b64, str):
        raise ValueError("DPAPI file missing encrypted payload")
    ciphertext = base64.b64decode(encrypted_b64.encode("ascii"))
    return decrypt_bytes(ciphertext).decode("utf-8")
