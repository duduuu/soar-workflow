import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv(".env")

class Settings:
    slack_webhook: str = os.getenv("SLACK_WEBHOOK", "")
    cti_api_key: str = os.getenv("CTI_API_KEY", "")
    cti_provider: str = os.getenv("CTI_PROVIDER", "abuseipdb").lower()

@lru_cache
def get_settings() -> Settings:
    return Settings()