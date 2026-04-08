from flask import Blueprint, redirect, render_template, request, session, url_for

from backend.cart import service
from bugs.bug_loader import is_bug_enabled


bp = Blueprint("cart", __name__, url_prefix="/cart")

_TOTAL_CACHE_KEY = "cart_total_cents"


def _require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None, redirect(url_for("auth.login"))
    return int(user_id), None


def _maybe_override_total(cart: dict) -> dict:
    if not is_bug_enabled("bug_cart_total_rounding"):
        session.pop(_TOTAL_CACHE_KEY, None)
        return cart

    cached = session.get(_TOTAL_CACHE_KEY)
    if cached is None:
        session[_TOTAL_CACHE_KEY] = cart["total_cents"]
        return cart

    cart["total_cents"] = int(cached)
    return cart


def _update_cached_total(user_id: int) -> None:
    if not is_bug_enabled("bug_cart_total_rounding"):
        return
    cart = service.get_cart(user_id)
    session[_TOTAL_CACHE_KEY] = cart["total_cents"]


@bp.get("/")
def view_cart():
    user_id, response = _require_login()
    if response:
        return response

    data = _maybe_override_total(service.get_cart(user_id))
    cart_items = data.get("items") or []
    if not isinstance(cart_items, list):
        cart_items = list(cart_items)
    cart_total_cents = int(data.get("total_cents") or 0)
    message = request.args.get("message", "")
    return render_template(
        "cart/view.html",
        cart_items=cart_items,
        cart_total_cents=cart_total_cents,
        message=message,
    )


@bp.post("/add")
def add_to_cart():
    user_id, response = _require_login()
    if response:
        return response

    product_id = int(request.form.get("product_id", "0") or 0)
    quantity = int(request.form.get("quantity", "1") or 1)
    ok, message = service.add_item(user_id, product_id, quantity)
    _update_cached_total(user_id)
    return redirect(url_for("cart.view_cart", message=message if ok else message))


@bp.post("/update/<int:cart_item_id>")
def update_cart_item(cart_item_id: int):
    user_id, response = _require_login()
    if response:
        return response

    quantity = int(request.form.get("quantity", "1") or 1)
    ok, message = service.update_quantity(user_id, cart_item_id, quantity)
    _update_cached_total(user_id)
    return redirect(url_for("cart.view_cart", message=message if ok else message))


@bp.post("/remove/<int:cart_item_id>")
def remove_from_cart(cart_item_id: int):
    user_id, response = _require_login()
    if response:
        return response

    ok, message = service.remove_item(user_id, cart_item_id)
    return redirect(url_for("cart.view_cart", message=message if ok else message))
