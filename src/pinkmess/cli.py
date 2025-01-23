from typing import Literal

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    CliApp,
    CliPositionalArg,
    CliSubCommand,
    SettingsConfigDict,
)

from pinkmess.config import settings
from pinkmess.note import Note


class NoteCreateCommand(BaseModel):
    """
    Creates a new empty note.
    """

    def cli_cmd(self) -> None:
        print("Creating new empty note...")
        settings.root_dir.mkdir(parents=True, exist_ok=True)
        note = Note.create_empty(settings.root_dir)
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


class ConfigSetCommand(BaseModel):
    """
    Sets configuration key and value.
    """

    key: CliPositionalArg[str]
    value: CliPositionalArg[str]

    def cli_cmd(self) -> None:
        print(f"Changing `{self.key}` value...")
        getattr(settings, self.key, self.value)


class ConfigCommands(BaseModel):
    """
    Configuration commands.
    """

    set: CliSubCommand[ConfigSetCommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)


class Pinkmess(BaseSettings):
    """
    Pinkmess CLI application.
    """

    config: CliSubCommand[ConfigCommands]
    note: CliSubCommand[NoteCommands]

    model_config = SettingsConfigDict(
        cli_prog_name="pinkmess",
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_implicit_flags=True,
        cli_use_class_docs_for_groups=True,
    )

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)


def entrypoint() -> None:
    CliApp.run(Pinkmess)


if __name__ == "__main__":
    entrypoint()
