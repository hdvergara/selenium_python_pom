from pydantic_settings import BaseSettings, SettingsConfigDict

from core.browser.browser_type import BrowserType


class BrowserConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

    browser: BrowserType = BrowserType.CHROME
    headless: bool = False


browser_config = BrowserConfig()
