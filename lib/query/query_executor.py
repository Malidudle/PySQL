from lib.query.select import selectExecutor
from lib.query.insert import insertExecutor
from lib.query.update import updateExecutor
from lib.query.delete import deleteExecutor


def queryExecutor(command):
    match command["verb"]:
        case "SELECT":
            return selectExecutor(command)
        case "INSERT":
            return insertExecutor(command)
        case "UPDATE":
            return updateExecutor(command)
        case "DELETE":
            return deleteExecutor(command)
        case _:
            raise ValueError(f"Invalid command: {command['verb']}")


__all__ = ["queryExecutor"]
