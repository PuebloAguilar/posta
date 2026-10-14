"""Run the real CLI's device flow with two private homes and fixture accounts."""
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread

issued = []
polls = {}
api_calls = []
tokens = {"a": "fixture-owner-a-only", "b": "fixture-owner-b-only"}
reject_a = False


class API(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def respond(self, body, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(body).encode())

    def do_POST(self):
        body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if self.path == "/device/code":
            owner = ("a", "b")[len(issued)]
            issued.append(owner)
            polls[owner] = 0
            self.respond({"device_code": owner, "user_code": "FIXTURE-" + owner,
                          "verification_uri": "https://fixture.invalid/authorize",
                          "expires_in": 15, "interval": 1})
        elif self.path == "/device/token":
            owner = json.loads(body)["device_code"]
            polls[owner] += 1
            if polls[owner] == 1:
                self.respond({"error": "authorization_pending"}, 400)
            else:
                self.respond({"access_token": tokens[owner],
                              "api_url": root + "/tenant/" + owner,
                              "organization_id": "fixture-org-" + owner})
        else:
            self.respond({"error": "unexpected"}, 404)

    def do_GET(self):
        api_calls.append((self.path, self.headers.get("Authorization")))
        for owner, token in tokens.items():
            if self.path == "/tenant/" + owner + "/public/v1/integrations":
                if self.headers.get("Authorization") != token or (owner == "a" and reject_a):
                    self.respond({"error": "Invalid OAuth token"}, 401)
                else:
                    self.respond([{"id": "fixture-ig-" + owner,
                                   "name": "Owner " + owner, "identifier": "instagram-standalone"}])
                return
        self.respond({"error": "wrong tenant"}, 403)


server = ThreadingHTTPServer(("127.0.0.1", 0), API)
root = "http://127.0.0.1:" + str(server.server_port)
Thread(target=server.serve_forever, daemon=True).start()


def cli(home, *args, poison=False):
    env = {k: v for k, v in os.environ.items()
           if k not in {"POSTIZ_API_KEY", "POSTIZ_API_URL", "POSTIZ_AUTH_SERVER"}}
    env["HOME"] = str(home)
    if poison:
        env.update(POSTIZ_API_KEY="unrelated-operator-fixture-key",
                   POSTIZ_API_URL=root + "/creator")
    return subprocess.run(["postiz", *args], env=env, text=True,
                          capture_output=True, timeout=20)


def result_json(text):
    for i, char in enumerate(text):
        if char in "[{":
            try:
                return json.JSONDecoder().raw_decode(text[i:])[0]
            except ValueError:
                pass
    raise AssertionError("Missing JSON")


try:
    with tempfile.TemporaryDirectory(prefix="posta-owners-") as d:
        homes = {owner: Path(d) / owner for owner in tokens}
        for h in homes.values():
            h.mkdir(mode=0o700)
            r = cli(h, "integrations:list")
            assert r.returncode != 0 and "No authentication found" in r.stderr
        assert not api_calls, "A clean home must not contact the creator's account"
        for owner, home in homes.items():
            r = cli(home, "auth:login", "--auth-server", root)
            assert r.returncode == 0 and "Successfully authenticated" in r.stdout
            assert "FIXTURE-" + owner in r.stdout and polls[owner] == 2
            p = home / ".postiz" / "credentials.json"
            saved = json.loads(p.read_text())
            assert saved["accessToken"] == tokens[owner]
            assert saved["organizationId"] == "fixture-org-" + owner
            assert stat.S_IMODE(p.stat().st_mode) == 0o600
            assert stat.S_IMODE(p.parent.stat().st_mode) == 0o700
            # A new CLI process reads this home's saved auth, even with a poisoned environment.
            r = cli(home, "integrations:list", poison=True)
            assert r.returncode == 0
            assert result_json(r.stdout)[0]["id"] == "fixture-ig-" + owner
        reject_a = True
        assert cli(homes["a"], "integrations:list").returncode != 0
        assert cli(homes["b"], "integrations:list").returncode == 0
        assert cli(homes["a"], "auth:logout").returncode == 0
        assert not (homes["a"] / ".postiz" / "credentials.json").exists()
        assert cli(homes["a"], "integrations:list").returncode != 0
        assert cli(homes["b"], "integrations:list").returncode == 0
        assert all("/creator" not in path for path, _ in api_calls)
        assert all(token == tokens[path.split("/")[2]] for path, token in api_calls)
        print("PASS: fresh homes, device pending/success, owner-specific auth/API, permissions, persistence, rejection isolation and logout; no creator fallback or social writes.")
finally:
    server.shutdown()
    server.server_close()
