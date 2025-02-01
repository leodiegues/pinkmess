from datetime import datetime
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

    path: CliPositionalArg[Path]
    """The path to the collection."""

    name: str | None = None
    """The alias of the collection."""

    llm_model: KnownModelName | None = None
    """The LLM model to be used for the collection."""

    llm_settings: ModelSettings | None = None
    """The LLM settings to be used for the collection."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def cli_cmd(self) -> None:
        print("Creating new collection...")
        new_collection_path = self.path.resolve().absolute()
        new_collection_path.mkdir(parents=True, exist_ok=True)
        new_collection = Collection(
            index=len(settings.collections),
            path=new_collection_path,
            name=self.name,
            llm_model=self.llm_model or settings.default_llm_model,
            llm_settings=self.llm_settings or settings.default_llm_settings,
        )

        for collection in settings.collections:
            if collection.path == new_collection.path:
                print(f"Collection already exists: {new_collection_path}")
                return

            if self.name is not None and collection.name == self.name:
                print(f"Collection with name '{self.name}' already exists.")
                return

        settings.collections.append(new_collection)
        settings.save()
        print(f"Collection successfully added: {self.path.resolve().absolute()}")


class CollectionSetCommand(BaseModel):
    """
    Sets the current collection.
    """

    name: CliPositionalArg[str]
    """The alias of the collection."""

    def cli_cmd(self) -> None:
        print(f"Setting current collection to {self.name}...")
        found = False
        for collection in settings.collections:
            if collection.name == self.name:
                settings.current_collection_index = collection.index
                settings.save()
                print(f"Current collection successfully set to alias: {self.name}")
                found = True
                break

        if not found:
            print(f"Collection with alias '{self.name}' not found.")


class CollectionShowCurrentCommand(BaseModel):
    """
    Shows the current collection.
    """

    def cli_cmd(self) -> None:
        if settings.current_collection is None:
            print("No current collection found.")
            return
        print(f"Current collection: '{settings.current_collection.name}'")


class CollectionListCommand(BaseModel):
    """
    Lists the collections.
    """

    def cli_cmd(self) -> None:
        if not settings.collections:
            print("No collections found.")
            return

        print("Collections:")
        for collection in settings.collections:
            print(f" -> {collection.name}: {collection.path.absolute()}")


class CollectionRemoveCommand(BaseModel):
    """
    Removes a collection.
    """

    name: CliPositionalArg[str]
    """The alias of the collection."""

    def cli_cmd(self) -> None:
        print(f"Removing collection named '{self.name}'...")
        found = False
        for collection in settings.collections:
            if collection.name == self.name:
                settings.collections.remove(collection)
                settings.save()
                print(f"Collection '{self.name}' successfully removed.")
                found = True
                break

        if not found:
            print(f"Collection '{self.name}' not found.")


class CollectionStatsCommand(BaseModel):
    """
    Shows the statistics of a collection.
    """

    def cli_cmd(self) -> None:
        collection = settings.current_collection
        n_notes = len(list(collection.path.glob("*.md")))
        created_at = datetime.fromtimestamp(collection.path.stat().st_ctime)
        updated_at = datetime.fromtimestamp(collection.path.stat().st_mtime)

        print(f"Statistics of collection '{collection.name}':")
        print(f" -> Number of notes:  {n_notes}")
        print(f" -> Created at:       {created_at.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f" -> Last modified at: {updated_at.strftime('%Y-%m-%d %H:%M:%S')}")


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

    list: CliSubCommand[CollectionListCommand]
    """Lists the collections."""

    ls: CliSubCommand[CollectionListCommand]
    """Alias for 'list'."""

    remove: CliSubCommand[CollectionRemoveCommand]
    """Removes a collection."""

    rm: CliSubCommand[CollectionRemoveCommand]
    """Alias for 'remove'."""

    stats: CliSubCommand[CollectionStatsCommand]
    """Shows the statistics of a collection."""

    def cli_cmd(self) -> None:
        CliApp.run_subcommand(self)
