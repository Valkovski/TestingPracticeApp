from backend.common.db import get_db_connection


def get_profile(user_id: int) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, email, full_name FROM users WHERE id = ?",
            (user_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()
