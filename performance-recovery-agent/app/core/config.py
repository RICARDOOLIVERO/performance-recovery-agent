from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "performance-recovery-agent"
    environment: str = "development"
    log_level: str = "INFO"
    llm_enabled: bool = False
    llm_api_url: str | None = None
    llm_api_key: str | None = None
    llm_model: str | None = None

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
