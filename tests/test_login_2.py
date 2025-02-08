import os

import allure
from dotenv import load_dotenv
from loguru import logger

from pages.login_page import LoginPage

load_dotenv()


@allure.feature('Login Feature')
class TestLogin:

    @allure.story('Usuario puede iniciar sesión con credenciales válidas')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_ok(self, browser):
        url = os.getenv("URL")
        logger.info("Iniciando la prueba de login")
        with allure.step("Se abre la aplicacion a probar"):
            browser.get(os.getenv("URL"))
        login_page = LoginPage(browser)
        with allure.step("Ingresar credenciales y hacer clic en iniciar sesión"):
            login_page.set_username(os.getenv("USER"))
            login_page.set_password(os.getenv("PASS"))
            login_page.click_login_button()
        with allure.step("Se valida que se cargue el Home"):
            assert url + "/inventory.html" in browser.current_url, "Mensaje opcional si no se cumple la asersion"
        logger.info("Prueba login finalizada")

    @allure.story('Usuario no puede iniciar sesion por credenciales invalidas')
    def test_login_fail(self, browser):
        logger.info("Iniciando la prueba de login")
        with allure.step("Se abre la aplicacion a probar"):
            browser.get(os.getenv("URL"))
        login_page = LoginPage(browser)
        with allure.step("Ingresar credenciales y hacer clic en iniciar sesión"):
            login_page.set_username(os.getenv("USER"))
            login_page.set_password("contraseña_valida")
            login_page.click_login_button()
        with allure.step("Se valida que se visualice el label de error"):
            assert login_page.is_displayed_lbl_error(), "No se visualiza el label"
        logger.info("Prueba login finalizada")
