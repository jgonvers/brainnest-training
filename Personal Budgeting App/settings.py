import pydantic
from dotenv import load_dotenv
import logging
import os

load_dotenv()


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_file = "development.env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class SQLiteSettings(BaseSettings):
    """Database settings."""

    db_url: str = pydantic.Field(..., env="DB_URL")


log_level = logging.INFO
logging.basicConfig(
    filename="budget.log",
    encoding="utf-8",
    level=log_level,
    format="%(asctime)s %(levelname)s: %(name)s: %(message)s",
)
logging.getLogger("sqlalchemy").setLevel(log_level)
db_echo = log_level == logging.DEBUG

db_settings = SQLiteSettings()
