def format_value(value):
    return f"'{value}'" if isinstance(value, str) else str(value)


def write_sql_insert(movies):
    with open("./insert.sql", "a") as bulk_insert_file:
        for m in movies:
            movie = ", ".join(format_value(mov) for mov in m.values())
            bulk_insert_file.write(f"\t({movie}),\n")
