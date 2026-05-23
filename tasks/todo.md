# Revenant Relay — Task Log

## Session 2026-05-23 — COMPLETE

### Reddit Adapter Wired
- [x] Fixed `_load_disabled()` key mismatch
- [x] Created `src/adapter_loader.py` — dispatches to real adapter or falls back to simulator
- [x] Created `src/secret_loader.py` — loads `B:\secrets\revenant-relay.env` at startup
- [x] Updated `src/main.py` — adapter dispatch, Reddit subreddit selection, `add_reddit_cooldown` on success
- [x] Updated `config/settings.json` — `RR_` prefix env vars, credential blocks for all platforms
- [x] Fixed `src/platforms/reddit.py` — media_path resolves relative to ROOT; supports refresh_token OR username/password auth
- [x] Fixed `src/cooldowns.py` — defensive guard for old flat-format Reddit entries
- [x] Installed PRAW 7.8.1
- [x] CLAUDE.md updated with current state

## Session 2026-05-23 (Afternoon) — COMPLETE

### 5 New Platform Adapters Added (David)
- [x] `src/platforms/pinterest.py` — Playwright-based, image posting, board selection
- [x] `src/platforms/tiktok.py` — Playwright-based, video-only, has `RR_TIKTOK_ENABLE_AUTOMATION` flag
- [x] `src/platforms/linkedin.py` — Playwright-based, company vs profile posting
- [x] `src/platforms/x.py` — Playwright-based, 280 char limit, image/video support
- [x] `src/platforms/snapchat.py` — Playwright-based, Ads Manager flow, video-first
- [x] All adapters registered in `src/adapter_loader.py`
- [x] All env var configs added to `config/settings.json`
- [x] Installed Playwright 1.60.0 + chromium browsers

### Pending
- [ ] Clear test cooldowns (`data/platform_cooldowns.json`) to unblock ad/platform combinations for testing
- [ ] Create real ads (RTS-001/002 are placeholders)
- [ ] Populate `B:\secrets\revenant-relay.env` with credentials
- [ ] Test each adapter with real credentials in dev mode

### Remaining Platforms
- Instagram (with Facebook)
- Indeed
