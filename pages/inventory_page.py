from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.actions.actions import Actions


class InventoryPage:
    """Sauce Demo inventory (product listing) after successful login."""

    PAGE_TITLE = (By.CSS_SELECTOR, '[data-test="title"]')

    def __init__(self, driver: WebDriver, default_timeout: int = 10):
        self.driver = driver
        self.actions = Actions(driver)
        self.default_timeout = default_timeout

    def is_loaded(self) -> bool:
        """Returns True when the product listing heading is visible."""
        return self.actions.is_visible(self.PAGE_TITLE, self.default_timeout)
