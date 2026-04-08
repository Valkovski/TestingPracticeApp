from backend.common.db import get_db_connection


def get_user_by_email(email: str) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, email, password_hash, full_name FROM users WHERE email = ?",
            (email,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def get_user_by_id(user_id: int) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, email, password_hash, full_name FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def create_user(email: str, password: str, full_name: str, created_at: str) -> int:
    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO users (email, password_hash, full_name, created_at) "
            "VALUES (?, ?, ?, ?)",
            (email, password, full_name, created_at),
        )
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()

