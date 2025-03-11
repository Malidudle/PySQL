command_list = ["SELECT", "INSERT", "UPDATE", "DELETE"]
verb_list = ["FROM", "WHERE", "INTO", "SET", "VALUES"]
operators = ["=", ">", "<", ">=", "<=", "!="]


def commandParser(command):
    tokens = command.strip().split()

    if not tokens or tokens[0] not in command_list:
        raise ValueError(f"Invalid command: {tokens[0] if tokens else 'Empty command'}")

    parsed_command = {
        "verb": tokens[0],
        "table": None,
        "columns": [],
        "where": [],
        "values": [],
        "set_clause": {},
    }

    i = 1
    current_section = None
    collecting_values = False
    value_buffer = ""

    while i < len(tokens):
        token = tokens[i]

        # Handle VALUES collection
        if collecting_values:
            value_buffer += " " + token
            if ")" in token:
                # Check if this is the end of all values or just one set
                values_str = value_buffer.strip()
                # Reset for next potential value set
                collecting_values = False
                value_buffer = ""

                # Process all value sets
                if "," in values_str and "(" in values_str:
                    # Multiple value sets like (1,'a'),(2,'b')
                    value_sets = []
                    current_set = ""
                    paren_count = 0

                    for char in values_str:
                        if char == "(":
                            paren_count += 1
                            current_set += char
                        elif char == ")":
                            paren_count -= 1
                            current_set += char
                            if paren_count == 0:
                                # Process this complete value set
                                set_values = current_set.strip("()")
                                values = [
                                    v.strip().strip("'\"")
                                    for v in set_values.split(",")
                                ]
                                value_sets.append(values)
                                current_set = ""
                        elif (
                            paren_count > 0 or char.strip()
                        ):  # Skip spaces outside parentheses
                            current_set += char

                    parsed_command["values"] = value_sets
                else:
                    # Single value set
                    values_str = values_str.strip("()")
                    values = [v.strip().strip("'\"") for v in values_str.split(",")]
                    parsed_command["values"] = [values]
            i += 1
            continue

        if token.upper() in verb_list:
            current_section = token.upper()
            i += 1
            continue

        if parsed_command["verb"] == "SELECT":
            if current_section is None:
                if token == "*":
                    parsed_command["columns"] = ["*"]
                else:
                    parsed_command["columns"].extend(token.split(","))
            elif current_section == "FROM":
                parsed_command["table"] = token
            elif current_section == "WHERE":
                if i + 2 < len(tokens) and tokens[i + 1] in operators:
                    parsed_command["where"].append(
                        {
                            "column": token,
                            "operator": tokens[i + 1],
                            "value": tokens[i + 2].strip("'\""),
                        }
                    )
                    i += 2

        elif parsed_command["verb"] == "INSERT":
            if current_section == "INTO":
                parsed_command["table"] = token
            elif current_section == "VALUES":
                if "(" in token:
                    collecting_values = True
                    value_buffer = token
                    # Don't process here - wait until we collect all value sets

        elif parsed_command["verb"] == "UPDATE":
            if current_section is None:
                parsed_command["table"] = token
            elif current_section == "SET":
                if "=" in token:
                    col, val = token.split("=", 1)
                    parsed_command["set_clause"][col.strip()] = val.strip("'\"")

        elif parsed_command["verb"] == "DELETE":
            if current_section == "FROM":
                parsed_command["table"] = token

        i += 1

    print(parsed_command)
    return parsed_command


# # For testing purposes
# if __name__ == "__main__":
#     print(commandParser("SELECT * FROM users WHERE id = 1"))
#     print(commandParser("INSERT INTO users VALUES (1, 'John', 'Doe')"))
#     print(commandParser("INSERT INTO users VALUES(1,'John','Doe')"))


__all__ = ["commandParser"]
