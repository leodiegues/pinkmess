import subprocess
from pathlib import Path
from typing import Any, Literal

import frontmatter
from pydantic import BaseModel
from pydantic_ai import Agent
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

        if collection is None:
            print("No current collection found.")
            return

        path, file_name_format = collection.path, collection.file_name_format
        path.mkdir(parents=True, exist_ok=True)
        note = Note.create_empty(path, file_name_format)
        settings.collections[
            settings.current_collection_index
        ].last_created_note = note.path
        settings.save()

        print(f"Note successfully created: {note.path.as_posix()}")


class NoteGenerateMetadataCommand(BaseModel):
    """
    Generates metadata through AI.
    """

    path: Path | None = None
    """The path to the note. If not provided, the last created note from the collection will be used."""

    key: Literal["summary", "tags"] = "summary"
    """The metadata key which should have its content generated."""

    def cli_cmd(self) -> None:
        from pinkmess.agents.note_summarization import note_summarization_agent
        from pinkmess.agents.note_tag_suggestion import note_tag_suggestion_agent

        key_agent_map: dict[str, Agent[Note, Any]] = {
            "summary": note_summarization_agent,
            "tags": note_tag_suggestion_agent,
        }

        if settings.current_collection is None:
            print("No current collection found.")
            return

        path = self.path or settings.current_collection.last_created_note

        if path is None:
            print("No note path provided and no last created note found.")
            return

        note = Note.from_path(path)

        agent = key_agent_map[self.key]
        response = agent.run_sync(
            "Generate metadata for the following note:", deps=note
        )

        if note.metadata is None:
            note.metadata = frontmatter.Post("")

        note.metadata[self.key] = response.data
        note.save()


class NoteLastCreatedCommand(BaseModel):
    """
    Gets the last created note.
    """

    def cli_cmd(self) -> None:
        if settings.current_collection is None:
            print("No current collection found.")
            return

        last_created_note = settings.current_collection.last_created_note

        if last_created_note is None:
            print("No last created note found.")
        else:
            print(f"Last created note: {last_created_note.as_posix()}")


class NoteEditCommand(BaseModel):
    """
    Edits a note.
    """

    path: Path | None = None
    """The path to the note. If not provided, the last created note from the collection will be used."""

    def cli_cmd(self) -> None:
        print("Editing note...")
        collection = settings.current_collection

        if collection is None:
            print("No current collection found.")
            return

        path = self.path or collection.last_created_note

        if path is None:
            print("No note path provided and no last created note found.")
            return

        note = Note.from_path(path)
        subprocess.run([settings.editor, note.path.as_posix()])


class NoteCommands(BaseModel):
    """
    Note commands.
    """

    create: CliSubCommand[NoteCreateCommand]
    generate_metadata: CliSubCommand[NoteGenerateMetadataCommand]
    last: CliSubCommand[NoteLastCreatedCommand]
    edit: CliSubCommand[NoteEditCommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
