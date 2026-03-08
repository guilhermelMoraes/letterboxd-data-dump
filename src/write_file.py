def format_value(value):
    return f"'{value}'" if isinstance(value, str) else str(value)


def write_sql_insert(row):
    with open("./insert.sql", "a") as insert_file:
        movie = ", ".join(format_value(mov) for mov in row.values())
        insert_file.write(f"\t({movie}),\n")
