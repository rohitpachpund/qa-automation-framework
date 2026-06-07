"""Shared framework configuration for Pytest and Playwright fixtures."""

BASE_URL = "https://dev.polarismarketresearch.com"
BROWSER = "chromium"
HEADLESS = False
SLOW_MO = 200
DEFAULT_TIMEOUT = 10_000
VIEWPORT = {"width": 1366, "height": 768}
