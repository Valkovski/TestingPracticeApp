from backend.cart import service as cart_service
from backend.orders import service as orders_service
from backend.products import service as products_service


def get_products(category: str | None, sort: str | None) -> dict:
    return products_service.get_product_list(category=category, sort=sort)


def get_cart(user_id: int) -> dict:
    return cart_service.get_cart(user_id)


def add_cart_item(user_id: int, product_id: int, quantity: int) -> tuple[bool, str]:
    return cart_service.add_item(user_id, product_id, quantity)


def update_cart_item(user_id: int, cart_item_id: int, quantity: int) -> tuple[bool, str]:
    return cart_service.update_quantity(user_id, cart_item_id, quantity)


def remove_cart_item(user_id: int, cart_item_id: int) -> tuple[bool, str]:
    return cart_service.remove_item(user_id, cart_item_id)


def checkout(user_id: int) -> tuple[bool, str, int | None]:
    return orders_service.checkout(user_id)


def get_orders(user_id: int) -> list[dict]:
    return orders_service.get_order_history(user_id)

