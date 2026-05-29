with open('M:/Projects/Revenant-Relay/site_fetch.css', 'r', encoding='utf-8') as f:
    content = f.read()

import re
matches = re.findall(r'(?i)(sell|soul|font-family).*', content)
for m in matches[:20]:
    print(m)
