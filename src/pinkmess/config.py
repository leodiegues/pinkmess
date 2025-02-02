from typing import Any

import rtoml
from platformdirs import user_config_path
from pydantic.fields import Field
from pydantic_ai.models import KnownModelName
from pydantic_ai.settings import ModelSettings
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_settings.sources import (
    PydanticBaseSettingsSource,
    TomlConfigSettingsSource,
)

from pinkmess.collection import Collection


DEFAULT_CONFIG_FILE = "config.toml"
DEFAULT_CONFIG_DIR = user_config_path() / "pinkmess"
DEFAULT_CONFIG_PATH = DEFAULT_CONFIG_DIR / DEFAULT_CONFIG_FILE
ENV_FILE_PATH = DEFAULT_CONFIG_DIR / ".env"
ENV_FILE_PATH.touch()


class Settings(BaseSettings):
    """Application settings."""

    collections: list[Collection] = Field(default_factory=list)
    """The collections of notes."""

    current_collection_index: int = 0
    """The index of the current collection."""

    default_llm_model: KnownModelName = "openai:gpt-4o-mini"
    """The default LLM model to be used."""

    default_llm_settings: ModelSettings = Field(default_factory=lambda: ModelSettings())
    """The default LLM settings to be used."""

    editor: str = "nvim"
    """The editor to be used."""

    model_config = SettingsConfigDict(toml_file=DEFAULT_CONFIG_PATH)

    def model_post_init(self, __context: Any) -> None:
        if not DEFAULT_CONFIG_PATH.exists():
            DEFAULT_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
            DEFAULT_CONFIG_PATH.touch()
            self.save()

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        return (TomlConfigSettingsSource(settings_cls), init_settings)

    @property
    def current_collection(self) -> Collection | None:
        """The current collection."""
        if not self.collections:
            return None
        return self.collections[self.current_collection_index]

    @property
    def llm_model(self) -> KnownModelName:
        """The LLM model to be used."""
        if not self.current_collection:
            return self.default_llm_model
        return self.current_collection.llm_model

    @property
    def llm_settings(self) -> ModelSettings:
        """The LLM settings to be used."""
        if not self.current_collection:
            return self.default_llm_settings
        return self.current_collection.llm_settings

    def get_collection_by_name(self, name: str) -> Collection | None:
        """Returns a collection by name."""
        for collection in self.collections:
            if collection.name == name:
                return collection
        return None

    def save(self) -> None:
        """Saves the settings."""
        DEFAULT_CONFIG_PATH.write_text(rtoml.dumps(self.model_dump(), pretty=True, none_value=None))


settings = Settings()
