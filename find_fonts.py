import os
from pathlib import Path

assets_dir = Path("C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets")
for f in os.listdir(assets_dir):
    if f.lower().endswith(('.ttf', '.otf', '.woff', '.woff2')):
        print(f"Font file: {f}")
