def load_adapter(platform, settings):
    """
    Return a real adapter instance for the given platform, or None to fall back
    to the simulator. Falls back silently if the adapter is unavailable (missing
    dependency, missing credentials).
    """
    if platform == "reddit":
        try:
            from .platforms.reddit import RedditAdapter
            return RedditAdapter(settings.get("reddit", {}))
        except RuntimeError as e:
            print(f"[Adapter] Reddit unavailable: {e}. Falling back to simulator.")
            return None
    return None
