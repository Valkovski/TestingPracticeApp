from flask import Blueprint, abort, render_template, request, session

from backend.products import service
from backend.profile import service as profile_service


bp = Blueprint("products", __name__, url_prefix="/products")


@bp.get("/")
def list_products():
    category = request.args.get("category") or None
    sort = request.args.get("sort") or None
    data = service.get_product_list(category=category, sort=sort)
    current_user = profile_service.get_profile_summary(session.get("user_id"))
    return render_template(
        "products/list.html",
        products=data["products"],
        categories=data["categories"],
        selected_category=category or "",
        selected_sort=data["sort"],
        current_user=current_user,
    )


@bp.get("/<int:product_id>")
def product_detail(product_id: int):
    product = service.get_product_detail(product_id)
    if not product:
        abort(404)
    return render_template("products/detail.html", product=product)
