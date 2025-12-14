from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "devops-showcase"
    ENV: str = "local"
    PORT: int = 8000

    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ISSUER: str = "app-repo"
    JWT_EXPIRES_MINUTES: int = 60

    GIT_SHA: str = "local"
    BUILD_TIME: str = "local"
    IMAGE_TAG: str = "local"


settings = Settings()
