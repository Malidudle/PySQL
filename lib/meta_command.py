from lib.schema_builder import build
from lib.schema_viewer import schemaViewer

command_dict = {
    "exit": exit,
    "help": lambda: print(
        """
        .help: Display this help message
        .exit: Exit the program
        .build: Build a new table
        .schema: Display a table's schema
        """
    ),
    "build": build,
    "schema": schemaViewer,
}


def metaCommand(command):
    if command in command_dict:
        command_dict[command]()
    else:
        print(f"Unknown command: {command}")


__all__ = ["metaCommand"]
