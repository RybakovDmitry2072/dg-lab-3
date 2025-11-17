from functools import cached_property

from pydantic import computed_field
from pydantic_settings import BaseSettings

from app.utils.vault_helper import vault_helper


class Settings(BaseSettings):
    @computed_field
    @cached_property
    def api_key_for_weather(self) -> str:
        return vault_helper.get_api_key(alias='weather-api-key')

    @computed_field
    @cached_property
    def api_key_for_event(self) -> str:
        return vault_helper.get_api_key(alias='event-api-key')

    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
