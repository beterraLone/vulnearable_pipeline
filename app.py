from fastapi import FastAPI
import sqlite3

app = FastAPI(
    title="Customer Service API",
    description="Учебный сервис для демонстрации DAST сканирования",
    version="1.0.0"
)

# Создаем учебную базу данных прямо в памяти
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, secret TEXT)")
    cursor.execute("DELETE FROM users")
    cursor.execute("INSERT INTO users (username, secret) VALUES ('admin', 'SUPER_SECRET_KEY_123')")
    cursor.execute("INSERT INTO users (username, secret) VALUES ('john', 'john_password')")
    conn.commit()
    conn.close()

init_db()

@app.get("/")
def root():
    return {"status": "ok", "message": "API is running"}

# ВНИМАНИЕ: ЭНДПОИНТ С КРИТИЧЕСКОЙ УЯЗВИМОСТЬЮ SQL INJECTION (OWASP Top 10)
# Разработчик сложил строку f-стрингом вместо параметризованного запроса!
@app.get("/api/users/search")
def search_user(name: str):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # ВОТ ОНА ДЫРА: уязвимость SQL-инъекции
    query = f"SELECT id, username FROM users WHERE username = '{name}'"
    cursor.execute(query)
    
    results = cursor.fetchall()
    conn.close()
    return {"found": results}