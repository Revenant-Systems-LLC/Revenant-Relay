import os
import warnings
from pathlib import Path

# rws-suppress: RWS-PY-011 A:\env is intentional default; overridden by RR_SECRETS_FILE env var; fails silently if absent
# 2026-08-06: was B:\secrets, which stopped existing when that drive was replaced
# and the secrets moved to A:\env under DPAPI. The old path silently found nothing,
# so every adapter fell through to the simulator and reported success for months.
_DEFAULT_SECRETS_DIR = Path(r"A:\env")
_DEFAULT_DPAPI_FILE = _DEFAULT_SECRETS_DIR / "revenant-relay.dpapi"
_DEFAULT_PLAINTEXT_FILE = _DEFAULT_SECRETS_DIR / "revenant-relay.env"
_SECRETS_ENV_VAR = "RR_SECRETS_FILE"


def _secrets_file_path() -> Path:
    configured = os.getenv(_SECRETS_ENV_VAR)
    if configured:
        return Path(configured).expanduser()
    if _DEFAULT_DPAPI_FILE.exists():
        return _DEFAULT_DPAPI_FILE
    return _DEFAULT_PLAINTEXT_FILE


def _load_env_text(text: str) -> None:
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip()
        value = value.strip()
        if key and key not in os.environ:
            os.environ[key] = value


def _load_plaintext_env(path: Path) -> None:
    _load_env_text(path.read_text(encoding="utf-8"))


def _load_dpapi_file(path: Path) -> None:
    from .dpapi_store import read_dpapi_env_file

    _load_env_text(read_dpapi_env_file(path))


def load_secrets() -> None:
    """
    Load secrets from A:\\env into os.environ.

    Priority:
      1. RR_SECRETS_FILE if set (.dpapi or .env)
      2. A:\\env\\revenant-relay.dpapi
      3. A:\\env\\revenant-relay.env (plaintext fallback only)

    Fails silently if nothing exists — adapters fall back to the simulator.
    """
    secrets_file = _secrets_file_path()
    if not secrets_file.exists():
        return

    try:
        if secrets_file.suffix.lower() == ".dpapi":
            _load_dpapi_file(secrets_file)
            return

        if secrets_file.suffix.lower() == ".env":
            dpapi_sibling = secrets_file.with_suffix(".dpapi")
            if dpapi_sibling.exists():
                _load_dpapi_file(dpapi_sibling)
                return
            warnings.warn(
                f"Loading plaintext secrets from {secrets_file}. "
                "Encrypt it to a .dpapi container beside it instead.",
                stacklevel=2,
            )
            _load_plaintext_env(secrets_file)
            return

        try:
            _load_dpapi_file(secrets_file)
        except (ValueError, OSError):
            _load_plaintext_env(secrets_file)
    except OSError:
        return
