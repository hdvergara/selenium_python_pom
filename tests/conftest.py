import os

import allure
import pytest
from dotenv import load_dotenv

from core.browser.browser import BrowserSettings
from tests.sauce_demo_env import SauceDemoEnv

load_dotenv()


@pytest.fixture
def sauce_demo_env() -> SauceDemoEnv:
    """Fail fast with a clear message when .env is missing or incomplete."""
    base_url = os.getenv("URL", "").strip()
    username = os.getenv("USER", "").strip()
    password = os.getenv("PASS", "").strip()
    missing = [name for name, val in (("URL", base_url), ("USER", username), ("PASS", password)) if not val]
    if missing:
        pytest.fail(
            f"Missing required environment variable(s): {', '.join(missing)}. "
            "Copy .env.example to .env and set URL, USER, and PASS."
        )
    return SauceDemoEnv(base_url=base_url, username=username, password=password)


@pytest.fixture
def browser():
    browser_settings = BrowserSettings()
    driver = browser_settings.get_driver()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    result = outcome.get_result()

    if result.when == "call" and result.failed:
        browser = item.funcargs.get("browser")
        if browser:
            allure.attach(
                browser.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
