"""example_lambda.example_hanlderのヘルスチェック"""

import sys
import json
import urllib.request

PING_EVENT = json.dumps({"method": "ping"})

req = urllib.request.Request(
    sys.argv[1],
    data=PING_EVENT.encode(),
    headers={"content-type": "application/json"},
)
with urllib.request.urlopen(req) as f:
    body = f.read()
    if json.loads(body) != "pong":
        sys.exit(f"Unexpected response returned: {body}")
sys.exit(0)
