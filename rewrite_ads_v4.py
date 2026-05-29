import os
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.resolve()

SIGNATURE = "яƏ̄Λ🅔ղaͣÑ† ×͡× Ƨÿ§τΣМͫs"

# Ads to update with the user's custom signature in the header
UPDATES = {
    "CS-004": {
        "header_replace": "яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs",
        "header_new": SIGNATURE
    },
    "RH-004": {
        "header_replace": "яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs",
        "header_new": SIGNATURE
    },
    "SYS-001": {
        "header_replace": "яᴇᴠᴇɴᴀɴᴛ sʏsᴛᴇᴍs",
        "header_new": SIGNATURE
    }
}

def main():
    updated_count = 0
    ads_dir = PROJECT_ROOT / "ads"
    
    for category in ads_dir.iterdir():
        if category.is_dir():
            for ad_folder in category.iterdir():
                if ad_folder.is_dir() and ad_folder.name in UPDATES:
                    ad_id = ad_folder.name
                    ad_file = ad_folder / "ad.json"
                    
                    if ad_file.exists():
                        try:
                            with open(ad_file, "r", encoding="utf-8") as f:
                                data = json.load(f)
                            
                            replace_info = UPDATES[ad_id]
                            target = replace_info["header_replace"]
                            replacement = replace_info["header_new"]
                            
                            # Replace in the main caption
                            if "caption" in data and target in data["caption"]:
                                data["caption"] = data["caption"].replace(target, replacement)
                                
                            # Replace in platform specific captions
                            if "platform_captions" in data:
                                for platform, cap in data["platform_captions"].items():
                                    if target in cap:
                                        data["platform_captions"][platform] = cap.replace(target, replacement)
                                        
                            with open(ad_file, "w", encoding="utf-8") as f:
                                json.dump(data, f, indent=2)
                                
                            print(f"Injected custom signature into: {ad_id}")
                            updated_count += 1
                        except Exception as e:
                            print(f"Error updating {ad_id}: {e}")
                            
    print(f"\nCompleted! Injected signature into {updated_count} ads.")

if __name__ == "__main__":
    main()
