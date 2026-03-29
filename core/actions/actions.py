from loguru import logger
from selenium.common import ElementNotInteractableException, StaleElementReferenceException, TimeoutException, \
    NoSuchElementException, ElementNotVisibleException
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select


class Actions:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def _wait_for_visible(self, locator: tuple[str, str], timeout: int):
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located(locator))

    def _wait_for_clickable(self, locator: tuple[str, str], timeout: int):
        return WebDriverWait(self.driver, timeout).until(EC.element_to_be_clickable(locator))

    def click(self, locator: tuple[str, str], timeout: int) -> None:
        """
        Clicks on a web element after waiting for it to be clickable.

        This method uses WebDriverWait to wait for the element to be in a clickable state
        for a specified timeout before attempting to interact with it.

        Args:
            locator (tuple[str, str]): A tuple containing the locator type (e.g., By.ID, By.XPATH)
                and the value of the locator (e.g., element ID, XPath expression).
            timeout (int): The maximum wait time in seconds for the element to become clickable.

        Raises:
            NoSuchElementException: If the element is not found within the specified timeout.
            ElementNotInteractableException: If the element is visible but not interactable.
            StaleElementReferenceException: If the element reference is no longer valid.
            TimeoutException: If the element is not clickable within the specified timeout.
        """
        try:
            element = self._wait_for_clickable(locator, timeout)
            element.click()
            logger.info(f"Clicked on element: '{locator}'")
        except Exception as e:
            logger.error(f"Click on element '{locator}' failed:  {e}")
            raise

    def send_text(self, locator: tuple[str, str], text: str, timeout: int) -> None:
        """
        Sends a specified text to a web element after waiting for it to be visible.

        This method uses WebDriverWait to wait for the element to be visible within a
        specified timeout before attempting to interact with it. It then clears the
        element (if it's an input field) and sends the provided text. Logs success
        and error messages.

        Args:
            locator (tuple[str, str]): A tuple containing the locator type (e.g., By.ID, By.XPATH)
                and the value of the locator (e.g., element ID, XPath expression).
            text (str): The text to send to the element.
            timeout (int): The maximum wait time in seconds for the element to become visible.

        Raises:
            NoSuchElementException: If the element is not found within the specified timeout.
            ElementNotVisibleException: If the element is not visible within the timeout.
            ElementNotInteractableException: If the element is visible but not interactable.
            TimeoutException: If the element is not visible within the specified timeout.
        """
        try:
            element = self._wait_for_visible(locator, timeout)
            element.clear()
            element.send_keys(text)
            logger.info(f"Entered '{text}' into '{locator}'")
        except Exception as e:
            logger.error(f"Error writing to '{locator}': {e}")
            raise

    def select_value_by_select(self, locator: tuple[str, str], value: str, timeout: int) -> None:
        """
        Selects a specific value from a dropdown (select) element after waiting for it to be visible.

        This method uses WebDriverWait to wait for the element to be visible within a
        specified timeout before attempting to interact with it. Then, it creates a
        Select object from the element and selects the option with the provided
        "value" attribute. Logs success and error messages.

        Args:
            locator (tuple[str, str]): A tuple containing the locator type (e.g., By.ID, By.XPATH)
                and the value of the locator (e.g., element ID, XPath expression).
            value (str): The value attribute of the option to select from the dropdown.
            timeout (int): The maximum wait time in seconds for the element to become visible.

        Raises:
            NoSuchElementException: If the element is not found within the specified timeout.
            ElementNotVisibleException: If the element is not visible within the timeout.
            ElementNotInteractableException: If the element is visible but not interactable.
            TimeoutException: If the element is not visible within the specified timeout.
        """
        try:
            select_element = self._wait_for_visible(locator, timeout)
            select = Select(select_element)
            select.select_by_value(value)
            logger.info(f"Value '{value}' selected from '{locator}'")
        except Exception as e:
            logger.error(f"Error selecting value: {e}")
            raise

    def select_value_by_visible_text(self, locator: tuple[str, str], value: str, timeout: int) -> None:
        """
        Selects a specific value from a dropdown (select) element after waiting for it to be visible.

        This method uses WebDriverWait to wait for the element to be visible within a
        specified timeout before attempting to interact with it. Then, it creates a
        Select object from the element and selects the option with the provided
        "visible_text" attribute. Logs success and error messages.

        Args:
            locator (tuple[str, str]): A tuple containing the locator type (e.g., By.ID, By.XPATH)
                and the value of the locator (e.g., element ID, XPath expression).
            value (str): The value attribute of the option to select from the dropdown.
            timeout (int): The maximum wait time in seconds for the element to become visible.

        Raises:
            NoSuchElementException: If the element is not found within the specified timeout.
            ElementNotVisibleException: If the element is not visible within the timeout.
            ElementNotInteractableException: If the element is visible but not interactable.
            TimeoutException: If the element is not visible within the specified timeout.
        """
        try:
            select_element = self._wait_for_visible(locator, timeout)
            select = Select(select_element)
            select.select_by_visible_text(value)
            logger.info(f"Value '{value}' selected from '{locator}'")
        except Exception as e:
            logger.error(f"Error selecting value: {e}")
            raise

    def get_text(self, locator: tuple[str, str], timeout: int) -> str:
        """
        Retrieves the text content of a web element after waiting for it to be visible.

        Args:
            locator (tuple[str, str]): Locator tuple (e.g. By.ID, value).
            timeout (int): Maximum wait in seconds for the element to become visible.

        Returns:
            str: The element's visible text.

        Raises:
            TimeoutException: If the element does not become visible within the timeout.
            Exception: Other Selenium errors (e.g. stale element), re-raised after logging.
        """
        try:
            element = self._wait_for_visible(locator, timeout)
            text = element.text
            logger.info(f"Captured text '{text}' from element '{locator}'")
            return text
        except TimeoutException as e:
            msg = (
                f"get_text failed: element {locator} did not become visible within {timeout}s; "
                "cannot read text."
            )
            logger.error(msg)
            raise TimeoutException(msg) from e
        except Exception as e:
            logger.error(f"get_text failed for element {locator}: {e}")
            raise

    def is_visible(self, locator: tuple[str, str], timeout: int) -> bool:
        """
        Returns whether the element is visible within the given timeout.

        If the wait times out, distinguishes between:
        - No matching nodes in the DOM (locator did not match any element after the wait).
        - At least one node exists but did not satisfy visibility within the timeout
          (e.g. hidden, not yet rendered, or still loading).

        Args:
            locator (tuple[str, str]): Locator tuple (e.g. By.ID, value).
            timeout (int): Maximum wait in seconds for visibility.

        Returns:
            bool: True if the element is visible; False if not visible after the scenarios above.
        """
        try:
            element = self._wait_for_visible(locator, timeout)
            return element.is_displayed()
        except TimeoutException:
            elements = self.driver.find_elements(*locator)
            if not elements:
                logger.warning(
                    "Element {!r} not present in the DOM after {}s (visibility wait timed out).",
                    locator,
                    timeout,
                )
                return False
            logger.warning(
                "Element {!r} is in the DOM but did not become visible within {}s "
                "(hidden, zero size, or still loading).",
                locator,
                timeout,
            )
            return False
        except Exception as e:
            logger.error("Unexpected error checking visibility of {!r}: {}", locator, e)
            raise

    def move_to_element(self, locator: tuple[str, str], timeout: int) -> None:
        """
        Moves the browser's focus to a web element after waiting for it to be visible.

        This method uses WebDriverWait to wait for the element to be visible within a
        specified timeout. If the element is found, it creates an ActionChains object
        and uses it to move the mouse cursor to the center of the element. Logs success
        and error messages.

        Args:
            locator (tuple[str, str]): A tuple containing the locator type (e.g., By.ID, By.XPATH)
                and the value of the locator (e.g., element ID, XPath expression).
            timeout (int): The maximum wait time in seconds for the element to become visible.

        Raises:
            NoSuchElementException: If the element is not found within the specified timeout.
            ElementNotVisibleException: If the element is not visible within the timeout.
            TimeoutException: If the element is not visible within the specified timeout.
        """
        try:
            element = self._wait_for_visible(locator, timeout)
            actions = ActionChains(self.driver)
            actions.move_to_element(element).perform()
            logger.info("Mouse hover action on element completed successfully.")
        except Exception as e:
            logger.error(f"Failed to move to element: {e}")
            raise
