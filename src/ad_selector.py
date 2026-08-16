import random
from .ad_loader import load_approved_ads, ads_for_platform
from .cooldowns import ads_in_cooldown
from .history import successful_ad_on_platform_yesterday


def select_ad_for_platform(platform, tier_label, cooldown_buckets):
    """
    Pick a random eligible ad for a platform.
    Filters: approved, allowed on this platform, not in cooldown.
    Tier 3A extra rule: must differ from the ad that succeeded on this
    platform yesterday.
    Returns the ad dict or None if nothing eligible.
    """
    pool = ads_for_platform(load_approved_ads(), platform)
    blocked = ads_in_cooldown(cooldown_buckets, platform)
    eligible = [a for a in pool if a["id"] not in blocked]

    if platform == "reddit":
        # An ad with no target_subreddits makes RedditAdapter.select_subreddit
        # return None, and main.py then drops Reddit for the whole run without
        # writing an attempt record — one bad ad silently kills the channel for
        # the day. Treat "nowhere to post it" as "not eligible" instead.
        eligible = [a for a in eligible if a.get("target_subreddits")]

    if tier_label == "tier3a":
        yesterday_ad = successful_ad_on_platform_yesterday(platform)
        if yesterday_ad:
            eligible = [a for a in eligible if a["id"] != yesterday_ad]

    if not eligible:
        return None
    return random.choice(eligible)
