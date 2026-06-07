import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from config import BROWSER, HEADLESS, SLOW_MO, VIEWPORT


@pytest.fixture(scope="session")
def browser() -> Browser:
    """Launch Chromium once per test session."""
    with sync_playwright() as playwright:
        browser_type = getattr(playwright, BROWSER)
        browser = browser_type.launch(headless=HEADLESS, slow_mo=SLOW_MO)
        yield browser
        browser.close()


@pytest.fixture()
def page(browser: Browser) -> Page:
    """Create a fresh browser context and page for each test."""
    context: BrowserContext = browser.new_context(viewport=VIEWPORT)
    page = context.new_page()
    yield page
    context.close()
