import os

import allure
import pytest


from pages.login_nemesis_page import LoginPageNemesis
from utils.browser_settings.browser_settings import BrowserSettings


@pytest.fixture
def browser():
    browser_settings = BrowserSettings()
    driver = browser_settings.get_driver()
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Ejecuta el resto del código en el hook
    outcome = yield
    result = outcome.get_result()

    # Solo actúa si la fase de llamada (cuando se ejecuta la prueba) falla
    if result.when == "call" and result.failed:
        # Intenta obtener el navegador de los argumentos de la función de prueba
        browser = item.funcargs.get("browser")
        if browser:
            # Toma la captura de pantalla y la adjunta en el reporte de Allure
            allure.attach(browser.get_screenshot_as_png(),
                          name="screenshot_on_failure",
                          attachment_type=allure.attachment_type.PNG)


@pytest.fixture
def logged_in_browser(browser):
    """
    Fixture que realiza el login y retorna un navegador autenticado.
    """
    browser.get(os.getenv("URL_NEMESIS"))
    login_page = LoginPageNemesis(browser)
    login_page.set_username(os.getenv("USER_NAME"))
    login_page.set_password(os.getenv("PASSWORD"))
    login_page.click_login_button()
    return browser
