import argparse
import json
import sys
from datetime import datetime
import time
import random
from pathlib import Path

# Allow running as `python src/main.py` from the repo root.
if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    _IMPORT_PREFIX = "src"
else:
    _IMPORT_PREFIX = __package__

paths = __import__(f"{_IMPORT_PREFIX}.paths", fromlist=["SETTINGS_FILE"])
cooldowns_mod = __import__(
    f"{_IMPORT_PREFIX}.cooldowns",
    fromlist=["load_clean_cooldowns", "add_cooldown", "add_reddit_cooldown"],
)
platform_selector_mod = __import__(
    f"{_IMPORT_PREFIX}.platform_selector", fromlist=["build_tiers", "select_next_platform"]
)
ad_selector_mod = __import__(f"{_IMPORT_PREFIX}.ad_selector", fromlist=["select_ad_for_platform"])
simulator_mod = __import__(f"{_IMPORT_PREFIX}.simulator", fromlist=["simulate_post"])
history_mod = __import__(f"{_IMPORT_PREFIX}.history", fromlist=["new_run", "append_run"])
reporter_mod = __import__(
    f"{_IMPORT_PREFIX}.reporter", fromlist=["write_run_json", "write_report_txt", "subject_line"]
)
ad_loader_mod = __import__(f"{_IMPORT_PREFIX}.ad_loader", fromlist=["caption_for"])
emailer_mod = __import__(f"{_IMPORT_PREFIX}.emailer", fromlist=["send_email_report"])
adapter_loader_mod = __import__(f"{_IMPORT_PREFIX}.adapter_loader", fromlist=["load_adapter"])
secret_loader_mod = __import__(f"{_IMPORT_PREFIX}.secret_loader", fromlist=["load_secrets"])

SETTINGS_FILE = paths.SETTINGS_FILE
load_clean_cooldowns = cooldowns_mod.load_clean_cooldowns
add_cooldown = cooldowns_mod.add_cooldown
add_reddit_cooldown = cooldowns_mod.add_reddit_cooldown
build_tiers = platform_selector_mod.build_tiers
select_next_platform = platform_selector_mod.select_next_platform
select_ad_for_platform = ad_selector_mod.select_ad_for_platform
simulate_post = simulator_mod.simulate_post
new_run = history_mod.new_run
append_run = history_mod.append_run
write_run_json = reporter_mod.write_run_json
write_report_txt = reporter_mod.write_report_txt
subject_line = reporter_mod.subject_line
caption_for = ad_loader_mod.caption_for
send_email_report = emailer_mod.send_email_report
load_adapter = adapter_loader_mod.load_adapter
load_secrets = secret_loader_mod.load_secrets


def load_settings():
    with SETTINGS_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def run(mode):
    load_secrets()
    settings = load_settings()
    settings["mode"] = mode
    goal = settings.get("daily_post_goal", 3)
    max_consec = settings.get("max_consecutive_failures", 3)
    cooldown_days = settings.get("cooldown_days", 7)
    
    mode_settings = settings.get(f"{mode}_mode", {})
    startup_range = mode_settings.get("startup_delay_minutes", [0, 0])
    if startup_range[1] > 0:
        delay_min = random.uniform(startup_range[0], startup_range[1])
        delay_sec = delay_min * 60
        print(f"[Startup] Waiting {delay_min:.1f} minutes before starting...")
        time.sleep(delay_sec)

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

        # Between-posts delay
        if run_log["attempts"]:
            between_range = mode_settings.get("between_posts_delay_minutes", [0, 0])
            if between_range[1] > 0:
                delay_min = random.uniform(between_range[0], between_range[1])
                delay_sec = delay_min * 60
                print(f"[Delay] Waiting {delay_min:.1f} minutes before next post...")
                time.sleep(delay_sec)

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
        elif mode == "scheduled":
            # Production never fabricates a success. If the adapter cannot load
            # — missing dependency, missing credentials, no adapter at all —
            # that is a real failure and must be reported as one. Simulating
            # here is what let a run email "COMPLETE - 3/3 Posted" while
            # nothing had been posted.
            result = {
                "success": False,
                "error_type": "ADAPTER_UNAVAILABLE",
                "detected_issue": f"No usable adapter loaded for {platform}.",
                "likely_cause": (
                    "Adapter module missing, a dependency is not installed, or the "
                    "platform's credentials are absent from the secret store."
                ),
                "suggested_fix": (
                    f"Install the adapter's dependencies and set the RR_{platform.upper()}_* "
                    f"credentials, or set {platform} to enabled=false in config/platforms.json."
                ),
                "raw_error": f"ADAPTER_UNAVAILABLE::{platform}",
                "post_url": None,
                "screenshot_path": None,
                "transient": False,
                "simulated": False,
            }
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
            "simulated": bool(result.get("simulated", False)),
        }
        run_log["attempts"].append(attempt)

        if result["success"]:
            run_log["successes"] += 1
            consecutive_failures = 0
            used_today.add(platform)
            if attempt["simulated"]:
                # A simulated post must never write production state. Cooldowns
                # would block a real ad for a week over a post that never
                # happened, and history drives tomorrow's tier selection.
                run_log["simulated_successes"] = run_log.get("simulated_successes", 0) + 1
                continue
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

    mode_settings = settings.get(f"{mode}_mode", {})
    if mode_settings.get("send_email_report"):
        run_log["email_report"] = send_email_report(run_log, settings, mode)
    else:
        run_log["email_report"] = {
            "attempted": False,
            "sent": False,
            "reason": "disabled",
        }

    append_run(run_log)
    json_path = write_run_json(run_log)
    txt_path = write_report_txt(run_log)

    print(subject_line(run_log))
    print(f"Stop reason: {run_log['stop_reason']}")
    print(f"Run log: {json_path}")
    print(f"Report:  {txt_path}")

    email_status = run_log.get("email_report", {})
    if email_status.get("attempted"):
        if email_status.get("sent"):
            print("[Email] Report status: sent")
        else:
            print(f"[Email] Report status: not sent ({email_status.get('error')})")

    return run_log


def main():
    parser = argparse.ArgumentParser(description="Revenant Relay")
    parser.add_argument("--mode", choices=["dev", "scheduled"], default="dev")
    args = parser.parse_args()
    run(args.mode)


if __name__ == "__main__":
    main()
