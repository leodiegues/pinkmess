from __future__ import annotations

from pathlib import Path

from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.fields import Field
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

    llm_model: KnownModelName = "openai:gpt-4o-mini"
    """The LLM model to be used for agents that interact with this collection."""

    llm_settings: ModelSettings = Field(default_factory=lambda: ModelSettings())
    """The settings of the LLM model."""

    last_created_note: Path | None = None
    """The path to the last created note."""

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

    @model_validator(mode="after")
    def set_last_created_note(self) -> Collection:
        """
        Sets the last created note.
        """
        if self.last_created_note is None:
            self.update_last_created_note()

        if self.last_created_note is not None and not self.last_created_note.is_relative_to(self.path):
            raise ValueError("Last created note is not in the collection.")

        return self

    @field_serializer("path", when_used="always")
    def serialize_path(self, path: Path) -> str:
        """
        Serializes the path.
        """
        return path.resolve().absolute().as_posix()

    @field_serializer("last_created_note", when_used="always")
    def serialize_last_created_note(self, path: Path | None) -> str | None:
        """
        Serializes the path.
        """
        if path is None:
            return None
        return path.resolve().absolute().as_posix()

    def update_last_created_note(self) -> None:
        """
        Updates the last created note.
        """
        existing_notes = sorted(self.path.glob("*.md"), reverse=True)
        if existing_notes:
            self.last_created_note = existing_notes[0]
