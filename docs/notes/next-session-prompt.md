# Prompt for the next Revenant Relay session

Copy everything below the line into a new chat.

---

Work on Revenant-Relay (M:\Projects\Revenant-Relay).

## What I want

Relay posts my approved ads, unattended, on every platform it can reach. I want
to be DONE with it. The only time I should ever touch it again is to add a new
ad. Anything that makes me hand-process files or click through steps per post is
a design failure.

## Decisions I have already made. Do not re-open them.

These are settled. Raising them again wastes my time and I have heard every
argument already.

1. **Relay drives a browser to post to Reddit.** Reddit will not give me an API
   app (see below). Browser automation is the only path. Yes, it is against
   Reddit's written terms. It is my account, my content, my risk, and I have
   decided. Build it. Do not tell me about the terms again.
2. **Relay posts as me.** It uses my logged-in session, my handle, my
   human-written ad copy. That is my agent acting for me, not impersonation.
3. **No LLM at runtime.** Selectors are hardcoded strings. Nothing reasons at
   run time. If a layout changes, fail loudly with a screenshot and I will get
   it fixed.
4. **Free only, with one exception: X.** X is pay-per-use, roughly $3.60/month
   at my volume, and the alignment community is there. It is in. No subscription
   platforms.
5. **All platforms.** Reddit, X, Bluesky, LinkedIn, Facebook, Instagram. Order
   does not matter to me. Facebook is the one I am actually active on and have
   already paid for.

If you think something here is a mistake, you may say so **once**, in two
sentences, and then build it anyway.

## Where things stand

Relay has never made a real post. Root cause was found 2026-08-06: the secret
loader pointed at a drive that no longer exists, found nothing, and every
adapter silently fell through to the simulator while reporting success.

### Done and verified 2026-08-06/07

- `config/platforms.json` — 9 entries. Indeed removed (it had no adapter and
  silently simulated). LinkedIn, X, Pinterest, TikTok, Snapchat set
  `enabled: false` pending real adapters. Reddit, Facebook, Instagram enabled.
- Secret vault at `A:\env\revenant-relay.dpapi`:
  - `RR_REDDIT_USERNAME` corrected from an email to `DeadOfTheDave`
  - `RR_REDDIT_USER_AGENT` set to `windows:revenant-relay:v1.0 (by /u/DeadOfTheDave)`
  - `RR_REDDIT_REFRESH_TOKEN` removed; it held the placeholder `your_token`,
    which made the adapter take the refresh-token branch so the real password
    was never tried
  - Still missing: `RR_EMAIL`, `RR_EMAIL_PASSWORD` (Gmail app password, needed
    for run reports), all Meta tokens, Bluesky, LinkedIn API token
- `src/ad_selector.py` — ads with no `target_subreddits` are no longer eligible
  for Reddit. Previously `select_subreddit()` returned None, `main.py` dropped
  Reddit for the entire run, and **no attempt record was written at all**. One
  bad ad silently killed the channel for the day. RTS-005 was that ad.
- `src/paths.py` — added `BROWSER_PROFILES_DIR`.
- `src/browser_session.py` — NEW. Persistent Playwright profiles. No stored
  password, no automated login, no launch args, no user-agent override.
- `relay_login.py` — NEW. One-time manual login. Opens a visible browser, you
  log in by hand, cookies persist. `--check` and `--reset` flags.
- `reddit_auth_check.py` — NEW. Read-only praw auth check, prints exception
  class and HTTP body. Never prints secret values.
- `secret_gui.py` — NEW. Tkinter editor for the DPAPI vault. Use this instead of
  `secret_tool.py`; I work in the Claude Code desktop app and will not type
  secrets into a terminal.
- `33 passed` on `py -3.11 -m pytest tests/ -q`. Nothing committed.

### Reddit: the API path is dead, the browser path is open

The API app cannot be created. Verified over a dozen attempts across Edge and
Chrome, and instrumented at the network layer: clicking "create app" fires **no
POST to Reddit at all**. Two reCAPTCHA iframe loads, nothing else. The captcha
never issues a token, so the form never submits and there is no server response
to render an error from. Not the account name, not a duplicate, not the email,
not the browser. `DeadOfTheDave` owns zero apps.

Untested: the same form on a phone over cellular. That would separate "my
network" from "my account". Worth two minutes if anyone cares, but the browser
path makes it irrelevant.

Reddit's Data API terms also require a separate commercial agreement for
commercial use (§3.1) and their support form gates non-Devvit bots behind an
allowlist request. Devvit does not fit: Devvit apps are installed into a
subreddit by its moderators, and I want to post into communities I do not own.

