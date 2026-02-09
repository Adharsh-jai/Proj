from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

def get_db():
    return sqlite3.connect("users.db")

# Create table
conn = get_db()
conn.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT
)
""")
conn.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    conn = get_db()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "users": users
    })

@app.post("/add")
async def add_user(request: Request):
    form = await request.form()
    name = form["name"]
    email = form["email"]

    conn = get_db()
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    return {"status": "success"}

@app.post("/delete/{user_id}")
def delete_user(user_id: int):
    conn = get_db()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    return {"status": "deleted"}
