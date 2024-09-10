def format_query(table, columns, condition=None):
    query = f"SELECT {', '.join(columns)} FROM {table}"
    if condition:
        query += f" WHERE {condition}"
    return query
