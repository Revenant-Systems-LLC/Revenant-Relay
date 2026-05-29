import urllib.request

url = "https://www.revenantsystems.net/assets/site.css"
try:
    response = urllib.request.urlopen(url)
    css = response.read().decode('utf-8')
    with open("M:/Projects/Revenant-Relay/site_fetch.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("Fetched CSS successfully!")
except Exception as e:
    print(f"Error fetching: {e}")
