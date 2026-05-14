from fastapi import FastAPI
import oracledb
import os

app = FastAPI()

DB_USER = os.getenv("DB_USER", "system")
DB_PASS = os.getenv("DB_PASS", "oracle")
DB_DSN = os.getenv("DB_DSN", "db-service:1521/xe")

@app.get("/read")
def read_db():
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT text_column FROM my_table")
                rows = cursor.fetchall()
                return {"data": [r[0] for r in rows]}
    except Exception as e:
        return {"data": [], "error": str(e)}

@app.post("/write/{item}")
def write_db(item: str):
    try:
        with oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN) as conn:
            with conn.cursor() as cursor:
                cursor.execute("INSERT INTO my_table (text_column) VALUES (:1)", [item])
                conn.commit()
                return {"status": "success"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}