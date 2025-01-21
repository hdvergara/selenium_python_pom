import os
import allure
import pytest
from dotenv import load_dotenv
from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from guara.transaction import AbstractTransaction, Application
from guara import it

load_dotenv()


# Transaction for logging in
class Login(AbstractTransaction):
    def __init__(self, driver):
        super().__init__(driver)

    def do(self, username, password):
        self.username = username
        self.password = password
        # Navigate to the login page
        self._driver.get(os.getenv("URL"))

        # Set the username and password
        self._driver.find_element(By.ID, "username").send_keys(self.username)
        self._driver.find_element(By.ID, "password").send_keys(self.password)

        # Click the login button
        self._driver.find_element(By.ID, "submit").click()

        # Return the current URL to validate if the login was successful
        return self._driver.current_url


# Assertion to verify successful login
class VerifyLoginSuccess(it.IAssertion):
    def asserts(self, result, expected_value):
        assert (
            result == expected_value
        ), f"Expected: {expected_value}, but got: {result}"


# Example of using Guará to validate the framework's capabilities
@allure.feature("Login Feature")
class TestLogin:

    @allure.story("Usuario puede iniciar sesión con credenciales válidas")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_ok(self, browser):
        # Initialize the application
        app = Application(browser)

        # Run the login transaction
        app.at(Login, username=os.getenv("USER"), password=os.getenv("PASS")).asserts(
            it.IsEqualTo, os.getenv("URL") + "/inventory.html"
        )

        logger.info("Prueba login finalizada")
