# SQLite Clone

A SQLite clone implementation in Python, focusing on core database functionality including B+ trees for indexing and SQL command parsing.

## Current Implementation Status

This is a work in progress. Currently implemented features:

- Basic SQL Commands:

  - `SELECT` - Fully working with equality (`=`) comparisons
  - `INSERT` - Fully working
  - `UPDATE` - Not yet implemented
  - `DELETE` - Not yet implemented

- B+ Tree indexing is implemented but currently only works for the `id` column

## Supported Commands

### SQL Commands

#### SELECT

```sql
SELECT column1, column2, ... FROM table_name [WHERE column = value]
SELECT * FROM table_name [WHERE column = value]
```

#### INSERT

```sql
INSERT INTO table_name VALUES (value1, value2, ...)
```

### Meta Commands

All meta commands start with a dot (`.`):

- `.help` - Display help message
- `.exit` - Exit the program
- `.build` - Build a new table
- `.schema` - Display a table's schema

## Acknowledgments

This project was built with the help of the following educational resources:

- [How Do Databases Work? | Interview Pen](https://youtu.be/FnsIJAaGRk4) 
- [Understanding B-Trees: The Data Structure Behind Modern Databases | Spanning Tree](https://youtu.be/K1a2Bk8NrYQ)

These videos provided valuable insights into database internals and guided the implementation of key features in this project.
