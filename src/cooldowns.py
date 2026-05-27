import json
from datetime import date, timedelta
from .paths import COOLDOWNS_FILE


def _load():
    try:
        with COOLDOWNS_FILE.open("r", encoding="utf-8") as f:
            return json.load(f).get("platform_cooldowns", {})
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return {}


def _save(buckets):
    with COOLDOWNS_FILE.open("w", encoding="utf-8") as f:
        json.dump({"platform_cooldowns": buckets}, f, indent=2)


def load_clean_cooldowns(today=None):
    """Load cooldowns, drop expired entries, persist, return cleaned buckets.

    Flat platforms:  {"linkedin": {"RTS-001": "2026-05-30"}}
    Reddit (nested): {"reddit": {"r/rpg": {"RTS-001": "2026-05-30"}}}
    """
    today = today or date.today()
    buckets = _load()
    cleaned = {}
    for platform, value in buckets.items():
        if platform == "reddit":
            # nested: subreddit -> ad_id -> expires
            kept_subs = {}
            for subreddit, ads in value.items():
                if not isinstance(ads, dict):
                    continue
                kept_ads = {
                    ad_id: expires
                    for ad_id, expires in ads.items()
                    if date.fromisoformat(expires) >= today
                }
                if kept_ads:
                    kept_subs[subreddit] = kept_ads
            if kept_subs:
                cleaned["reddit"] = kept_subs
        else:
            kept = {
                ad_id: expires
                for ad_id, expires in value.items()
                if date.fromisoformat(expires) >= today
            }
            if kept:
                cleaned[platform] = kept
    _save(cleaned)
    return cleaned


def ads_in_cooldown(buckets, platform):
    return set(buckets.get(platform, {}).keys())


def reddit_ads_in_cooldown(buckets, subreddit):
    """Return set of ad_ids on cooldown for a specific subreddit."""
    return set(buckets.get("reddit", {}).get(subreddit, {}).keys())


def add_cooldown(platform, ad_id, days=7, today=None):
    today = today or date.today()
    expires = (today + timedelta(days=days)).isoformat()
    buckets = _load()
    buckets.setdefault(platform, {})[ad_id] = expires
    _save(buckets)
    return expires


def add_reddit_cooldown(subreddit, ad_id, days=7, today=None):
    """Add a per-subreddit cooldown for Reddit posts."""
    today = today or date.today()
    expires = (today + timedelta(days=days)).isoformat()
    buckets = _load()
    buckets.setdefault("reddit", {}).setdefault(subreddit, {})[ad_id] = expires
    _save(buckets)
    return expires
