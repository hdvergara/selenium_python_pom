from dataclasses import dataclass


@dataclass(frozen=True)
class SauceDemoEnv:
    """Required test data for Sauce Demo (Swag Labs) scenarios."""

    base_url: str
    username: str
    password: str