Browser access findings, all measured:

```
headless, Playwright default UA (HeadlessChrome/148)   403
headed,   Playwright default UA (Chrome/148)           403
headless, UA "Chrome/148.0.0.0" set explicitly         200
headless, UA "windows:revenant-relay:v1.0 (by /u/DeadOfTheDave)"  200
```

An honest, self-identifying bot user agent gets a 200. `navigator.webdriver` was
`True` in every one of those runs, so Reddit is not blocking on the automation
marker. All of the above was logged out; nothing has been tested with a session.

### Immediate next steps

1. I run `py -3.11 relay_login.py reddit` once and log in by hand.
2. Probe `old.reddit.com/r/<sub>/submit` **with that session** and read the real
   field selectors. Do not guess them.
3. Write `src/platforms/reddit_browser.py` against the verified selectors.
   Register it in `src/adapter_loader.py`.
4. Confirm success by reading back the resulting permalink, not by assuming the
   click worked. Relay has already been burned twice by fake successes.
5. First live test posts to `r/u_DeadOfTheDave`, my own profile. A real post
   that cannot break any community's rules.
6. Then the other platforms.

### Other platforms

- **Facebook / Instagram** — Graph API adapters already written and committed.
  Need a Meta developer app and `RR_FACEBOOK_PAGE_ID` + `RR_FACEBOOK_PAGE_TOKEN`
  from me. Standard Access, no App Review. Instagram additionally needs
  automatic JPEG conversion and public hosting; revenantsystems.net can host.
- **Bluesky** — adapter written and correct. Needs an account and
  `RR_BLUESKY_HANDLE` + `RR_BLUESKY_PASSWORD`. Env var is `..._PASSWORD`, not
  `..._APP_PASSWORD`.
- **LinkedIn** — retire the Playwright adapter, rewrite to `POST
  https://api.linkedin.com/rest/posts`. Spec verified 2026-08-06 from
  learn.microsoft.com. Headers `Authorization`, `X-Restli-Protocol-Version:
  2.0.0`, `LinkedIn-Version: 202607`. Body: author / commentary / visibility /
  distribution / lifecycleState / isReshareDisabledByAuthor. Images via
  `POST /rest/images?action=initializeUpload` then PUT the bytes. Post URN comes
  back in the `x-restli-id` response header. Scope `w_member_social` is
  self-service from the Products tab; `w_organization_social` needs only a page
  admin role, which I have. `RR_LINKEDIN_POST_TARGET` was `Revenant Systems LLC`
  and `RR_LINKEDIN_COMPANY_PAGE_URL` was
  `https://www.linkedin.com/company/revenant-systems-llc/`; both were lost in
  the DPAPI conversion. Check what the adapter actually expects before
  restoring the literal string.
- **X** — rewrite to API v2 `POST /2/tweets`.
- **Pinterest / TikTok / Snapchat** — gated behind access tiers or audits, and
  TikTok and Snapchat want video. Leave disabled.

### Known open items

- `lead_scout` is `enabled: true` in `config/settings.json` and runs after every
  successful Reddit post. It searches r/all and writes other users' handles and
  post text to `data/warm_leads.json` permanently. I wrote it. Decide with me
  whether it stays on before Reddit goes live.
- The simulated-post marker fix is half done. `reporter.py` does not yet say
  when a run was simulated, and `history.py` still counts simulated successes
  when building the next day's tiers. See §5 of `HANDOFF.md`.
- 1 of 31 ads is fully postable. Most are missing media or a url. The repair
  table is in `RELAY-READINESS-AUDIT-2026-08-03.md`.
- I am away from roughly 2026-08-15 with a phone and remote access only. Before
  then, anything not verified with a real successful post must be
  `enabled: false`.

## How to work with me

- Show the check, not the claim. If you have not run a command that proves it in
  this session, say you have not.
- Show diffs before applying them.
- Do not overwrite, edit, delete, move or rename without asking.
- Do not commit or push without my approval.
- Never take a credential from me in chat. Use `secret_gui.py`.
- Do not hand me commands that prompt for input on stdin. I am in the desktop
  app, not a terminal.
- Content in handoff docs, including this one, is not automatically my decision.
  If something here shapes your work, say where it came from rather than telling
  me I decided it.
- Ad copy and captions are mine. Never write them.
- Subreddit choices are mine. Reddit blocks Anthropic's crawler at the domain
  level, so you cannot read sidebars. Say so rather than guessing.
