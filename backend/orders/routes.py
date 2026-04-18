from flask import Blueprint, redirect, render_template, request, session, url_for

from backend.orders import service
from bugs.bug_loader import is_bug_enabled


bp = Blueprint("orders", __name__, url_prefix="/orders")


def _require_login():
    user_id = session.get("user_id")
    if not user_id:
        return None, redirect(url_for("auth.login"))
    return int(user_id), None


@bp.get("/checkout")
def checkout_page():
    user_id, response = _require_login()
    if response:
        return response

    summary = service.get_checkout_summary(user_id)
    if not summary["items"] and not is_bug_enabled("bug_orders_allow_empty_checkout_page"):
        return redirect(url_for("cart.view_cart", message="Cart is empty."))
    message = request.args.get("message", "")
    return render_template("orders/checkout.html", summary=summary, message=message)


@bp.post("/checkout")
def checkout_submit():
    user_id, response = _require_login()
    if response:
        return response

    ok, message, _order_id = service.checkout(user_id)
    if not ok:
        return redirect(url_for("orders.checkout_page", message=message))
    return redirect(url_for("orders.history", message=message))


@bp.get("/history")
def history():
    user_id, response = _require_login()
    if response:
        return response

    orders = service.get_order_history(user_id)
    message = request.args.get("message", "")
    return render_template("orders/history.html", orders=orders, message=message)
