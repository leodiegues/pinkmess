from typing import Literal
from pydantic import BaseModel
from pydantic_settings import CliApp, CliSubCommand
from pinkmess.config import settings
from pinkmess.note import Note


class NoteCreateCommand(BaseModel):
    """
    Creates a new empty note.
    """

    def cli_cmd(self) -> None:
        print("Creating new empty note...")
        collection = settings.current_collection
        path, file_name_format = collection.path, collection.file_name_format
        path.mkdir(parents=True, exist_ok=True)
        note = Note.create_empty(path, file_name_format)
        print(f"Note successfully created: {note.path.as_posix()}")


class NoteGenerateMetadataCommand(BaseModel):
    """
    Generates metadata through AI.
    """

    key: Literal["summary", "tags"] = "summary"
    """The metadata key which should have its content generated."""

    def cli_cmd(self) -> None:
        pass


class NoteCommands(BaseModel):
    """
    Note commands.
    """

    create: CliSubCommand[NoteCreateCommand]
    generate_metadata: CliSubCommand[NoteGenerateMetadataCommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
