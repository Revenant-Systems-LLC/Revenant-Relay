import urllib.request

url = "https://www.revenantsystems.net/"
try:
    response = urllib.request.urlopen(url)
    html = response.read().decode('utf-8')
    with open("M:/Projects/Revenant-Relay/site_fetch.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Fetched successfully!")
except Exception as e:
    print(f"Error fetching: {e}")
