from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any


@dataclass
class Note:
    """
    A representation of a note.
    """

    path: Path
    """Path to the note file."""

    content: str | None = None
    """Content of the note."""

    metadata: dict[str, Any] = field(default_factory=dict)
    """Metadata related to the note."""

    @classmethod
    def create_empty(cls, dir_path: Path) -> Note:
        """
        Initializes an empty note given a directory.
        """
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        note_path = dir_path / f"{now}.md"
        note_path.touch()
        return cls(path=note_path)

    def load(self) -> None:
        """
        Loads the note content and metadata.
        """
        text = self.path.read_text()
        self.content = text
