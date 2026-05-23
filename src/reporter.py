import json
from datetime import date
from .paths import LOGS_DIR


def _log_dir_for_today():
    d = LOGS_DIR / date.today().isoformat()
    d.mkdir(parents=True, exist_ok=True)
    return d


def write_run_json(run):
    path = _log_dir_for_today() / "run.json"
    with path.open("w", encoding="utf-8") as f:
        json.dump(run, f, indent=2)
    return path


def write_report_txt(run):
    path = _log_dir_for_today() / "report.txt"
    lines = []
    status = run.get("final_status", "UNKNOWN")
    successes = run.get("successes", 0)
    goal = run.get("daily_goal", 3)
    lines.append(f"Revenant Relay - {status} - {successes}/{goal} Posted")
    lines.append("")
    lines.append(f"Run ID: {run['run_id']}")
    lines.append(f"Date: {run['date']}  Mode: {run['mode']}")
    lines.append(f"Started: {run['started_at']}  Ended: {run.get('ended_at')}")
    lines.append(f"Stop reason: {run.get('stop_reason')}")
    lines.append(f"Successes: {successes}   Failures: {run.get('failures', 0)}")
    lines.append("")

    succeeded = [a for a in run["attempts"] if a["success"]]
    failed = [a for a in run["attempts"] if not a["success"]]

    if succeeded:
        lines.append("Successful posts:")
        for a in succeeded:
            lines.append(f"  - {a['platform']}  ad={a['ad_id']}  tier={a['tier']}  url={a.get('post_url')}")
        lines.append("")

    if failed:
        lines.append("Failed attempts:")
        for a in failed:
            lines.append(f"  - {a['platform']}  ad={a['ad_id']}  tier={a['tier']}")
            lines.append(f"      type={a.get('error_type')}  cause={a.get('likely_cause')}")
            lines.append(f"      fix={a.get('suggested_fix')}")
            if a.get("screenshot_path"):
                lines.append(f"      screenshot={a['screenshot_path']}")
        lines.append("")

    with path.open("w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path


def subject_line(run):
    successes = run.get("successes", 0)
    goal = run.get("daily_goal", 3)
    status = run.get("final_status", "UNKNOWN")
    return f"Revenant Relay - {status} - {successes}/{goal} Posted"
