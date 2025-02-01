from pathlib import Path
from pydantic import BaseModel
from pydantic.config import ConfigDict
from pydantic_ai.models import KnownModelName
from pydantic_ai.settings import ModelSettings
from pydantic_settings import CliApp, CliPositionalArg, CliSubCommand
from pinkmess.collection import Collection
from pinkmess.config import settings

class CollectionCreateCommand(BaseModel):
    """
    Creates a new collection.
    """

    path: CliPositionalArg[str]
    """The path to the collection."""

    alias: str
    """The alias of the collection."""

    llm_model: KnownModelName | None = None
    """The LLM model to be used for the collection."""

    llm_settings: ModelSettings | None = None
    """The LLM settings to be used for the collection."""

    model_config = ConfigDict(arbitrary_types_allowed=True)


    def cli_cmd(self) -> None:
        print("Adding new root directory...")
        new_collection_path = Path(self.path)
        new_collection = Collection(index=len(settings.collections), path=new_collection_path.as_posix(), alias=self.alias, llm_model=self.llm_model or settings.default_llm_model, llm_settings=self.llm_settings or settings.default_llm_settings)
        new_collection_path.mkdir(parents=True, exist_ok=True)
        settings.collections.append(new_collection)
        settings.save()
        print(f"Root directory successfully added: {new_collection_path.as_posix()}")


class CollectionSetCommand(BaseModel):
    """
    Sets the current collection.
    """

    alias: CliPositionalArg[str]
    """The alias of the collection."""

    def cli_cmd(self) -> None:
        print(f"Setting current collection to {self.alias}...")
        found = False
        for collection in settings.collections:
            if collection.alias == self.alias:
                settings.current_collection_index = collection.index
                settings.save()
                print(f"Current collection successfully set to alias: {self.alias}")
                found = True
                break

        if not found:
            print(f"Collection with alias '{self.alias}' not found.")

class CollectionShowCurrentCommand(BaseModel):
    """
    Shows the current collection.
    """

    def cli_cmd(self) -> None:
        print(f"Current collection: '{settings.current_collection.alias}'")

class CollectionRemoveCommand(BaseModel):
    """
    Removes a collection.
    """

    alias: CliPositionalArg[str]
    """The alias of the collection."""

    def cli_cmd(self) -> None:
        print(f"Removing collection with alias '{self.alias}'...")
        found = False
        for collection in settings.collections:
            if collection.alias == self.alias:
                settings.collections.remove(collection)
                settings.save()
                print(f"Collection with alias '{self.alias}' successfully removed.")
                found = True
                break

        if not found:
            print(f"Collection with alias '{self.alias}' not found.")

class CollectionCommands(BaseModel):
    """
    Collection commands.
    """

    create: CliSubCommand[CollectionCreateCommand]
    """Creates a new collection."""

    set: CliSubCommand[CollectionSetCommand]
    """Sets the current collection."""

    current: CliSubCommand[CollectionShowCurrentCommand]
    """Shows the current collection."""

    remove: CliSubCommand[CollectionRemoveCommand]
    """Removes a collection."""

    rm: CliSubCommand[CollectionRemoveCommand]
    """Alias for 'remove'."""

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
