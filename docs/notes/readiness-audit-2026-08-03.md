# Relay readiness audit — 2026-08-03

Why Relay has not run. Short version: **it was never the platform permissions.** The ad library is
broken and the run loop cannot tell a real post from a simulated one. Both are fixable without
contacting a single platform.

---

## 1. The ad library — 1 of 31 ads is postable today

Relay's hard law: only `approved: true` ads may post. Current state:

| Check | Count |
|---|---|
| Total ads | 31 |
| `approved: true` | **7** |
| Media file missing on disk | 24 |
| `url` empty | 26 |
| `media_path` pointing at the dead `C:\The-Ossuary\` tree (shredded 2026-07-16) | 17 |

### The 7 approved ads, in detail

| Ad | url | media | Verdict |
|---|---|---|---|
| **ALG-001** | ok | `ads/skills/ALG-001/media.png` (839 KB, exists) | **POSTABLE NOW** |
| AI-001 | ok | `ads/skills/AI-001/media.png` — file absent | needs art |
| BUN-001 | ok | `ads/skills/BUN-001/media.png` — file absent | needs art |
| SEC-001 | ok | `ads/skills/SEC-001/media.png` — file absent | needs art |
| SEO-001 | ok | `ads/skills/SEO-001/media.png` — file absent | needs art |
| RTS-004 | MISSING | dead `C:\The-Ossuary\...\Revenant Systems.mp4` | needs url + media |
| RTS-005 | MISSING | `media_path` is an empty string | needs url + media |

The four "needs art" ads all advertise the Skill Packs, which are live products with Stripe links.
They are the closest thing to a shippable campaign.

### Media that exists but is not wired up

Many ads have perfectly good art sitting **inside their own folder** while `ad.json` points somewhere
dead. Repair is mechanical — repoint `media_path` at the local file:

| Ad | ad.json points at (dead) | file actually in the folder |
|---|---|---|
| CS-001 | `C:/The-Ossuary/.../revsys-wordmark-alt.png` | `checklist.png` |
| CS-002 | `C:/Users/Dave/Desktop/algiz2.png` | `comb.png` |
| CS-003 | `C:/Users/Dave/Desktop/algiz22.png` | `matrix_preview.png` |
| CS-004 | `C:/The-Ossuary/.../revsys-wordmark.jpg` | `formatting_rules.mp4` |
| RH-001 / RH-002 / RH-004 | `C:/The-Ossuary/.../Circle4.png` | `comb.png` / `BACKGROUND.mp4` / `comb.png` |
| RTS-001 | `C:/The-Ossuary/.../auto-match.mp4` | `auto-match.mp4` (49 MB, local) |
| RTS-002 | `C:/The-Ossuary/.../rts-header-logo-alt2.png` | `gunmetal_theme1.png` |
| RTS-003 | `C:/The-Ossuary/.../rts-header-logo-alt.png` | `CYBORG_GOLD.png` |
| BUN-002 / BUN-003 / BUN-004 | `C:/The-Ossuary/...` | `CYBORG_GOLD.png` / `bundle_split.mp4` / `fromtheGrave.png` |
| SYS-001 / SYS-002 / SYS-004 | dead paths | `circuit_zoom.mp4` / `manifesto.png` / `anatomy.png` |

Five ads (CS-005, RH-005, RTS-006, BUN-006, SYS-005) already point at working infographics under
`M:\Projects\Revenant-Relay\assets\`. They only lack approval and urls.

Anything genuinely gone can be recovered from `B:\The-Ossuary\Revenant-Systems\Branding-Marketing\revenantsystems-net\assets\`
(186 files, verified present — this is where the shredded `C:` tree moved).

⚠ Zero-byte placeholder files exist at `ads/rts/RTS-001/media.png` and `ads/rts/RTS-002/media.png`.

---

## 2. The run loop cannot report its own failure

`adapter_loader.load_adapter()` returns `None` on any missing credential or dependency, and
[`main.py:127`](src/main.py) silently falls back to `simulate_post()`. The attempt record written to
`run.json` has **no field marking it simulated**. A simulated success still:

- increments `successes` → email reads `Revenant Relay - COMPLETE - 3/3 Posted`
- writes a real 7-day cooldown for an ad that never posted
- appends to `run_history.json`, which builds tomorrow's platform tiers

Only tell-tale: `post_url` contains `.example/simulated/`. This is the same failure class as the
MemPalace outage — a system that cannot announce its own death.

**Fix:** carry a `simulated` flag on every attempt, skip cooldown/history writes for simulated posts,
and state simulation plainly in the report and email subject.

---

## 3. Platform reality — the "permission slog" is mostly imaginary

The split is not "who grants permission," it is "who has an official API."

### Official API — sanctioned, self-service, no human to email

| Platform | Method | Credentials |
|---|---|---|
| **Reddit** | PRAW official API | **present and complete — ready now** |
| **Facebook** | Meta Graph API v21.0, Page posting | needs `RR_FACEBOOK_PAGE_ID`, `RR_FACEBOOK_PAGE_TOKEN` |
| **Instagram** | Meta Graph API v21.0, Business account | needs `RR_INSTAGRAM_USER_ID`, `RR_INSTAGRAM_TOKEN`, `RR_INSTAGRAM_MEDIA_BASE_URL` |

The Facebook and Instagram adapters (written 2026-07-26, still uncommitted) use the Graph API, not
browser automation. They are the *correct* implementations. Both need one Meta developer app and a
long-lived Page token — self-service, no approval letter.

⚠ Instagram fetches media from a **public URL** (hence `MEDIA_BASE_URL`) and accepts **JPEG only**.
Every current ad is `.png` or `.mp4`, so Instagram needs JPEG conversions and public hosting.

### Browser automation — drives a logged-in personal account, against most platforms' terms

| Platform | Credentials |
|---|---|
| LinkedIn | username/password present |
| X | username/password present |
| Snapchat | username/password present |
| Pinterest | absent |
| TikTok | absent (also gated behind `RR_TIKTOK_ENABLE_AUTOMATION`) |

Account-lock risk here is Dave's own accounts, not just the bot. Decision deferred, not made.

### Broken config

- **`indeed`** is `enabled: true` with `adapter: "indeed"`, but no `src/platforms/indeed.py` exists and
  `adapter_loader` has no branch for it. It silently simulates on every selection.
- **`bluesky`** disabled 2026-08-03 by Dave (no account exists). Adapter retained and functional.

---

## 4. Documentation drift

`CLAUDE.md` states secrets live at `B:\secrets\revenant-relay.env`. **That path does not exist.**
The live path is `A:\env\revenant-relay.dpapi`, selected via the `RR_SECRETS_FILE` environment
variable. Matches Muninn's record that the old B: drive changed hands.

---

## 5. Shortest path to Relay's first real post

1. Fix the simulated-post marker (code, ~30 min).
2. Repoint `media_path` on the ads whose art is already local (mechanical).
3. Dave supplies: art for the 4 approved Skill Pack ads, missing `url` values, and approval decisions.
   **Captions and approval are Dave's alone — no AI-written ad copy, ever.**
4. First live run: **Reddit**, one post, watched. Credentials are already in place.
5. Meta tokens → Facebook Page + Instagram Business.
6. Only then decide the browser-automation tier.
