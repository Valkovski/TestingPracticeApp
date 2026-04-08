from datetime import datetime

from backend.orders import repository
from bugs.bug_loader import is_bug_enabled


def get_checkout_summary(user_id: int) -> dict:
    items = repository.list_cart_items_for_checkout(user_id)
    total_cents = 0
    for item in items:
        item["line_total_cents"] = item["quantity"] * item["unit_price_cents"]
        total_cents += item["line_total_cents"]
    return {"items": items, "total_cents": total_cents}


def checkout(user_id: int) -> tuple[bool, str, int | None]:
    summary = get_checkout_summary(user_id)
    if not summary["items"] and not is_bug_enabled("bug_orders_checkout_empty_cart"):
        return False, "Cart is empty.", None

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_cents = summary["total_cents"]
    if is_bug_enabled("bug_orders_wrong_total"):
        total_cents = sum(item["unit_price_cents"] for item in summary["items"])

    order_id = repository.create_order(
        user_id=user_id,
        status="placed",
        total_cents=total_cents,
        created_at=created_at,
    )

    for item in summary["items"]:
        repository.add_order_item(
            order_id=order_id,
            product_id=item["product_id"],
            quantity=item["quantity"],
            unit_price_cents=item["unit_price_cents"],
        )

    if is_bug_enabled("bug_orders_duplicate_order"):
        duplicate_order_id = repository.create_order(
            user_id=user_id,
            status="placed",
            total_cents=total_cents,
            created_at=created_at,
        )
        for item in summary["items"]:
            repository.add_order_item(
                order_id=duplicate_order_id,
                product_id=item["product_id"],
                quantity=item["quantity"],
                unit_price_cents=item["unit_price_cents"],
            )

    repository.clear_cart(user_id)
    return True, "Order placed.", order_id


def get_order_history(user_id: int) -> list[dict]:
    return repository.list_orders(user_id)
