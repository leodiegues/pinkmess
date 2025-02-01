from pathlib import Path
from typing import Literal

from pydantic import BaseModel
from pydantic_settings import (
    BaseSettings,
    CliApp,
    CliExplicitFlag,
    CliPositionalArg,
    CliSubCommand,
    SettingsConfigDict,
)
from pydantic_settings.sources import CliMutuallyExclusiveGroup

from pinkmess.config import Collection, settings
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

class ConfigAddRootDirCommand(BaseModel):
    """
    Adds a new root directory.
    """

    root_dir: CliPositionalArg[Path]
    """The root directory to be added."""

    alias: str
    """An alias for the root directory."""

    def cli_cmd(self) -> None:
        print(f"Adding new root directory: {self.root_dir}")
        settings.root_dirs.append(Collection(len(settings.root_dirs), self.root_dir, self.alias))
        print(f"Root directory successfully added: {self.root_dir}")


class ConfigSetRootDirCommand(BaseModel):
    """
    Sets the current root directory.
    """

    alias: CliPositionalArg[str]
    """The alias of the root directory to be set as current."""

    def cli_cmd(self) -> None:
        settings.set_current_root_dir_index_by_alias(self.alias)
        print(f"Current root directory successfully set: {settings.root_dir}")

class ConfigShowCommand(BaseModel):
    """
    Shows the current configuration.
    """

    def cli_cmd(self) -> None:
        print(settings.model_dump_json(indent=2))


class CollectionCommands(BaseModel):
    """
    Collection commands.
    """

    add: CliSubCommand[ConfigAddRootDirCommand]
    set: CliSubCommand[ConfigSetRootDirCommand]
    show: CliSubCommand[ConfigShowCommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)


class Pinkmess(BaseSettings):
    """
    Pinkmess CLI application.
    """

    config: CliSubCommand[CollectionCommands]
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
