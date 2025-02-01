import subprocess
from typing import Any

import dotenv
from pydantic import BaseModel
from pydantic_settings import CliApp, CliPositionalArg, CliSubCommand

from pinkmess.config import DEFAULT_CONFIG_PATH, ENV_FILE_PATH, settings


class ConfigEditCommand(BaseModel):
    """
    Edits the current configuration.
    """

    def cli_cmd(self) -> None:
        config_path = DEFAULT_CONFIG_PATH.resolve().as_posix()
        print(f"Editing current configuration: {config_path}")
        print("Opening the configuration file in your default editor...")
        subprocess.run([settings.editor, config_path])
        print("Configuration file closed.")


class ConfigShowCommand(BaseModel):
    """
    Shows the current configuration.
    """

    def cli_cmd(self) -> None:
        print("Showing current configuration...")
        print(settings.model_dump_json(indent=2))


class ConfigSetEnvCommand(BaseModel):
    """
    Sets the environment variable.
    """

    key: CliPositionalArg[str]
    value: CliPositionalArg[Any]

    def cli_cmd(self) -> None:
        print("Setting environment variable...")
        dotenv.set_key(ENV_FILE_PATH, self.key, self.value)
        print(f"Environment variable set: {self.key}")


class ConfigCommands(BaseModel):
    """
    Shows the current configuration.
    """

    edit: CliSubCommand[ConfigEditCommand]
    show: CliSubCommand[ConfigShowCommand]
    set_env: CliSubCommand[ConfigSetEnvCommand]

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
