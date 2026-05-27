import json
import random
from .paths import PLATFORMS_FILE, DISABLED_FILE
from .history import platforms_used_yesterday


def _load_platforms_config():
    try:
        with PLATFORMS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f).get("platforms", {})
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return {}


def _load_disabled():
    try:
        with DISABLED_FILE.open("r", encoding="utf-8") as f:
            entries = json.load(f).get("disabled", [])
        return {e["platform"] if isinstance(e, dict) else e for e in entries}
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return set()


def build_tiers():
    """
    Tier 1: not used yesterday + not hard-disabled.
    Tier 2: failed yesterday.
    Tier 3A: succeeded yesterday (fallback, must use different ad).
    Tier 3B: succeeded yesterday with no alternate ad available (caller decides).
    Hard disabled: skipped entirely.
    """
    cfg = _load_platforms_config()
    disabled_manual = _load_disabled()

    succeeded, failed, attempted = platforms_used_yesterday()

    enabled = {p for p, v in cfg.items() if v.get("enabled") and p not in disabled_manual}

    tier1 = sorted(enabled - attempted)
    tier2 = sorted(enabled & failed)
    tier3a = sorted(enabled & succeeded)

    random.shuffle(tier1)
    random.shuffle(tier2)
    random.shuffle(tier3a)

    return {
        "tier1": tier1,
        "tier2": tier2,
        "tier3a": tier3a,
        "disabled": sorted(disabled_manual | (set(cfg.keys()) - enabled)),
    }


def select_next_platform(tiers, used_today, unavailable_today):
    """
    Pick the next platform to attempt.
    Walks tier1 -> tier2 -> tier3a, random inside each tier, excluding any
    platform already used or marked unavailable for today.
    Returns (platform, tier_label) or (None, None) if exhausted.
    """
    for label in ("tier1", "tier2", "tier3a"):
        candidates = [p for p in tiers[label] if p not in used_today and p not in unavailable_today]
        if candidates:
            return random.choice(candidates), label
    return None, None
