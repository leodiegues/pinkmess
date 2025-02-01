
from pydantic_settings import BaseSettings, CliApp, SettingsConfigDict
from pydantic_settings.sources import CliSubCommand

from pinkmess.cli.collection import CollectionCommands
from pinkmess.cli.config import ConfigCommands
from pinkmess.cli.note import NoteCommands


class Pinkmess(BaseSettings):
    """
    Pinkmess CLI application.
    """

    # config: CliSubCommand[CollectionCommands]
    note: CliSubCommand[NoteCommands]
    collection: CliSubCommand[CollectionCommands]
    config: CliSubCommand[ConfigCommands]

    model_config = SettingsConfigDict(
        cli_prog_name="pinkmess",
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_implicit_flags=True,
        cli_use_class_docs_for_groups=True,
        arbitrary_types_allowed=True
    )

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)


def entrypoint() -> None:
    CliApp.run(Pinkmess)


if __name__ == "__main__":
    entrypoint()
