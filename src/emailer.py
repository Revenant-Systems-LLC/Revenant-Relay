import os
import smtplib
import ssl
from email.utils import parseaddr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_report(run_log, settings, mode):
    """
    Send final email report after run completes.
    Only sends if email config exists and credentials are available in env vars.
    Fails gracefully if email sending fails — logs error but doesn't crash engine.
    """
    run_log["email_report"] = {
        "enabled": bool(settings.get("email")),
        "attempted": False,
        "sent": False,
        "error": None,
        "recipient": None,
    }

    if not settings.get("email"):
        return run_log["email_report"]

    email_config = settings["email"]
    smtp_host = email_config.get("smtp_host")
    smtp_port = email_config.get("smtp_port", 587)
    sender_email_var = email_config.get("sender_email_env_var")
    sender_password_var = email_config.get("sender_password_env_var")
    recipient_email = email_config.get("recipient_email")
    subject_prefix = email_config.get("subject_prefix", "Revenant Relay")
    use_ssl = email_config.get("use_ssl", smtp_port == 465)

    run_log["email_report"]["recipient"] = recipient_email

    # Load credentials from env vars
    sender_email = os.getenv(sender_email_var)
    sender_password = os.getenv(sender_password_var)

    if not sender_email or not sender_password or not recipient_email:
        print(
            f"[Email] Skipping email: missing credentials "
            f"({sender_email_var}={bool(sender_email)}, "
            f"{sender_password_var}={bool(sender_password)}, "
            f"recipient={recipient_email})"
        )
        run_log["email_report"]["error"] = "missing_credentials_or_recipient"
        return run_log["email_report"]

    if not _is_valid_email(recipient_email):
        print(f"[Email] Skipping email: invalid recipient '{recipient_email}'")
        run_log["email_report"]["error"] = "invalid_recipient_email"
        return run_log["email_report"]

    try:
        # Build email
        status = run_log.get("final_status", "UNKNOWN")
        successes = run_log.get("successes", 0)
        goal = run_log.get("daily_goal", 3)
        subject = f"{subject_prefix} - {status} - {successes}/{goal} Posted"

        # Email body: human-readable report
        body = _build_report_body(run_log)

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = recipient_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Send via encrypted SMTP transport.
        run_log["email_report"]["attempted"] = True
        tls_context = ssl.create_default_context()
        if use_ssl:
            with smtplib.SMTP_SSL(smtp_host, smtp_port, context=tls_context) as server:
                server.login(sender_email, sender_password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(smtp_host, smtp_port) as server:
                server.ehlo()
                server.starttls(context=tls_context)
                server.ehlo()
                server.login(sender_email, sender_password)
                server.send_message(msg)

        print(f"[Email] Report sent to {recipient_email} (subject: {subject})")
        run_log["email_report"]["sent"] = True
        return run_log["email_report"]

    except Exception as e:
        print(f"[Email] Failed to send report: {e}")
        run_log["email_report"]["error"] = str(e)
        return run_log["email_report"]


def _is_valid_email(value):
    _, parsed = parseaddr(value or "")
    return bool(parsed and "@" in parsed and "." in parsed.split("@")[-1])


def _build_report_body(run_log):
    """Generate human-readable report body from run_log."""
    lines = []

    status = run_log.get("final_status", "UNKNOWN")
    successes = run_log.get("successes", 0)
    goal = run_log.get("daily_goal", 3)
    lines.append(f"Revenant Relay - {status} - {successes}/{goal} Posted")
    lines.append("")
    lines.append(f"Run ID: {run_log['run_id']}")
    lines.append(f"Date: {run_log['date']}  Mode: {run_log['mode']}")
    lines.append(f"Started: {run_log['started_at']}  Ended: {run_log.get('ended_at')}")
    lines.append(f"Stop reason: {run_log.get('stop_reason')}")
    lines.append(f"Successes: {successes}   Failures: {run_log.get('failures', 0)}")
    lines.append("")

    attempts = run_log.get("attempts", [])
    succeeded = [a for a in attempts if a.get("success")]
    failed = [a for a in attempts if not a.get("success")]

    if succeeded:
        lines.append("Successful posts:")
        for a in succeeded:
            lines.append(
                f"  - {a['platform']}  ad={a['ad_id']}  tier={a['tier']}  url={a.get('post_url')}"
            )
        lines.append("")

    if failed:
        lines.append("Failed attempts:")
        for a in failed:
            lines.append(f"  - {a['platform']}  ad={a['ad_id']}  tier={a['tier']}")
            lines.append(
                f"      type={a.get('error_type')}  cause={a.get('likely_cause')}"
            )
            lines.append(f"      fix={a.get('suggested_fix')}")
            if a.get("screenshot_path"):
                lines.append(f"      screenshot={a['screenshot_path']}")
        lines.append("")

    return "\n".join(lines)
