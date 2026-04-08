from backend.common.db import get_db_connection


def list_cart_items_for_checkout(user_id: int) -> list[dict]:
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT "
            "  ci.product_id, "
            "  ci.quantity, "
            "  p.name AS product_name, "
            "  p.price_cents AS unit_price_cents "
            "FROM cart_items ci "
            "JOIN products p ON p.id = ci.product_id "
            "WHERE ci.user_id = ? "
            "ORDER BY ci.id",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def clear_cart(user_id: int) -> None:
    connection = get_db_connection()
    try:
        connection.execute("DELETE FROM cart_items WHERE user_id = ?", (user_id,))
        connection.commit()
    finally:
        connection.close()


def create_order(user_id: int, status: str, total_cents: int, created_at: str) -> int:
    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO orders (user_id, status, total_cents, created_at) "
            "VALUES (?, ?, ?, ?)",
            (user_id, status, total_cents, created_at),
        )
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def add_order_item(
    order_id: int, product_id: int, quantity: int, unit_price_cents: int
) -> None:
    connection = get_db_connection()
    try:
        connection.execute(
            "INSERT INTO order_items (order_id, product_id, quantity, unit_price_cents) "
            "VALUES (?, ?, ?, ?)",
            (order_id, product_id, quantity, unit_price_cents),
        )
        connection.commit()
    finally:
        connection.close()


def list_orders(user_id: int) -> list[dict]:
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT id, status, total_cents, created_at "
            "FROM orders WHERE user_id = ? "
            "ORDER BY id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()

