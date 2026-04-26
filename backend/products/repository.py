from backend.common.db import get_db_connection


def list_categories() -> list[str]:
    connection = get_db_connection()
    try:
        rows = connection.execute(
            "SELECT DISTINCT category FROM products ORDER BY category"
        ).fetchall()
        return [row["category"] for row in rows]
    finally:
        connection.close()


def list_products(category: str | None, sort: str) -> list[dict]:
    if sort == "price_desc":
        order_by = "price_cents DESC"
    elif sort == "name_desc":
        order_by = "name DESC"
    elif sort == "name_asc":
        order_by = "name ASC"
    else:
        order_by = "price_cents ASC"
    sql = (
        "SELECT id, name, description, category, price_cents, stock_qty "
        "FROM products "
    )
    params: list[object] = []
    if category:
        sql += "WHERE category = ? "
        params.append(category)
    sql += f"ORDER BY {order_by}"

    connection = get_db_connection()
    try:
        rows = connection.execute(sql, params).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def get_product(product_id: int) -> dict | None:
    connection = get_db_connection()
    try:
        row = connection.execute(
            "SELECT id, name, description, category, price_cents, stock_qty "
            "FROM products WHERE id = ?",
            (product_id,),
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()
