import os
from pathlib import Path

_SECRETS_FILE = Path(r"B:\secrets\revenant-relay.env")


def load_secrets():
    """
    Load secrets from B:\\secrets\\revenant-relay.env into os.environ.
    Fails silently if B: is not mounted or the file doesn't exist — adapters
    will fall back to the simulator when credentials are missing.
    """
    if not _SECRETS_FILE.exists():
        return

    with _SECRETS_FILE.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, _, value = line.partition("=")
            key = key.strip()
            value = value.strip()
            if key:
                os.environ[key] = value
