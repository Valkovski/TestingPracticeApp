import os
import secrets

from flask import Flask, redirect, render_template, request, session

from database.reset_db import reset_db

from backend.api.routes import bp as api_bp
from backend.auth.routes import bp as auth_bp
from backend.cart.routes import bp as cart_bp
from backend.orders.routes import bp as orders_bp
from backend.products.routes import bp as products_bp
from backend.profile.routes import bp as profile_bp


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(16)

app.register_blueprint(auth_bp)
app.register_blueprint(products_bp)
app.register_blueprint(cart_bp)
app.register_blueprint(orders_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(api_bp)


def is_logged_in() -> bool:
    return bool(session.get("user_id"))


def get_current_user_id() -> int | None:
    user_id = session.get("user_id")
    return int(user_id) if user_id is not None else None


@app.context_processor
def inject_auth_helpers():
    return {"is_logged_in": is_logged_in, "get_current_user_id": get_current_user_id}


@app.before_request
def require_login_for_store():
    path = request.path or "/"
    if path.startswith("/static/") or path.startswith("/auth/") or path.startswith("/api/"):
        return None

    if path.startswith(("/products", "/cart", "/orders", "/profile")) and not is_logged_in():
        return redirect("/auth/login")
    return None


@app.get("/")
def index():
    if is_logged_in():
        return redirect("/products")
    return render_template("home.html")


@app.post("/reset")
def reset_app():
    reset_db()
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run()
