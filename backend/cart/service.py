from datetime import datetime

from backend.cart import repository
from bugs.bug_loader import is_bug_enabled


def get_cart(user_id: int) -> dict:
    items = repository.list_cart_items(user_id)
    total_cents = 0
    for item in items:
        line_total_cents = item["quantity"] * item["price_cents"]
        if is_bug_enabled("bug_cart_total_rounding"):
            line_total_cents = (line_total_cents // 100) * 100
        item["line_total_cents"] = line_total_cents
        total_cents += item["line_total_cents"]
    return {"items": items, "total_cents": total_cents}


def add_item(user_id: int, product_id: int, quantity: int) -> tuple[bool, str]:
    if quantity <= 0:
        return False, "Quantity must be at least 1."

    product = repository.get_product(product_id)
    if not product:
        return False, "Product not found."

    current_qty = repository.get_cart_quantity_for_product(user_id, product_id)
    if current_qty + quantity > product["stock_qty"]:
        return False, "Not enough stock available."

    if not is_bug_enabled("bug_cart_total_rounding"):
        existing = repository.get_cart_item_by_user_and_product(user_id, product_id)
        if existing:
            new_qty = existing["quantity"] + quantity
            repository.update_cart_item_quantity(user_id, existing["id"], new_qty)
            return True, "Item updated in cart."

    added_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repository.insert_cart_item(user_id, product_id, quantity, added_at)
    return True, "Item added to cart."


def update_quantity(user_id: int, cart_item_id: int, quantity: int) -> tuple[bool, str]:
    if quantity <= 0:
        repository.delete_cart_item(user_id, cart_item_id)
        return True, "Item removed."

    ok = repository.update_cart_item_quantity(user_id, cart_item_id, quantity)
    return (True, "Quantity updated.") if ok else (False, "Cart item not found.")


def remove_item(user_id: int, cart_item_id: int) -> tuple[bool, str]:
    ok = repository.delete_cart_item(user_id, cart_item_id)
    return (True, "Item removed.") if ok else (False, "Cart item not found.")
