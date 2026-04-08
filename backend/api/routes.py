from flask import Blueprint, jsonify, request, session

from backend.api import service
from bugs.bug_loader import is_bug_enabled


bp = Blueprint("api", __name__, url_prefix="/api")


def _json_response(payload: dict | list | str, status_code: int):
    if is_bug_enabled("bug_api_always_200"):
        status_code = 200

    if status_code == 204:
        return ("", 204) if not is_bug_enabled("bug_api_always_200") else (jsonify({}), 200)

    if isinstance(payload, (dict, list)):
        return jsonify(payload), status_code
    return jsonify({"data": payload}), status_code


def _require_user_id():
    user_id = session.get("user_id")
    if not user_id:
        return None, _json_response({"error": "unauthorized"}, 401)
    return int(user_id), None


@bp.get("/products")
def products():
    category = request.args.get("category") or None
    sort = request.args.get("sort") or None
    data = service.get_products(category=category, sort=sort)
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response(
            {
                "data": data["products"],
                "meta": {"categories": data["categories"], "sort": data["sort"]},
                "category": category,
            },
            200,
        )

    return _json_response(
        {
            "products": data["products"],
            "categories": data["categories"],
            "selected_category": category,
            "sort": data["sort"],
        },
        200,
    )


@bp.get("/cart")
def cart():
    user_id, response = _require_user_id()
    if response:
        return response
    cart_data = service.get_cart(user_id)
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response({"cart_items": cart_data["items"], "total": cart_data["total_cents"]}, 200)
    return _json_response(cart_data, 200)


@bp.post("/cart")
def cart_add():
    user_id, response = _require_user_id()
    if response:
        return response

    payload = request.get_json(silent=True) or {}
    try:
        product_id = int(payload.get("product_id", 0))
        quantity = int(payload.get("quantity", 1))
    except (TypeError, ValueError):
        if not is_bug_enabled("bug_api_missing_validation"):
            return _json_response({"error": "invalid payload"}, 400)
        product_id = 0
        quantity = 1

    ok, message = service.add_cart_item(user_id, product_id, quantity)
    status = 200 if ok else 400
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response({"msg": message, "ok": ok}, status)
    return _json_response({"message": message}, status)


@bp.put("/cart/<int:cart_item_id>")
def cart_update(cart_item_id: int):
    user_id, response = _require_user_id()
    if response:
        return response

    payload = request.get_json(silent=True) or {}
    try:
        quantity = int(payload.get("quantity", 1))
    except (TypeError, ValueError):
        if not is_bug_enabled("bug_api_missing_validation"):
            return _json_response({"error": "invalid payload"}, 400)
        quantity = 1

    ok, message = service.update_cart_item(user_id, cart_item_id, quantity)
    status = 200 if ok else 404
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response({"status": "ok" if ok else "error", "message": message}, status)
    return _json_response({"message": message}, status)


@bp.delete("/cart/<int:cart_item_id>")
def cart_remove(cart_item_id: int):
    user_id, response = _require_user_id()
    if response:
        return response

    ok, message = service.remove_cart_item(user_id, cart_item_id)
    if not ok:
        return _json_response({"error": message}, 404)
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response({"removed": True}, 204)
    return _json_response("", 204)


@bp.get("/orders")
def orders():
    user_id, response = _require_user_id()
    if response:
        return response
    orders_data = service.get_orders(user_id)
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response(orders_data, 200)
    return _json_response({"orders": orders_data}, 200)


@bp.post("/orders")
def orders_checkout():
    user_id, response = _require_user_id()
    if response:
        return response

    ok, message, order_id = service.checkout(user_id)
    if not ok:
        if is_bug_enabled("bug_api_inconsistent_json"):
            return _json_response({"message": message}, 400)
        return _json_response({"error": message}, 400)
    if is_bug_enabled("bug_api_inconsistent_json"):
        return _json_response({"id": order_id, "status": "created"}, 201)
    return _json_response({"message": message, "order_id": order_id}, 201)
