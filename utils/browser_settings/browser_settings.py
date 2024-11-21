from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from utils.browser_settings.browser_type import BrowserType
from utils.config.settings import settings


class BrowserSettings:
    """
        This class manages browser settings and provides a WebDriver instance.

        It reads browser type and headless configuration from settings and provides methods
        to get a WebDriver instance for the specified browser and quit the driver properly.
        """

    def __init__(self):
        self.browser_type = settings.browser
        self.headless = settings.headless
        self.driver = None

    def get_driver(self):
        """
                Initializes and configures a WebDriver instance based on the browser type.

                Selects the appropriate browser driver (Chrome, Firefox, or Edge) and configures
                it with headless mode if specified. Maximizes the browser window and returns the driver.

                Raises:
                    ValueError: If the provided browser type is not supported.
                """
        logger.info(f"Selecting and configuring browser: {self.browser_type.value}")
        match self.browser_type:
            case BrowserType.CHROME:
                options = ChromeOptions()
                if self.headless:
                    options.add_argument('--headless')
                self.driver = webdriver.Chrome(
                    service=ChromeService(ChromeDriverManager().install()),
                    options=options
                )
            case BrowserType.FIREFOX:
                options = FirefoxOptions()
                options.set_preference("app.update.auto", False)
                options.set_preference("app.update.enabled", False)
                if self.headless:
                    options.add_argument('--headless')
                self.driver = webdriver.Firefox(
                    service=FirefoxService(GeckoDriverManager().install()),
                    options=options
                )
            case BrowserType.EDGE:
                options = EdgeOptions()
                if self.headless:
                    options.add_argument('--headless')
                self.driver = webdriver.Edge(
                    service=EdgeService(EdgeChromiumDriverManager().install()),
                    options=options
                )
            case _:
                raise ValueError(f"Browser not supported: {self.browser_type}")

        self.driver.maximize_window()
        return self.driver

    def quit_driver(self):
        """
                Quits the currently running WebDriver instance and logs a message.

                This method closes the browser window associated with the WebDriver instance if it exists.
                It then logs a message indicating that the browser has been closed.
                """
        if self.driver:
            self.driver.quit()
            logger.info(f"Browser {self.browser_type.value} closed.")