from __future__ import annotations

from dataclasses import field
from pathlib import Path

from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.functional_serializers import field_serializer
from pydantic.functional_validators import field_validator, model_validator
from pydantic_ai.models import KnownModelName
from pydantic_ai.settings import ModelSettings


class Collection(BaseModel):
    """A representation of a collection of notes."""

    index: int
    """The index of the root directory."""

    path: Path
    """The path to the root directory."""

    name: str | None = None
    """An alias for the root directory."""

    file_name_format: str = "%Y%m%d%H%M%S"
    """The format of the note file name."""

    llm_model: KnownModelName = "anthropic:claude-3-5-sonnet-latest"
    """The LLM model to be used for agents that interact with this collection."""

    llm_settings: ModelSettings = field(default_factory=ModelSettings)
    """The settings of the LLM model."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("path")
    def is_path_valid(cls, path: Path) -> Path:
        """
        Validates the path.
        """
        if not path.exists():
            raise ValueError("Path does not exist.")
        if not path.is_dir():
            raise ValueError("Path is not a directory.")
        return path

    @model_validator(mode="after")
    def set_alias(self) -> Collection:
        """
        Sets the alias of the collection.
        """
        if self.name is None:
            self.name = self.path.name
        return self

    @field_serializer("path", when_used="always")
    def serialize_path(self, path: Path) -> str:
        """
        Serializes the path.
        """
        return path.as_posix()
