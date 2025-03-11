def get_schema(table_name: str) -> list[str]:
    from pathlib import Path

    schema_file = Path(f"db/schemas/{table_name}.schema")
    if not schema_file.exists():
        raise FileNotFoundError(f"Schema for table '{table_name}' does not exist")

    with open(schema_file, "r") as f:
        return [line.strip() for line in f if line.strip()]


__all__ = ["get_schema"]
