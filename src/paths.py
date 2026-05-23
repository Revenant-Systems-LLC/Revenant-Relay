from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ADS_DIR = ROOT / "ads"
CONFIG_DIR = ROOT / "config"
DATA_DIR = ROOT / "data"
LOGS_DIR = ROOT / "logs"

SETTINGS_FILE = CONFIG_DIR / "settings.json"
PLATFORMS_FILE = CONFIG_DIR / "platforms.json"
RUN_HISTORY_FILE = DATA_DIR / "run_history.json"
COOLDOWNS_FILE = DATA_DIR / "platform_cooldowns.json"
DISABLED_FILE = DATA_DIR / "disabled_platforms.json"
