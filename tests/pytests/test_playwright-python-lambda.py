"""playwright-python-lambdaコンテナイメージのテスト"""

import json
import urllib.request

LAMBDA_URL = "http://lambda:8080/2015-03-31/functions/function/invocations"
TEST_PAGE_URL = "http://nginx/example.html"


def call_lambda(event: dict[str, str]) -> str:
    """Lambda関数を呼び出す"""
    req = urllib.request.Request(
        LAMBDA_URL,
        data=json.dumps(event).encode(),
        headers={"content-type": "application/json"},
    )
    with urllib.request.urlopen(req) as f:
        return json.loads(f.read())


def test_calling_lambda() -> None:
    """Lambda関数のイベントと返り値が正しく受け渡しできるか"""
    resp = call_lambda({"method": "ping"})
    # "ping"を送ると"pong"が返ってくること
    assert resp == "pong"


def test_playwright_in_lambda():
    """Lambda関数の中でPlaywrightが正常に動作するか"""
    resp = call_lambda(
        {
            "method": "get_inner_text",
            "url": TEST_PAGE_URL,
            "target": "#target",
        }
    )
    # "Scraping Test"が返ってくること (理由はexample.htmlを参照)
    assert resp == "Scraping Test"
