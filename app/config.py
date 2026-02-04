from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "ML-Anonymizer"
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "app"
    DB_PASSWORD: str = "123456"
    DB_NAME: str = "app"


settings = Settings()
