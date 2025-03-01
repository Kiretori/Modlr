import sqlite3

conn = sqlite3.connect("database/app.db")
cur = conn.cursor()



with open("database/sql/schema.sql", "r") as schema_file:
    sql_script = schema_file.read()

tables = {"profiles", "model_types", "models", "model_features", "model_versions"}

for table in tables:
    print(f"Dropping table: {table}")
    cur.execute(f"DROP TABLE IF EXISTS {table};")



cur.executescript(sql_script)
conn.commit()
print("Changes commited")
conn.close()