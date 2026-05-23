import json
from pathlib import Path
from .paths import ADS_DIR


def load_all_ads():
    """Walk ads/ and return every ad.json found. Includes unapproved ads."""
    ads = []
    for ad_json in ADS_DIR.rglob("ad.json"):
        with ad_json.open("r", encoding="utf-8") as f:
            data = json.load(f)
        data["_source_path"] = str(ad_json)
        ads.append(data)
    return ads


def load_approved_ads():
    """Only ads with approved == true."""
    return [a for a in load_all_ads() if a.get("approved") is True]


def ads_for_platform(ads, platform):
    """Filter ads to those allowed on a given platform."""
    return [a for a in ads if platform in a.get("allowed_platforms", [])]


def caption_for(ad, platform):
    """Platform-specific caption if present, else default. Never generated."""
    overrides = ad.get("platform_captions", {})
    return overrides.get(platform, ad.get("caption", ""))
