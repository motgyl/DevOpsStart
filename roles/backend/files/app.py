import os
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("todo-backend")

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_PORT = os.environ.get("DB_PORT", "5432")
DB_NAME = os.environ.get("DB_NAME", "tododb")
DB_USER = os.environ.get("DB_USER", "todo")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "todo")


def get_conn():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


@app.get("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return jsonify(status="ok", db="reachable"), 200
    except Exception as e:
        log.exception("DB unreachable")
        return jsonify(status="degraded", db="unreachable", error=str(e)), 503


@app.get("/api/todos")
def list_todos():
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute("SELECT id, title, done, created_at FROM todos ORDER BY id DESC")
            rows = cur.fetchall()
        return jsonify(rows)
    finally:
        conn.close()


@app.post("/api/todos")
def create_todo():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="title is required"), 400

    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "INSERT INTO todos (title, done) VALUES (%s, false) RETURNING id, title, done, created_at",
                (title,),
            )
            row = cur.fetchone()
        conn.commit()
        return jsonify(row), 201
    finally:
        conn.close()


@app.patch("/api/todos/<int:todo_id>")
def toggle_todo(todo_id):
    conn = get_conn()
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(
                "UPDATE todos SET done = NOT done WHERE id = %s RETURNING id, title, done, created_at",
                (todo_id,),
            )
            row = cur.fetchone()
        conn.commit()
        if not row:
            return jsonify(error="not found"), 404
        return jsonify(row)
    finally:
        conn.close()


@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            deleted = cur.rowcount
        conn.commit()
        if not deleted:
            return jsonify(error="not found"), 404
        return "", 204
    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 7001)))
