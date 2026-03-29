from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

from core.browser.browser_type import BrowserType
from core.config.browser_config import browser_config


class BrowserSettings:
    """
        This class manages browser settings and provides a WebDriver instance.

        It reads browser type and headless configuration from settings and provides methods
        to get a WebDriver instance for the specified browser and quit the driver properly.
        """

    def __init__(self):
        self.browser_type = browser_config.browser
        self.headless = browser_config.headless
        self.driver = None

    def get_driver(self):
        """
                Initializes and configures a WebDriver instance based on the browser type.

                Selects the appropriate browser driver (Chrome, Firefox, or Edge) and configures
                headless mode when enabled (Chrome/Edge: --headless=new; Firefox: -headless).
                Maximizes the browser window and returns the driver.
                Driver binaries are resolved via Selenium Manager (built into Selenium 4.6+); no Service/executable_path.

                Raises:
                    ValueError: If the provided browser type is not supported.
                """
        logger.info(f"Selecting and configuring browser: {self.browser_type.value}")
        match self.browser_type:
            case BrowserType.CHROME:
                options = ChromeOptions()
                if self.headless:
                    options.add_argument("--headless=new")
                self.driver = webdriver.Chrome(options=options)
            case BrowserType.FIREFOX:
                options = FirefoxOptions()
                options.set_preference("app.update.auto", False)
                options.set_preference("app.update.enabled", False)
                if self.headless:
                    # Gecko: documented flag is -headless (not Chrome-style --headless).
                    options.add_argument("-headless")
                self.driver = webdriver.Firefox(options=options)
            case BrowserType.EDGE:
                options = EdgeOptions()
                if self.headless:
                    options.add_argument("--headless=new")
                self.driver = webdriver.Edge(options=options)
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
