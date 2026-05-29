import os
import json
import http.server
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8999
PROJECT_ROOT = Path(__file__).parent.resolve()
ASSETS_DIR = Path("C:/The-Ossuary/Revenant-Systems/Branding-Marketing/revenantsystems-net/assets")

class AdPreviewRequestHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Serve the main HTML preview page
        if path == "/" or path == "/index.html":
            return str(PROJECT_ROOT / "ads_preview.html")
        
        # Route local assets path cleanly
        if path.startswith("/assets/"):
            relative_path = path.replace("/assets/", "", 1)
            # Remove query parameters if any (like ?t=123)
            relative_path = relative_path.split("?")[0]
            # Decode URL-encoded characters (like %20 for spaces)
            relative_path = urllib.parse.unquote(relative_path)
            
            # Check local project assets folder first, fallback to ASSETS_DIR
            local_path = PROJECT_ROOT / "assets" / relative_path
            if local_path.exists():
                return str(local_path)
            return str(ASSETS_DIR / relative_path)
            
        return super().translate_path(path)

    def do_GET(self):
        # Endpoint to fetch all ads with their approval status
        if self.path == "/api/ads":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            ads_data = self.get_all_ads()
            self.wfile.write(json.dumps(ads_data).encode("utf-8"))
            return
            
        return super().do_GET()

    def do_POST(self):
        if self.path.startswith("/api/save/"):
            ad_id = self.path.replace("/api/save/", "")
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                payload = json.loads(post_data.decode('utf-8'))
                
                success = self.save_ad_changes(ad_id, payload)
                self.send_response(200 if success else 400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            except Exception as e:
                print(f"Error handling POST /api/save: {e}")
                self.send_response(400)
                self.end_headers()
            return

        # Legacy triggers (kept for robustness)
        if self.path.startswith("/api/approve/"):
            ad_id = self.path.replace("/api/approve/", "")
            success = self.update_ad_status(ad_id, True)
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            return

        if self.path.startswith("/api/reject/"):
            ad_id = self.path.replace("/api/reject/", "")
            success = self.update_ad_status(ad_id, False)
            self.send_response(200 if success else 400)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"success": success}).encode("utf-8"))
            return

    def get_all_ads(self):
        ads_list = []
        ads_dir = PROJECT_ROOT / "ads"
        if not ads_dir.exists():
            return []
            
        for category_dir in ads_dir.iterdir():
            if category_dir.is_dir():
                for ad_dir in category_dir.iterdir():
                    if ad_dir.is_dir():
                        ad_json_path = ad_dir / "ad.json"
                        if ad_json_path.exists():
                            try:
                                with open(ad_json_path, "r", encoding="utf-8") as f:
                                    ad_data = json.load(f)
                                    ad_data["_file_path"] = str(ad_json_path)
                                    # Normalize media paths for the web page
                                    if "media_paths" in ad_data:
                                        ad_data["web_media_paths"] = [self.normalize_media_path(p) for p in ad_data["media_paths"]]
                                    elif "media_path" in ad_data and ad_data["media_path"]:
                                        ad_data["web_media_paths"] = [self.normalize_media_path(ad_data["media_path"])]
                                    else:
                                        ad_data["web_media_paths"] = []
                                    ads_list.append(ad_data)
                            except Exception as e:
                                print(f"Error loading {ad_json_path}: {e}")
        return ads_list

    def normalize_media_path(self, path):
        # Turn absolute system path into our custom virtual route `/assets/filename`
        if not path:
            return ""
        filename = Path(path).name
        return f"/assets/{filename}"

    def update_ad_status(self, ad_id, approved):
        ads_dir = PROJECT_ROOT / "ads"
        for category_dir in ads_dir.iterdir():
            if category_dir.is_dir():
                for ad_dir in category_dir.iterdir():
                    if ad_dir.is_dir() and ad_dir.name == ad_id:
                        ad_json_path = ad_dir / "ad.json"
                        if ad_json_path.exists():
                            try:
                                with open(ad_json_path, "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                data["approved"] = approved
                                with open(ad_json_path, "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=2)
                                return True
                            except Exception as e:
                                print(f"Error writing to {ad_json_path}: {e}")
        return False

    def save_ad_changes(self, ad_id, payload):
        ads_dir = PROJECT_ROOT / "ads"
        for category_dir in ads_dir.iterdir():
            if category_dir.is_dir():
                for ad_dir in category_dir.iterdir():
                    if ad_dir.is_dir() and ad_dir.name == ad_id:
                        ad_json_path = ad_dir / "ad.json"
                        if ad_json_path.exists():
                            try:
                                with open(ad_json_path, "r", encoding="utf-8") as f:
                                    data = json.load(f)
                                
                                # Set status if specified in payload, else keep original
                                if "approved" in payload:
                                    data["approved"] = payload["approved"]
                                
                                # Set base caption
                                if "caption" in payload:
                                    data["caption"] = payload["caption"]
                                    
                                # Sync platform-specific captions
                                if "platform_captions" in payload:
                                    if "platform_captions" not in data:
                                        data["platform_captions"] = {}
                                    for pk, val in payload["platform_captions"].items():
                                        data["platform_captions"][pk] = val
                                        
                                with open(ad_json_path, "w", encoding="utf-8") as f:
                                    json.dump(data, f, indent=2)
                                return True
                            except Exception as e:
                                print(f"Error saving changes to {ad_json_path}: {e}")
        return False

def run():
    # Allow port reuse so restarting is fast
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), AdPreviewRequestHandler) as httpd:
        print(f"\n==================================================")
        print(f"💀 REVENANT SYSTEMS - AD PREVIEW SERVER RUNNING 💀")
        print(f"==================================================")
        print(f"-> Open your web browser and go to: http://localhost:{PORT}")
        print(f"-> Press Ctrl+C in this terminal to stop the server.")
        print(f"==================================================\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server...")

if __name__ == "__main__":
    run()
