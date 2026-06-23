import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_PATH = "data/users.db"


def init_user_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users (username, password)
            VALUES (?, ?)
        """, (username, hashed_password))

        conn.commit()
        return True, "註冊成功"

    except sqlite3.IntegrityError:
        return False, "帳號已存在"

    finally:
        conn.close()


def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, username, password
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()
    conn.close()

    if user is None:
        return False, "帳號不存在", None

    user_id, db_username, hashed_password = user

    if not check_password_hash(hashed_password, password):
        return False, "密碼錯誤", None

    return True, "登入成功", {
        "id": user_id,
        "username": db_username
    }