def load_sql_statement(file):
    with open(file, "r") as sql_file:
        return sql_file.read()