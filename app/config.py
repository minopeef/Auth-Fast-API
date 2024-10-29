import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_URL: str = 'sqlite+aiosqlite:///data/db.sqlite3'
    SECRET_KEY: str
    ALGORITHM: str

    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")
    )


# Получаем параметры для загрузки переменных среды
settings = Settings()
database_url = settings.DB_URL
