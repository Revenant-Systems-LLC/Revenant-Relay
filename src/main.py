import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

# Allow running as `python src/main.py` from the repo root.
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from src.paths import SETTINGS_FILE
    from src.cooldowns import load_clean_cooldowns, add_cooldown, add_reddit_cooldown
    from src.platform_selector import build_tiers, select_next_platform
    from src.ad_selector import select_ad_for_platform
    from src.simulator import simulate_post
    from src.history import new_run, append_run
    from src.reporter import write_run_json, write_report_txt, subject_line
    from src.ad_loader import caption_for
    from src.emailer import send_email_report
    from src.adapter_loader import load_adapter
    from src.secret_loader import load_secrets
else:
    from .paths import SETTINGS_FILE
    from .cooldowns import load_clean_cooldowns, add_cooldown, add_reddit_cooldown
    from .platform_selector import build_tiers, select_next_platform
    from .ad_selector import select_ad_for_platform
    from .simulator import simulate_post
    from .history import new_run, append_run
    from .reporter import write_run_json, write_report_txt, subject_line
    from .ad_loader import caption_for
    from .emailer import send_email_report
    from .adapter_loader import load_adapter
    from .secret_loader import load_secrets


def load_settings():
    with SETTINGS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def run(mode):
    load_secrets()
    settings = load_settings()
    goal = settings.get("daily_post_goal", 3)
    max_consec = settings.get("max_consecutive_failures", 3)
    cooldown_days = settings.get("cooldown_days", 7)

    cooldowns = load_clean_cooldowns()
    tiers = build_tiers()
    run_log = new_run(mode)
    run_log["daily_goal"] = goal

    used_today = set()
    unavailable_today = set()
    consecutive_failures = 0
    retried_once = set()

    while True:
        if run_log["successes"] >= goal:
            run_log["final_status"] = "COMPLETE"
            run_log["stop_reason"] = f"Reached daily goal of {goal} successful posts."
            break
        if consecutive_failures >= max_consec:
            run_log["final_status"] = "FAILED" if run_log["successes"] == 0 else "PARTIAL"
            run_log["stop_reason"] = f"Hit {max_consec} consecutive failures."
            break

        platform, tier_label = select_next_platform(tiers, used_today, unavailable_today)
        if platform is None:
            run_log["final_status"] = "PARTIAL" if run_log["successes"] > 0 else "FAILED"
            run_log["stop_reason"] = "No eligible platform/ad combinations remain."
            break

        ad = select_ad_for_platform(platform, tier_label, cooldowns)
        if ad is None:
            unavailable_today.add(platform)
            continue

        caption = caption_for(ad, platform)
        subreddit = None
        adapter = load_adapter(platform, settings)
        if adapter is not None:
            if platform == "reddit":
                subreddit = adapter.select_subreddit(ad, cooldowns)
                if subreddit is None:
                    unavailable_today.add(platform)
                    continue
                result = adapter.post_ad(ad, caption, subreddit)
            else:
                result = adapter.post_ad(ad, caption)
        else:
            result = simulate_post(platform, ad)

        attempt = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "platform": platform,
            "ad_id": ad["id"],
            "tier": tier_label,
            "subreddit": subreddit,
            "caption_used": caption,
            "success": result["success"],
            "error_type": result["error_type"],
            "detected_issue": result["detected_issue"],
            "likely_cause": result["likely_cause"],
            "suggested_fix": result["suggested_fix"],
            "raw_error": result["raw_error"],
            "post_url": result["post_url"],
            "screenshot_path": result["screenshot_path"],
        }
        run_log["attempts"].append(attempt)

        if result["success"]:
            run_log["successes"] += 1
            consecutive_failures = 0
            used_today.add(platform)
            if subreddit is not None:
                expires = add_reddit_cooldown(subreddit, ad["id"], days=cooldown_days)
                cooldowns.setdefault("reddit", {}).setdefault(subreddit, {})[ad["id"]] = expires
            else:
                expires = add_cooldown(platform, ad["id"], days=cooldown_days)
                cooldowns.setdefault(platform, {})[ad["id"]] = expires
            continue

        # failure path
        run_log["failures"] += 1
        if result["transient"] and platform not in retried_once:
            retried_once.add(platform)
            # leave platform available, do not mark unavailable, but count the failure
            consecutive_failures += 1
            continue

        unavailable_today.add(platform)
        consecutive_failures += 1

    run_log["ended_at"] = datetime.now().isoformat(timespec="seconds")
    append_run(run_log)
    json_path = write_run_json(run_log)
    txt_path = write_report_txt(run_log)

    print(subject_line(run_log))
    print(f"Stop reason: {run_log['stop_reason']}")
    print(f"Run log: {json_path}")
    print(f"Report:  {txt_path}")

    mode_settings = settings.get(f"{mode}_mode", {})
    if mode_settings.get("send_email_report"):
        try:
            send_email_report(run_log, settings, mode)
        except Exception as e:
            print(f"[Email] Unexpected error: {e}")

    return run_log


def main():
    parser = argparse.ArgumentParser(description="Revenant Relay")
    parser.add_argument("--mode", choices=["dev", "scheduled"], default="dev")
    args = parser.parse_args()
    run(args.mode)


if __name__ == "__main__":
    main()
