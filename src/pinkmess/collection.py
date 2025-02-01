from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic.functional_validators import field_validator
from pydantic_ai.models import KnownModelName
from pydantic_ai.settings import ModelSettings


class Collection(BaseModel):
    """A representation of a collection of notes."""

    index: int
    """The index of the root directory."""

    path: str
    """The path to the root directory."""

    alias: str | None = None
    """An alias for the root directory."""

    file_name_format: str = "%Y%m%d%H%M%S"
    """The format of the note file name."""

    llm_model: KnownModelName = "anthropic:claude-3-5-sonnet-latest"
    """The LLM model to be used for agents that interact with this collection."""

    llm_settings: ModelSettings = field(default_factory=ModelSettings)
    """The settings of the LLM model."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @field_validator("path")
    def is_path_valid(cls, path: str) -> str:
        """
        Validates the path.
        """
        if not Path(path).exists():
            raise ValueError("Path does not exist.")
        if not Path(path).is_dir():
            raise ValueError("Path is not a directory.")
        return path
