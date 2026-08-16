from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADS_DIR = ROOT / "ads"
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

# Persistent Playwright profiles, one directory per platform. These hold real
# session cookies written by a human login (see relay_login.py), which is why
# no adapter using them needs a stored password. Deliberately NOT Dave's real
# Opera GX profile: Playwright locks whatever profile directory it opens, so
# pointing at a live browser profile risks corrupting it mid-run.
BROWSER_PROFILES_DIR = DATA_DIR / "browser_profiles"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
PLATFORMS_FILE = CONFIG_DIR / "platforms.json"
RUN_HISTORY_FILE = DATA_DIR / "run_history.json"
COOLDOWNS_FILE = DATA_DIR / "platform_cooldowns.json"
DISABLED_FILE = DATA_DIR / "disabled_platforms.json"
WARM_LEADS_FILE = DATA_DIR / "warm_leads.json"
