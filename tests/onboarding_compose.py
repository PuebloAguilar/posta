"""The default deployment must ignore an operator's unrelated Postiz key."""
import json
import os
from pathlib import Path
import subprocess
import tempfile

with tempfile.TemporaryDirectory(prefix="posta-compose-") as directory:
    credentials = Path(directory) / "plow-credentials"
    credentials.write_text("PLOW_API_BASE=https://plow.invalid\nPLOW_AGENT_TOKEN=fixture-only\n")
    env = {**os.environ, "PLOW_CREDENTIALS": str(credentials),
           "POSTIZ_API_KEY": "unrelated-operator-fixture-key",
           "POSTIZ_API_URL": "https://unrelated-operator.invalid/api"}
    result = subprocess.run(["docker", "compose", "config", "--format", "json"],
                            env=env, text=True, capture_output=True, check=True)
    agent = json.loads(result.stdout)["services"]["agent"]
    settings = agent["environment"]
    assert not settings.get("POSTIZ_API_KEY"), "Default deployment inherited the operator's API key"
    assert not settings.get("POSTIZ_API_URL"), "Default deployment inherited the operator's API URL"
    assert agent["volumes"][0]["target"] == "/var/lib/hermes"
    print("PASS: default Compose ignores operator Postiz credentials and retains its own home.")
