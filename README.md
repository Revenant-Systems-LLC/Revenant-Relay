# Revenant Relay

Ad distribution bot for Revenant Systems LLC.

## What it is
Posts human-approved ads across selected social platforms on a rotating schedule. Replaces Relayed.social with a self-hosted, free, runs-on-Dave's-machine alternative.

## What it is not
- Not an ad generator. No AI-generated public-facing copy. Ever.
- Not an agent. No LLM at runtime. No persona. No reasoning loop.
- Not a social platform. Not a content engine. Not a growth suite.

## Architecture
- **Runtime:** pure Python. No agent framework.
- **State:** JSON files on disk in `data/`.
- **Operator surface:** Discord. Ads live in `mimirs-well`. Reports land in `skalds-log`.
- **Browser automation:** Playwright (added after engine works).
- **Schedule:** Windows Task Scheduler triggers once daily.

## Platforms (v1 target)
Facebook, Instagram, X, Reddit, Pinterest, TikTok, LinkedIn, Indeed.

## Daily goal
3 successful posts per scheduled run. Stops at 3 successes, 3 consecutive failures, or no eligible platform/ad combinations.

## Run modes
- **dev** — visible browser, local report, email/Discord optional.
- **scheduled** — headless, always reports to Discord, screenshots on failure.

## Project layout
```
Revenant-Relay/
  ads/         approved ad library (image + ad.json per ad)
  config/      platforms.json, settings.json
  data/        run_history.json, platform_cooldowns.json, disabled_platforms.json
  logs/        YYYY-MM-DD/ run.json, report.txt, failures/*.png
  src/         engine code
    platforms/ one adapter per platform
```

## Status
v0.0 — scaffolded. Engine not yet written.


## Pinterest adapter environment
Set these environment variables for real Pinterest posting:
- `RR_PINTEREST_USERNAME`
- `RR_PINTEREST_PASSWORD`
- Optional: `RR_PINTEREST_BOARD_NAME`

## TikTok adapter environment
Set these environment variables for TikTok adapter initialization:
- `RR_TIKTOK_USERNAME`
- `RR_TIKTOK_PASSWORD`
- Optional safety gate: `RR_TIKTOK_ENABLE_AUTOMATION` (default disabled; set to `true` to attempt browser automation bootstrap)

## LinkedIn adapter environment
Set these environment variables for real LinkedIn posting:
- `RR_LINKEDIN_USERNAME`
- `RR_LINKEDIN_PASSWORD`
- `RR_LINKEDIN_POST_TARGET` (`company` or `profile`; `company` recommended)
- `RR_LINKEDIN_COMPANY_PAGE_URL` (required when target is `company`)

## X adapter environment
Set these environment variables for real X posting:
- `RR_X_USERNAME`
- `RR_X_PASSWORD`