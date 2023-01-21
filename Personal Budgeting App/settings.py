import pydantic
from dotenv import load_dotenv

load_dotenv()


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = "development.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class SQLiteSettings(BaseSettings):
    """Database settings."""

    db_url: str = pydantic.Field(..., env="DB_URL")


db_settings = SQLiteSettings()
print(db_settings.db_url)
