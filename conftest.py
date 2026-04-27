import pytest
from playwright.sync_api import Page, sync_playwright


@pytest.fixture(scope="function")
# Otevře engeto.cz a odsouhlasí cookies.
def engeto_page():
    with sync_playwright() as context:
        browser = context.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        page.goto("https://engeto.cz/")
        cookie_btn = page.locator("#cookiescript_accept")
        if cookie_btn.is_visible():
            cookie_btn.click()
        yield page
        browser.close()
