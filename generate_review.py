import json
import pathlib

md_lines = ["# Unapproved Ads Review", ""]
ad_count = 0

for p in pathlib.Path('m:/Projects/Revenant-Relay/ads').rglob('ad.json'):
    try:
        data = json.loads(p.read_text('utf-8'))
    except Exception as e:
        continue
        
    if not data.get('approved'):
        ad_count += 1
        md_lines.append(f"## {data.get('id', 'Unknown ID')} - {data.get('product', 'Unknown Product')}")
        md_lines.append(f"**Format:** {data.get('post_format')}")
        md_lines.append(f"**Platforms:** {', '.join(data.get('allowed_platforms', []))}")
        md_lines.append(f"**Media:** {data.get('media_path', 'None')}")
        md_lines.append(f"### Default Caption\n```text\n{data.get('caption', '')}\n```")
        if 'platform_captions' in data:
            for plat, cap in data['platform_captions'].items():
                md_lines.append(f"### {plat.title()} Caption\n```text\n{cap}\n```")
        md_lines.append("---\n")

md_lines.insert(1, f"Found **{ad_count}** unapproved ads.\n")
pathlib.Path('m:/Projects/Revenant-Relay/ads_review.md').write_text('\n'.join(md_lines), 'utf-8')
