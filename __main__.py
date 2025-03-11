from lib.meta_command import metaCommand
from lib.command_parser import commandParser
from lib.query.query_executor import queryExecutor


def main():
    while True:
        print("sqlite >", end=" ")
        command = input()

        if command[0] == ".":
            metaCommand(command[1:])
        else:
            command = commandParser(command)
            queryExecutor(command)


if __name__ == "__main__":
    main()
