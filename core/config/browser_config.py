from dotenv import load_dotenv
from pydantic.v1 import ConfigDict
from pydantic_settings import BaseSettings

from core.browser.browser_type import BrowserType

load_dotenv()

class BrowserConfig(BaseSettings):
    browser: BrowserType = BrowserType.CHROME
    headless: bool = False

    model_config = ConfigDict(env_file=".env", extra="allow")

browser_config = BrowserConfig()