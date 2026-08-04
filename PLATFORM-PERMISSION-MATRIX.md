# Relay platform permission matrix — 2026-08-03

Read-only research. No code changed, no config touched, no platform contacted, nothing committed.

Companion to [`RELAY-READINESS-AUDIT-2026-08-03.md`](RELAY-READINESS-AUDIT-2026-08-03.md), which covers the
ad library and the simulated-post bug. Those findings are not re-litigated here — this document answers
one question only: **which platforms can Relay legitimately post to, and by what mechanism.**

---

## Bottom line

The blocker was never "get permission from each site." It is a **mechanism** question, and it splits
*inside* platforms rather than between them. Every platform in Relay's config is one of two things:

- **Posting through the platform's own API to an account Dave owns** — sanctioned, self-service, no human
  to email. Meta says this in as many words: *"If your app only serves your Instagram professional account
  or an account you manage, Standard Access is all your app needs."*
- **Driving a logged-in personal account with Playwright** — prohibited by name on every platform that
  bothers to write it down. LinkedIn's §8.2.13 is the clearest: *"Use bots or other unauthorized automated
  methods to access the Services, add or download contacts, send or redirect messages, create, comment on,
  like, share, or re-share posts."*

**The two are independent.** A platform can ban the browser adapter and hand you a free posting API in the
same breath — LinkedIn does exactly that. So "Relay's LinkedIn adapter is forbidden" and "Dave may post to
LinkedIn programmatically" are both true, and the second is the one that matters.

Denominators, stated once and used throughout: **`config/platforms.json` holds 10 platform entries.
`src/platforms/` holds 9 adapters** — Indeed is configured but has no adapter at all. Of those 9 adapters,
**5 drive browser sessions (LinkedIn, X, Pinterest, TikTok, Snapchat) and those are the forbidden ones.**
The other 4 (Reddit, Facebook, Instagram, Bluesky) go through official APIs and are the legitimate ones —
and they are the ones that already work or need only a token.

**Launch surface that can run legitimately today: Reddit, Facebook, Instagram.** All three need zero
permission letters. Reddit carries one unresolved gate (below). X joins them for the price of an adapter
rewrite and pennies per post.

**Act on this first:** 6 of the 10 config entries are `enabled: true` for platforms Relay either cannot
legitimately post to or cannot post to at all (LinkedIn, X, Pinterest, TikTok, Snapchat, Indeed).
`build_tiers()` treats every enabled entry as a candidate, so **a live run today could select LinkedIn on
any given day** — the one platform with a clause naming exactly what the adapter does.

**Exactly one platform in the whole set requires an actual human permission request** — and it is not a
platform, it is Reddit's individual subreddit moderators. Draft message in §5.

---

## 1. The matrix

`Mechanism today` is what the adapter in `src/platforms/` actually does, not what the platform offers.

