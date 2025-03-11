from lib.query.get_schema import get_schema


def selectExecutor(command: dict) -> None:
    from lib.bplus_tree import search_bplus_tree
    from pathlib import Path

    table_name = command["table"].lower()
    db_file = Path(f"db/{table_name}.db")

    if not db_file.exists():
        print(f"Table '{table_name}' does not exist")
        return

    try:
        all_columns = ["id"] + get_schema(table_name)
    except FileNotFoundError as e:
        print(f"Schema error: {str(e)}")
        return

    if command.get("columns"):
        selected_columns = []
        column_indices = []
        for col_name in command["columns"]:
            if col_name in all_columns:
                selected_columns.append(col_name)
                column_indices.append(all_columns.index(col_name))
            else:
                print(f"Column '{col_name}' does not exist in table '{table_name}'")
                return
        columns = selected_columns
    else:
        columns = all_columns
        column_indices = list(range(len(all_columns)))

    offset = 0
    where_clause = command.get("where", [])

    if where_clause:
        where_condition = where_clause[0]
        if "value" not in where_condition or "column" not in where_condition:
            print("Invalid WHERE clause format")
            return

        if where_condition["column"] not in all_columns:
            print(
                f"Column '{where_condition['column']}' does not exist in table '{table_name}'"
            )
            return

        if where_condition["column"] == "id":
            offset = search_bplus_tree(table_name, where_condition["value"])

    try:
        with open(db_file, "rb") as f:
            f.seek(offset)
            records = []

            if where_clause and where_clause[0]["column"] == "id":
                record = f.readline().decode("utf-8").strip()
                if record:
                    values = record.split(",")
                    if len(values) == len(all_columns):
                        records.append([values[i] for i in column_indices])
            else:
                while True:
                    record = f.readline().decode("utf-8").strip()
                    if not record:
                        break
                    values = record.split(",")
                    if len(values) == len(all_columns):
                        records.append([values[i] for i in column_indices])

            if not records:
                print("\nNo records found.")
                return

            col_widths = [len(col) for col in columns]
            for record in records:
                for i, value in enumerate(record):
                    col_widths[i] = max(col_widths[i], len(str(value)))

            print("\n" + "=" * (sum(col_widths) + (3 * len(columns)) + 1))
            header = "|"
            for i, col in enumerate(columns):
                header += f" {col.center(col_widths[i])} |"
            print(header)
            print("=" * (sum(col_widths) + (3 * len(columns)) + 1))

            for record in records:
                row = "|"
                for i, value in enumerate(record):
                    row += f" {str(value).ljust(col_widths[i])} |"
                print(row)
            print("=" * (sum(col_widths) + (3 * len(columns)) + 1))
            print(f"\nTotal records: {len(records)}")

    except Exception as e:
        print(f"Error reading from table '{table_name}': {str(e)}")
        return


__all__ = ["selectExecutor"]
