import os
from pathlib import Path

assets_dir = Path("C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets")
for f in os.listdir(assets_dir):
    if 'trio' in f.lower():
        print(f"TRIO file: {f}")
