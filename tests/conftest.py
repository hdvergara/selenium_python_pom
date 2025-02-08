import allure
import pytest

from core.browser.browser import BrowserSettings


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
            allure.attach(browser.get_screenshot_as_png(),
                          name="screenshot_on_failure",
                          attachment_type=allure.attachment_type.PNG)
