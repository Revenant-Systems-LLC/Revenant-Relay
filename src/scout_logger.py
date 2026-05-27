import json
from datetime import datetime
from .paths import WARM_LEADS_FILE


def _load_leads():
    """Load leads from the local warm leads file, falling back cleanly to an empty list."""
    try:
        if not WARM_LEADS_FILE.exists():
            return []
        with WARM_LEADS_FILE.open("r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("leads", [])
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return []


def _save_leads(leads):
    """Persist leads list back to the local warm leads file."""
    try:
        WARM_LEADS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with WARM_LEADS_FILE.open("w", encoding="utf-8") as f:
            json.dump({"leads": leads}, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Scout] Warning: Failed to save warm leads: {e}")


def log_leads(new_leads):
    """
    Append new leads to data/warm_leads.json, strictly deduplicating by post_url.
    Returns the count of successfully added new unique leads.
    """
    if not new_leads:
        return 0

    existing_leads = _load_leads()
    existing_urls = {
        lead["post_url"] for lead in existing_leads 
        if isinstance(lead, dict) and lead.get("post_url")
    }

    added_count = 0
    now_str = datetime.now().isoformat(timespec="seconds")

    for lead in new_leads:
        if not isinstance(lead, dict):
            continue
        
        post_url = lead.get("post_url", "").strip()
        if not post_url:
            continue

        if post_url in existing_urls:
            continue

        # Format and append lead
        scouted_lead = {
            "platform": lead.get("platform", "unknown"),
            "keyword": lead.get("keyword", "unknown"),
            "author": lead.get("author", "unknown"),
            "post_content": lead.get("post_content", "").strip(),
            "post_url": post_url,
            "discovered_at": now_str
        }
        
        existing_leads.append(scouted_lead)
        existing_urls.add(post_url)
        added_count += 1

    if added_count > 0:
        _save_leads(existing_leads)
        print(f"[Scout] Logged {added_count} new unique warm leads to {WARM_LEADS_FILE.name}")
    else:
        print("[Scout] No new unique leads discovered.")

    return added_count
