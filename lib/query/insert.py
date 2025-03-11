def insertExecutor(command):
    from lib.bplus_tree import insert_into_bplus_tree

    command["table"] = command["table"].lower()

    with open(f"db/{command['table']}.db", "ab+") as f:
        f.seek(0, 2)
        offset = f.tell()

        values_str = ",".join(str(value) for value in command["values"])
        record = values_str + "\n"

        f.write(record.encode("utf-8"))

        primary_key = command["values"][0]

    insert_into_bplus_tree(command["table"], primary_key, offset)

    print(f"Inserted {len(command['values'])} values into {command['table']}")


__all__ = ["insertExecutor"]
