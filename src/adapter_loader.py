def load_adapter(platform, settings):
    """
    Return a real adapter instance for the given platform, or None to fall back
    to the simulator. Falls back silently if the adapter is unavailable (missing
    dependency, missing credentials).
    """
    if platform == "reddit":
        try:
            from .platforms.reddit import RedditAdapter
            return RedditAdapter(settings.get("reddit", {}), settings)
        except Exception as e:
            print(f"[Adapter] Reddit unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "pinterest":
        try:
            from .platforms.pinterest import PinterestAdapter
            return PinterestAdapter(settings.get("pinterest", {}), settings)
        except Exception as e:
            print(f"[Adapter] Pinterest unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "linkedin":
        try:
            from .platforms.linkedin import LinkedInAdapter
            return LinkedInAdapter(settings.get("linkedin", {}), settings)
        except Exception as e:
            print(f"[Adapter] LinkedIn unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "tiktok":
        try:
            from .platforms.tiktok import TikTokAdapter
            return TikTokAdapter(settings.get("tiktok", {}), settings)
        except Exception as e:
            print(f"[Adapter] TikTok unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "snapchat":
        try:
            from .platforms.snapchat import SnapchatAdapter
            return SnapchatAdapter(settings.get("snapchat", {}), settings)
        except Exception as e:
            print(f"[Adapter] Snapchat unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "x":
        try:
            from .platforms.x import XAdapter
            return XAdapter(settings.get("x", {}), settings)
        except Exception as e:
            print(f"[Adapter] X unavailable: {e}. Falling back to simulator.")
            return None
    if platform == "bluesky":
        try:
            from .platforms.bluesky import BlueskyAdapter
            return BlueskyAdapter(settings.get("bluesky", {}))
        except Exception as e:
            print(f"[Adapter] Bluesky unavailable: {e}. Falling back to simulator.")
            return None
    return None