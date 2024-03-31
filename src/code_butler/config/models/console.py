from pydantic_settings import BaseSettings, SettingsConfigDict


class Console(BaseSettings):
    color: bool = True
    model_config = SettingsConfigDict(env_prefix="CODE_BUTLER_CONSOLE_", extra="allow")
