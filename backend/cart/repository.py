from backend.common.db import get_db_connection


def get_product(product_id: int) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, name, price_cents, stock_qty FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def get_cart_item_by_user_and_product(user_id: int, product_id: int) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, user_id, product_id, quantity "
            "FROM cart_items WHERE user_id = ? AND product_id = ?",
            (user_id, product_id),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def insert_cart_item(user_id: int, product_id: int, quantity: int, added_at: str) -> int:
    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "INSERT INTO cart_items (user_id, product_id, quantity, added_at) "
            "VALUES (?, ?, ?, ?)",
            (user_id, product_id, quantity, added_at),
        )
        connection.commit()
        return int(cursor.lastrowid)
    finally:
        connection.close()


def update_cart_item_quantity(user_id: int, cart_item_id: int, quantity: int) -> bool:
    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "UPDATE cart_items SET quantity = ? WHERE id = ? AND user_id = ?",
            (quantity, cart_item_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def delete_cart_item(user_id: int, cart_item_id: int) -> bool:
    connection = get_db_connection()
    try:
        cursor = connection.execute(
            "DELETE FROM cart_items WHERE id = ? AND user_id = ?",
            (cart_item_id, user_id),
        )
        connection.commit()
        return cursor.rowcount > 0
    finally:
        connection.close()


def list_cart_items(user_id: int) -> list[dict]:
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT "
            "  ci.id AS cart_item_id, "
            "  ci.quantity, "
            "  p.id AS product_id, "
            "  p.name AS product_name, "
            "  p.price_cents AS price_cents "
            "FROM cart_items ci "
            "JOIN products p ON p.id = ci.product_id "
            "WHERE ci.user_id = ? "
            "ORDER BY ci.id DESC",
            (user_id,),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()

