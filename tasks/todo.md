# Revenant Relay — Task Log

## Session 2026-05-23 — COMPLETE

### Reddit Adapter Wired
- [x] Fixed `_load_disabled()` key mismatch (`"disabled"` → `"disabled_platforms"`, handles object and string formats)
- [x] Created `src/adapter_loader.py` — dispatches to real adapter or falls back to simulator
- [x] Created `src/secret_loader.py` — loads `B:\secrets\revenant-relay.env` at startup, silent if B: not mounted
- [x] Updated `src/main.py` — adapter dispatch, Reddit subreddit selection, `add_reddit_cooldown` on success
- [x] Updated `config/settings.json` — `RR_` prefix env vars, credential blocks for all platforms, removed duplicate discord key
- [x] Fixed `src/platforms/reddit.py` — media_path resolves relative to ROOT; supports refresh_token OR username/password auth
- [x] Fixed `src/cooldowns.py` — defensive guard for old flat-format Reddit entries
- [x] Installed PRAW 7.8.1
- [x] CLAUDE.md updated with current state

### Pending before Reddit goes live
- [ ] Create `B:\secrets\revenant-relay.env` with Reddit credentials
  - `RR_REDDIT_CLIENT_ID` — from reddit.com/prefs/apps (script app)
  - `RR_REDDIT_CLIENT_SECRET` — from same app
  - `RR_REDDIT_USERNAME` / `RR_REDDIT_PASSWORD` — no refresh token needed

## Next Session — Platform Adapters

Priority order per CLAUDE.md: Pinterest → TikTok → Indeed → LinkedIn → X → Facebook → Instagram

All browser-based (Playwright). Pattern: build adapter in `src/platforms/<platform>.py`, register in `src/adapter_loader.py`.
