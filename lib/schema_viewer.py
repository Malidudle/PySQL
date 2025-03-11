def schemaViewer():
    from pathlib import Path

    table_name = input("Enter the name of the table: ")

    schema_file = Path(f"db/schemas/{table_name}.schema")
    if not schema_file.exists():
        print(f"Schema for table '{table_name}' does not exist")
        return

    with open(schema_file, "r") as f:
        columns = f.read().split("\n")
        columns = [col for col in columns if col]
        col_widths = [len(col) for col in columns]

        print("\n" + "=" * (sum(col_widths) + (3 * len(columns)) + 1))

        header = "|"
        for i, col in enumerate(columns):
            header += f" {col.center(col_widths[i])} |"
        print(header)

        print("=" * (sum(col_widths) + (3 * len(columns)) + 1))


__all__ = ["schemaViewer"]
