"""Playwrightを使ったLambda関数ハンドラのサンプル"""

import os
from typing import Any

from playwright.sync_api import sync_playwright


def example_handler(event: dict[str, str], context: Any) -> str:
    """Lambda関数ハンドラのサンプル"""
    method = event["method"]
    if method == "ping":
        return "pong"
    elif method == "get_inner_text":
        url = event["url"]
        css_selector = event["target"]
        return get_inner_text(url, css_selector)
    raise ValueError(f"Invalid method: {method}")


def get_inner_text(url: str, css_selector: str) -> str:
    args = os.getenv("PWPYLAMBDA_CHROMIUM_ARGS", "").split()
    with sync_playwright() as p:
        browser = p.chromium.launch(args=args)
        try:
            page = browser.new_page()
            page.goto(url)
            text = page.locator(f"css={css_selector}").inner_text()
        finally:
            browser.close()
    return text
