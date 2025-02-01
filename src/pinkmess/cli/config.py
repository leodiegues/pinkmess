from pydantic import BaseModel
from pydantic_settings import CliApp, CliSubCommand
from pinkmess.config import settings


class ConfigShowCommand(BaseModel):
    """
    Shows the current configuration.
    """

    def cli_cmd(self) -> None:
        print("Showing current configuration...")
        print(settings.model_dump_json(indent=2))

class ConfigCommands(BaseModel):
    """
    Shows the current configuration.
    """

    show: CliSubCommand[ConfigShowCommand]
    """Shows the current configuration."""

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
