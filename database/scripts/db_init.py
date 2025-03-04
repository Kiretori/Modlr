import sqlite3
from database.scripts import db_queries as queries
conn = sqlite3.connect("database/app.db")
cur = conn.cursor()



with open("database/sql/schema.sql", "r") as schema_file:
    sql_script = schema_file.read()

tables = {"profiles", "model_types", "models", "model_features", "model_versions"}

for table in tables:
    print(f"Dropping table: {table}")
    cur.execute(f"DROP TABLE IF EXISTS {table};")



cur.executescript(sql_script)



queries.insert_model_type(cur, "Regressor", "Regression model type")
queries.insert_model_type(cur, "Classifier", "Classifier model type")





conn.commit()
print("Changes commited")
conn.close()