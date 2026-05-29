import shutil
from pathlib import Path

src = Path("C:/The-Ossuary/Revenant-Systems/Misc/Fonts/_ttfs/Sell Your Soul.ttf")
dest = Path("M:/Projects/Revenant-Relay/assets/Sell Your Soul.ttf")

try:
    shutil.copy2(src, dest)
    print("Font copied successfully!")
except Exception as e:
    print(f"Error copying font: {e}")
