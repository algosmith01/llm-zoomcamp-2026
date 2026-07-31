import duckdb

con = duckdb.connect("logfire.duckdb")

print(con.sql("SHOW SCHEMAS").fetchall())
print(con.sql("SHOW TABLES FROM raw").fetchall())

df = con.sql("""
    SELECT *
    FROM raw.records
    LIMIT 10
""").df()

print(df)