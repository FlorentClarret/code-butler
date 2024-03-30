from pydantic_settings import BaseSettings, SettingsConfigDict


class Github(BaseSettings):
    token: str = ""
    model_config = SettingsConfigDict(env_prefix="CODE_BUTLER_GITHUB_", extra="allow")
