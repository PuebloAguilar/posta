"""Exercise the installed official CLI against a local API, never a real account.

Run inside the built image as uid 10000, with no production credentials mounted.
"""
import json
import os
from pathlib import Path
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.parse import urlparse

calls = []
created = []


class API(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        calls.append(("GET", self.path, self.headers.get("Authorization")))
        path = urlparse(self.path).path
        if path == "/api/public/v1/integrations":
            self.respond([{"id": "test-ig", "identifier": "instagram-standalone", "name": "Test account"}])
        elif path == "/api/public/v1/integration-settings/test-ig":
            self.respond({"output": {"rules": "Media required", "maxLength": 2200,
                                      "settings": {"required": ["post_type"]}}})
        elif path == "/api/public/v1/posts":
            self.respond({"posts": [{"id": "test-post", "state": "QUEUE",
                                     "publishDate": "2026-10-15T12:00:00Z",
                                     "releaseURL": None}]})
        else:
            self.respond({"error": "unexpected path"}, 404)

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", "0")))
        calls.append(("POST", self.path, self.headers.get("Authorization")))
        if self.path == "/api/public/v1/upload":
            assert "multipart/form-data" in self.headers.get("Content-Type", "")
            assert b"approved.png" in body
            self.respond({"id": "test-media", "path": "https://test.invalid/uploads/approved.png"})
        elif self.path == "/api/public/v1/posts":
            created.append(json.loads(body))
            self.respond([{"postId": "test-post", "integration": "test-ig"}])
        else:
            self.respond({"error": "unexpected path"}, 404)


def result_json(output):
    for i, char in enumerate(output):
        if char in "[{":
            try:
                return json.JSONDecoder().raw_decode(output[i:])[0]
            except json.JSONDecodeError:
                continue
    raise AssertionError("No JSON found in CLI output")


server = ThreadingHTTPServer(("127.0.0.1", 0), API)
Thread(target=server.serve_forever, daemon=True).start()
env = {**os.environ, "POSTIZ_API_URL": f"http://127.0.0.1:{server.server_port}/api",
       "POSTIZ_API_KEY": "fixture-key-only"}


def cli(*args):
    result = subprocess.run(["postiz", *args], env=env, text=True,
                            capture_output=True, timeout=20)
    assert result.returncode == 0, result.stderr
    return result.stdout


try:
    assert cli("--version").strip() == "2.0.16"
    assert "Credentials are valid" in cli("auth:status")
    assert result_json(cli("integrations:list"))[0]["id"] == "test-ig"
    assert result_json(cli("integrations:settings", "test-ig"))["output"]["maxLength"] == 2200
    with tempfile.TemporaryDirectory(prefix="postiz-fixture-") as directory:
        media = Path(directory) / "approved.png"
        # A 1x1 fixture; only multipart transport is under test, not image rendering.
        import base64
        media.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAusB9Wl6bN8AAAAASUVORK5CYII="))
        upload = result_json(cli("upload", str(media)))
        assert upload == {"id": "test-media", "path": "https://test.invalid/uploads/approved.png"}
        for post_type in ("draft", "schedule", "now"):
            payload = {"type": post_type, "date": "2026-10-15T12:00:00Z",
                       "shortLink": False, "tags": [], "posts": [{
                           "integration": {"id": "test-ig"},
                           "value": [{"content": "Approved fixture", "image": [upload]}],
                           "settings": {"__type": "instagram-standalone", "post_type": "story"}}]}
            request = Path(directory) / "request.json"
            request.write_text(json.dumps(payload))
            response = result_json(cli("posts:create", "--json", str(request)))
            assert response == [{"postId": "test-post", "integration": "test-ig"}]
            assert created[-1] == payload, "CLI must preserve approved JSON including uploaded id/path"
        posts = result_json(cli("posts:list", "--startDate", "2026-10-15T00:00:00Z",
                                "--endDate", "2026-10-16T00:00:00Z"))
        assert posts["posts"][0]["state"] == "QUEUE"
        assert posts["posts"][0]["releaseURL"] is None
    assert len(created) == 3
    assert all(call[2] == "fixture-key-only" for call in calls), "Wrong auth source or header"
    assert all(call[1].startswith("/api/public/v1/") for call in calls)
    print("PASS: CLI version, auth, discovery, provider schema, multipart upload, draft/schedule/now JSON, list/QUEUE, API prefix and auth header (9 checks).")
finally:
    server.shutdown()
    server.server_close()
