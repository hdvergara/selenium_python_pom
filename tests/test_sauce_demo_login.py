"""Login and post-login scenarios against Sauce Demo (https://www.saucedemo.com/)."""

from urllib.parse import urlparse

import allure
import pytest
from loguru import logger

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from tests.sauce_demo_env import SauceDemoEnv


@allure.feature("Login")
class TestLogin:
    """End-to-end login flows; requires `sauce_demo_env` (URL, USER, PASS)."""

    @pytest.mark.smoke
    @pytest.mark.regression
    @allure.story("User can sign in with valid credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_ok(self, browser, sauce_demo_env: SauceDemoEnv):
        logger.info("Starting login test (happy path)")
        with allure.step("Open the application under test"):
            browser.get(sauce_demo_env.base_url)
        login_page = LoginPage(browser)
        with allure.step("Enter credentials and submit login"):
            login_page.set_username(sauce_demo_env.username)
            login_page.set_password(sauce_demo_env.password)
            login_page.click_login_button()
        with allure.step("Assert inventory page is loaded (URL and UI)"):
            path = urlparse(browser.current_url).path
            assert path == "/inventory.html", (
                f"Expected path /inventory.html after login, got {path!r} (url={browser.current_url!r})"
            )
            inventory = InventoryPage(browser)
            assert inventory.is_loaded(), "Inventory page title should be visible after successful login"
        logger.info("Login test (happy path) finished")

    @pytest.mark.regression
    @allure.story("User cannot sign in with invalid credentials")
    def test_login_fail(self, browser, sauce_demo_env: SauceDemoEnv):
        logger.info("Starting login test (invalid password)")
        with allure.step("Open the application under test"):
            browser.get(sauce_demo_env.base_url)
        login_page = LoginPage(browser)
        with allure.step("Enter credentials and submit login"):
            login_page.set_username(sauce_demo_env.username)
            login_page.set_password("wrong_password")
            login_page.click_login_button()
        with allure.step("Assert error message is displayed"):
            assert login_page.is_error_message_displayed(), "Error message should be visible"
        logger.info("Login test (invalid password) finished")

    @pytest.mark.regression
    @allure.story("Locked-out user cannot access the store")
    def test_login_locked_out_user(self, browser, sauce_demo_env: SauceDemoEnv):
        """Uses the public demo account `locked_out_user` (documented on the login page)."""
        logger.info("Starting login test (locked-out user)")
        with allure.step("Open the application under test"):
            browser.get(sauce_demo_env.base_url)
        login_page = LoginPage(browser)
        with allure.step("Sign in as locked_out_user"):
            login_page.set_username("locked_out_user")
            login_page.set_password(sauce_demo_env.password)
            login_page.click_login_button()
        with allure.step("Assert error message is displayed"):
            assert login_page.is_error_message_displayed(), "Error message should be visible for locked-out user"
        logger.info("Login test (locked-out user) finished")
