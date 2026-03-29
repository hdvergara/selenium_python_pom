from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from core.actions.actions import Actions


class LoginPage:
    """Sauce Demo (Swag Labs) login — IDs and data-test hooks are stable across locales."""

    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    # Prefer test hook over XPath with long English copy (survives i18n / copy tweaks).
    ERROR_MESSAGE = (By.CSS_SELECTOR, '[data-test="error"]')

    def __init__(self, driver: WebDriver, default_timeout=10):
        self.driver = driver
        self.actions = Actions(driver)
        self.default_timeout = default_timeout

    def set_username(self, user: str) -> None:
        self.actions.send_text(self.USERNAME_INPUT, user, self.default_timeout)

    def set_password(self, password: str) -> None:
        self.actions.send_text(self.PASSWORD_INPUT, password, self.default_timeout)

    def click_login_button(self) -> None:
        self.actions.click(self.LOGIN_BUTTON, self.default_timeout)

    def is_error_message_displayed(self) -> bool:
        return self.actions.is_visible(self.ERROR_MESSAGE, self.default_timeout)
