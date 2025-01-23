from pathlib import Path

from platformdirs import user_config_path, user_documents_path
from pydantic_settings import BaseSettings

DEFAULT_CONFIG_FILE = "config.toml"
DEFAULT_CONFIG_DIR = user_config_path() / DEFAULT_CONFIG_FILE
DEFAULT_NOTES_ROOT_DIR = user_documents_path() / "notes"


class Settings(BaseSettings):
    """Application settings."""

    root_dir: Path = DEFAULT_NOTES_ROOT_DIR
    """The root directory where notes should be created."""


settings = Settings()
