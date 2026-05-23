import os
from pathlib import Path

_DEFAULT_SECRETS_FILE = Path("config/secrets.env")
_SECRETS_ENV_VAR = "RR_SECRETS_FILE"


def _secrets_file_path():
    configured = os.getenv(_SECRETS_ENV_VAR)
    if configured:
        return Path(configured).expanduser()
    return _DEFAULT_SECRETS_FILE


def load_secrets():
    """
    Load secrets from RR_SECRETS_FILE or default config/secrets.env into os.environ.
    Fails silently if the file doesn't exist — adapters
    will fall back to the simulator when credentials are missing.
    """
    secrets_file = _secrets_file_path()
    if not secrets_file.exists():
        return

    with secrets_file.open("r", encoding="utf-8") as f:
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
