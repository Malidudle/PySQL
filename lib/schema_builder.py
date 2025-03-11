def build():
    print(
        """
        WELCOME TO THE SCHEMA BUILDER!
        ==============================

        To create a new table, enter the name of the table you want to create.
        The id column is automatically added to the table.
        You can add as many columns as you want to the table.
        When you are done, enter "DONE" to finish the table.
        To exit the schema builder, enter "EXIT".
        """
    )

    table_name = input("Enter the name of the table: ")
    if table_name == "DONE" or table_name == "EXIT":
        return

    columns = []
    while True:
        column_name = input("Enter the name of the column: ")
        if column_name == "DONE":
            break
        elif column_name == "EXIT":
            return
        else:
            columns.append(column_name)

    with open(f"db/schemas/{table_name}.schema", "w") as f:
        for column in columns:
            f.write(f"{column}\n")

    print(f"Table {table_name} created with columns: {', '.join(columns)}")