| Platform | Mechanism today | Class | Legit path | Primary source + quoted clause |
|---|---|---|---|---|
| **Reddit** | `praw` — official API, OAuth | **PERMITTED** *(destination gated)* | Already correct. Credentials present and complete. | API terms text **UNVERIFIED** — `reddit.com` and `redditinc.com` block Anthropic's crawler (HTTP 403 / explicit user-agent block). PRAW is Reddit's own documented client and the OAuth app is already provisioned. See §2 for the real gate. |
| **Facebook** | Meta Graph API v21.0, Page post | **PERMITTED** | Graph API to a Page Dave owns. `pages_manage_posts`, `pages_read_engagement`. **No App Review.** | [Access Levels](https://developers.facebook.com/docs/graph-api/overview/access-levels/): *"Permissions with Standard Access can only be requested from app users who have a role on the requesting app."* Advanced Access — the tier that needs review — is only for serving accounts you don't own. |
| **Instagram** | Meta Graph API v21.0, Business account | **PERMITTED** | Graph API to Dave's own Business account linked to the Page. `instagram_basic`, `instagram_content_publish`. **No App Review.** | [Instagram Platform overview](https://developers.facebook.com/docs/instagram-platform/overview/): *"Standard Access is all your app needs"* for an account you own or manage. Limit is **100 API-published posts per rolling 24h** ([content publishing docs](https://developers.facebook.com/docs/instagram-platform/content-publishing)) — note the adapter's error string says 50; harmless but stale. JPEG only, media must be *"hosted on a publicly accessible server."* |
| **Bluesky** | AT Protocol, app password | **PERMITTED** | Already correct. Disabled only because no account exists. | [Community Guidelines](https://bsky.social/about/support/community-guidelines) contain no bot or automation prohibition. Binding constraints are *"Do not send spam or repeatedly post content in ways that disrupt normal conversations"* and *"Do not post undisclosed commercial content, sponsored material, or advertising without clearly identifying its commercial nature."* → **disclose the commercial nature in the caption.** |
| **X** | Playwright on personal login | **FORBIDDEN as built** → **PERMITTED via API** | Rewrite to X API v2 `POST /2/tweets`. Pay-per-use, no subscription. | [X Developer Policy](https://docs.x.com/developer-terms/policy) requires apps *"use the APIs as intended and documented"*; browser-driving a logged-in account is off-API by construction. [Pricing](https://docs.x.com/x-api/getting-started/pricing): *"The X API uses pay-per-usage pricing. No subscriptions—pay only for what you use."* **$0.015/post, $0.200 for a post containing a URL.** No free posting tier. The docs don't define whether "post with URL" means any URL in the text or a card-rendered link, so treat $0.200 as the ceiling. Note `daily_post_goal: 3` is shared across *all* platforms, so X would draw roughly one post/day → **$0.45–$6.00/mo.** |
| **LinkedIn** | Playwright on personal login | **FORBIDDEN as built** → **PERMITTED via API** | **Self-service.** Add the *Share on LinkedIn* product in the Developer Portal → grants `w_member_social` → `POST /rest/posts`. Company Page posting via `w_organization_social` needs only a page **role**, not a partnership. | The browser adapter is banned by [User Agreement §8.2.13](https://www.linkedin.com/legal/user-agreement) — *"Use bots or other unauthorized automated methods to access the Services… **create, comment on, like, share, or re-share posts**, or otherwise drive inauthentic engagement."* **But the API path is open:** [Share on LinkedIn](https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin) — *"w_member_social — Required to create a LinkedIn post on behalf of the authenticated member"*, added by selecting *"your app from My Apps, navigate to the Products tab, and add the Share on LinkedIn product."* Rate limit **150 requests/member/day**. For the company page, [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api) — `w_organization_social` is *"Restricted to organizations where the authenticated member has one of the following company page roles: ADMINISTRATOR, DIRECT_SPONSORED_CONTENT_POSTER, CONTENT_ADMIN."* Note the contrast: `r_member_social` is flagged *"restricted and is available to approved users only"* — the **write** scopes carry no such flag. |
| **Pinterest** | Playwright on personal login | **FORBIDDEN as built** → **GRAY via API** | API v5 `POST /pins`, but see the tier trap. | [Developer Guidelines](https://policy.pinterest.com/en/developer-guidelines) prohibit *"actions on behalf of end users without their specific knowledge and consent… including… creating, saving and editing Pins"* and *"features that enable end users to automatically initiate actions without specifically considering each action."* Relay's per-ad `approved: true` gate is a genuine answer to that second clause — Dave considers each ad. **The killer is the access tier:** [Access Tiers](https://developers.pinterest.com/docs/key-concepts/access-tiers/) — *"all Pins and Boards created with Trial access are only visible to their creator as Sandbox entities."* Trial-tier Pins reach nobody. Standard access requires *"a video recording of your app completing an action using the Pinterest API."* |
| **TikTok** | Playwright on personal login (behind `RR_TIKTOK_ENABLE_AUTOMATION`) | **FORBIDDEN as built** → **GRAY via API** | Content Posting API, `video.publish` scope. | [Content Posting API](https://developers.tiktok.com/doc/content-posting-api-get-started/): *"All content posted by unaudited clients will be restricted to private viewing mode. Once you have successfully tested your integration, to lift the restrictions on content visibility, your API client must undergo an audit."* Same trap as Pinterest — works, but posts nobody can see until audited. Video-first; static ads underperform regardless. |
| **Snapchat** | Playwright on personal login | **FORBIDDEN as built** → **GRAY via API** | Public Profile API — genuinely supports organic posting, not just ads. | [Profile Asset Management](https://developers.snap.com/api/marketing-api/Public-Profile-API/ProfileAssetManagement): `POST /v1/public_profiles/{profile_id}/spotlights` and `.../saved_stories`. Hard constraint: **`.mp4`, 6–60 s, min 540×960.** Requires a Public Profile. Note the adapter's own error text already concedes the browser flow needs *"a verified Snapchat Ads Manager business workflow/API setup."* [Business Services Terms](https://www.snap.com/terms/business-services) contain no explicit automation clause. |
| **Indeed** | **None — adapter does not exist** | **EXCLUDE** | Not a permission problem. | `config/platforms.json` sets `"indeed": {"enabled": true}` but there is no `src/platforms/indeed.py` and no `adapter_loader` branch — **it silently simulates on every selection.** [Indeed ToS](https://www.indeed.com/legal): *"Use of any automation, scripting, or bots to automate the Indeed Apply process outside of Indeed's official vendors and tooling is prohibited."* Beyond that, Indeed is a paid job-board product and Relay's ads sell software, not jobs. Wrong surface entirely. |

### Reading the classes

- **PERMITTED** — official API, account Dave owns, self-service credentials, no human approval step.
- **GRAY** — an official API exists and permits the action, but a gating step (access tier, audit) stands
  between Relay and posts that other people can actually see. Not forbidden. Not yet useful.
- **FORBIDDEN** — the mechanism Relay currently uses is prohibited by a named clause.

---

## 2. The Reddit gate — the one thing to resolve before the first post

Reddit's *API* is not the problem. The problem is **where** Relay points it.

The ad library names 14 destination subreddits across `target_subreddits`:

| Subreddit | Times targeted | | Subreddit | Times targeted |
|---|---|---|---|---|
| r/artificial | 5 | | r/seo | 1 |
| r/LocalLLaMA | 3 | | r/redteamsec | 1 |
| r/netsec | 2 | | r/marketing | 1 |
| r/AI_Agents | 2 | | r/cybersecurity | 1 |
| r/singularity | 1 | | r/bugbounty | 1 |
| r/automations | 1 | | r/LangChain | 1 |
| r/GrowthHacking | 1 | | r/ChatGPT | 1 |

**Sitewide permission does not grant local permission.** A subreddit may forbid promotion outright, confine
it to a weekly thread, or allow it freely, and the local rule always wins. Several on this list —
r/LocalLLaMA, r/netsec, r/cybersecurity, r/artificial — are known for aggressive removal of vendor posts.
Posting an ad into one of those is how an account gets sitewide-flagged as a spammer, which would poison
the single platform where Relay's credentials already work.

**I could not verify any of these rules from here.** Reddit blocks Anthropic's crawler at the domain level,
so `reddit.com`, `old.reddit.com` and `redditinc.com` are all unreachable to this research. Every cell above
is **UNVERIFIED by tooling.**

**Prerequisite before Relay's first live Reddit post:** Dave reads the sidebar rules of each target
subreddit manually and reduces the list to an allowlist. Anything not on the allowlist gets stripped from
`target_subreddits`. Where a subreddit's rules are ambiguous, modmail them — draft in §5.

The honest classification is therefore: **Reddit API = PERMITTED. Reddit destinations = unresolved.**

---

## 3. Recommended Relay v1 shortlist

Shrink the launch surface to three platforms. All three are API-based, all three are accounts Dave owns,
none require a permission letter.

| Rank | Platform | Why it's in | What it still needs |
|---|---|---|---|
| **1** | **Reddit** | Sanctioned API, credentials already present and complete. Highest-intent audience for developer tooling. | Subreddit allowlist (§2). Nothing else. |
| **2** | **Facebook** | Graph API to an owned Page. Standard Access — no App Review, no wait. | One Meta developer app; `RR_FACEBOOK_PAGE_ID` + `RR_FACEBOOK_PAGE_TOKEN`. |
| **3** | **Instagram** | Same Meta app, same token flow. Adapter already written correctly. | Same Meta app, plus **JPEG conversions and public hosting** for the media — every current ad is `.png`/`.mp4`. This is real work, not a checkbox. |

**Defensible additions, in order of effort:**

- **LinkedIn** — **free, self-service, and the highest-value channel in the set for what Revenant Systems
  sells.** Add the *Share on LinkedIn* product to a LinkedIn developer app, get `w_member_social`, and post
  via `POST /rest/posts`. If the target is the Revenant Systems **Company Page**, use `w_organization_social`
  instead — that needs a page admin role, which Dave has, not a partnership. 150 requests/member/day is
  ~50× Relay's needs. Requires replacing the Playwright adapter, not keeping it. Rank this **above X**: same
  amount of work, no per-post cost, better audience fit.
- **X** — the API path is unambiguous and the adapter rewrite is bounded. Budget under $6/mo at the current
  shared 3-posts-a-day goal. Recommend as v1.2, purely to keep the first live run small.
- **Bluesky** — adapter is written and correct; the only blocker is that no account exists. Creating one is
  a five-minute self-service action, not a permission. **But it is the only shortlist item that requires
  editing approved ad copy rather than adding credentials:** their guidelines require commercial content be
  clearly identified as such, so every caption Relay would post to Bluesky needs that disclosure written
  into it. Captions are Dave's alone, so this is his edit to make, not a config change. Cheapest
  incremental reach in the whole matrix once that's done.

**Cut from v1 entirely:**

- **The LinkedIn Playwright adapter specifically** — retire it. §8.2.13 names exactly what it does. This is
  a mechanism cut, not a platform cut; LinkedIn itself is now a recommended addition above.
- **Pinterest, TikTok, Snapchat** — each has a legitimate API, and each gates visibility behind a tier or
  audit that makes the first N posts invisible. Revisit once the top three are producing.
- **Indeed** — remove from config. It is a live bug (`enabled: true` with no adapter, silently simulating),
  not a channel.

**Config-level consequence** (not applied — read-only task): the 6 misconfigured entries flagged in the
bottom line all need `enabled: false` before any live run, or `build_tiers()` will keep offering them as
candidates.

---

## 4. Where this contradicts the readiness audit

The [readiness audit](RELAY-READINESS-AUDIT-2026-08-03.md) got the big call right and one framing wrong.

**Confirmed:**
- "It was never the platform permissions" — correct, and this research strengthens it. There is no letter
  to write for nine of ten platforms.
- Reddit / Facebook / Instagram as the sanctioned-API tier — correct, and now cited.
- Indeed as broken config — correct.
- Instagram's JPEG-only and public-URL constraints — correct. (Its rate-limit figure of 50/24h is stale;
  Meta documents 100. That number lives in an adapter error *string*, not in any throttling logic — it is
  cosmetic, and nothing to go hunting for.)

**Corrected:**
- The audit files LinkedIn, X, Snapchat, Pinterest and TikTok under a heading that treats them as a
  *risk* decision — "Account-lock risk here is Dave's own accounts… Decision deferred, not made."
  **All five have an official posting API the project never used.** They are not "risky browser automation
  vs nothing" — they are "wrong mechanism chosen," a fixable engineering problem rather than a risk to
  accept.

**Corrected again, 2026-08-03 (second pass) — this document's own first-pass error:**
- The first version of this matrix classified **LinkedIn as FORBIDDEN with "no path available to a solo
  business"** and asserted the organic-share API was partner-gated. **That was wrong**, and Dave pushed back
  on it, correctly. It conflated two different things: the **Community Management/Marketing Developer
  Platform partner program** (genuinely gated) with **ordinary organic posting scopes** (not gated).
  `w_member_social` is added self-service from the Developer Portal's Products tab, and
  `w_organization_social` is gated on holding a **company page role**, not on a partnership. LinkedIn's row
  now reads the same as X's: forbidden as built, permitted via API.
- Consequence: the earlier claim "nine of ten platforms need no permission request" understated it. The
  correct statement is that **no platform requires a written permission request at all** — only Reddit's
  individual subreddit moderators do.
- The audit does not flag the subreddit question. Reddit is its designated first live post, and that post
  lands in a specific community with its own promo rules. §2 closes that gap.

---

## 5. Human permission requests

**No platform needs one.** Meta, Bluesky, Reddit's API, **LinkedIn's Share on LinkedIn product** and
Snapchat's Public Profile API are all self-service. Pinterest's Standard upgrade, TikTok's audit and X's
API access are self-service developer submissions — forms and a video, not correspondence. There is no
letter to write to any of them.

The one place a real human decides: **subreddit moderators.**

### Draft modmail — send per subreddit, only where the rules are ambiguous

> **Subject:** Permission check before posting — Revenant Systems (solo dev tools)
>
> Hi mods,
>
> I run Revenant Systems, a one-person shop building developer tooling (VS Code theme generator, agent/automation skill packs). I'd like to post about it here occasionally and I'd rather ask first than guess at the rules.
>
> Concretely, what I'm proposing: no more than one post a month, each one written by me, on-topic for this community, with the commercial nature stated plainly in the post itself. No comment automation, no voting, no DMs, no reposting the same thing.
>
> Reading the sidebar I wasn't certain whether that falls under your self-promotion rule or not. Three straight answers would settle it:
>
> 1. Are vendor/self-promo posts allowed here at all, or restricted to a specific thread or day?
> 2. If they're allowed, is there a frequency limit or flair you want used?
> 3. Is there anything you'd want disclosed beyond "I built this"?
>
> If the answer is simply no, that's a fine answer and I'll leave the community alone.
>
> Thanks for the work you do here,
> Dave — Revenant Systems

**How to use it:** send to the subreddits on the §2 list whose sidebar rules are genuinely ambiguous. Where
the sidebar already says "no self-promotion," don't send anything — remove that subreddit from
`target_subreddits` and move on. Where it already permits promo under stated conditions, don't send
anything either; just follow the stated conditions. Modmail is for the middle case only.

---

## 6. Verification status

Honest accounting of what was and wasn't retrieved from primary sources.

| Verified from primary source | Not verified |
|---|---|
| LinkedIn User Agreement §8.2.2, §8.2.13 | **Reddit Data API Terms** — `reddit.com` / `redditinc.com` block Anthropic's crawler outright; `support.reddithelp.com` returned 403 |
| Meta Graph API access levels + Instagram Standard Access | **All 14 subreddit rule sets** — same domain block (§2) |
| Instagram content publishing limits and formats | X consumer ToS — `x.com/en/tos` returns HTTP 402 to this crawler (developer policy at `docs.x.com` did resolve) |
| X Developer Policy and pay-per-usage pricing | Snapchat approval/eligibility requirements for Public Profile API — docs specify technical constraints only |
| Pinterest Developer Guidelines + access tiers | Whether Pinterest would approve a single-user tool for Standard access |
| TikTok Content Posting API audit requirement | |
| Bluesky Community Guidelines | |
| **LinkedIn Share on LinkedIn (`w_member_social`) + Posts API (`w_organization_social`)** | Whether a LinkedIn developer app already exists under the Revenant Systems business — Dave believes one did; not checkable from here |
| Snapchat Public Profile API endpoints; Business Services Terms | |
| Indeed ToS automation clause | |

Terms change. Re-check before acting on anything here more than a few months from now.
