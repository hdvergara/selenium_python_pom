from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from utils.web_actions.actions import Actions


class LoginPage:

    usernameInput = (By.ID, "user-name")
    passwordInput = (By.ID, "password")
    loginButton = (By.ID, "login-button")
    errorLoginLabel = (By.XPATH, "//*[contains(text(),'Epic sadface: Username')]")


    def __init__(self, driver: WebDriver, default_timeout=10 ):
        self.driver = driver
        self.actions = Actions(driver)
        self.default_timeout = default_timeout

    def set_username(self, user: str) -> None:
        self.actions.send_text(self.usernameInput,user, self.default_timeout)

    def set_password(self, password: str) -> None:
        self.actions.send_text(self.passwordInput, password, self.default_timeout)

    def click_login_button(self) -> None:
        self.actions.click(self.loginButton, self.default_timeout)

    def is_displayed_lbl_error(self) -> bool:
        return self.actions.is_visible(self.errorLoginLabel, self.default_timeout)