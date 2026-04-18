import sys
from pathlib import Path
import sqlite3

import pytest

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from app import app as flask_app  # noqa: E402
from database.reset_db import reset_db  # noqa: E402


@pytest.fixture()
def client():
    reset_db()
    flask_app.config.update(TESTING=True)
    with flask_app.test_client() as client:
        yield client


def login(client, email="test@test.com", password="test"):
    return client.post(
        "/auth/login",
        data={"email": email, "password": password},
        follow_redirects=False,
    )


def get_first_cart_item_id(user_id: int = 1) -> int | None:
    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        row = con.execute(
            "SELECT id FROM cart_items WHERE user_id = ? ORDER BY id DESC LIMIT 1",
            (user_id,),
        ).fetchone()
        return int(row[0]) if row else None
    finally:
        con.close()


def test_home_requires_no_login(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Welcome" in resp.data


def test_protected_routes_redirect_to_login_when_logged_out(client):
    for path in ["/products/", "/cart/", "/orders/history", "/profile/ping"]:
        resp = client.get(path, follow_redirects=False)
        assert resp.status_code == 302
        assert resp.headers["Location"].endswith("/auth/login")


def test_login_redirects_to_products(client):
    resp = login(client)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/products")


def test_register_then_login(client):
    resp = client.post(
        "/auth/register",
        data={"full_name": "New User", "email": "new.user@example.com", "password": "pass"},
        follow_redirects=False,
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/auth/login")

    resp = login(client, email="new.user@example.com", password="pass")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/products")


def test_products_access_after_login(client):
    login(client)
    resp = client.get("/products/", follow_redirects=False)
    assert resp.status_code == 200


def test_cart_add_update_remove_and_total(client):
    login(client)

    resp = client.post(
        "/cart/add",
        data={"product_id": "1", "quantity": "2"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"USB-C Cable" in resp.data

    cart_item_id = get_first_cart_item_id(user_id=3)
    assert cart_item_id is not None

    resp = client.post(
        f"/cart/update/{cart_item_id}",
        data={"quantity": "3"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    assert b"$26.97" in resp.data

    resp = client.post(f"/cart/remove/{cart_item_id}", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Your cart is empty." in resp.data


def test_checkout_multiple_items_creates_order_and_clears_cart(client):
    login(client)
    client.post("/cart/add", data={"product_id": "1", "quantity": "1"})
    client.post("/cart/add", data={"product_id": "2", "quantity": "2"})

    resp = client.post("/orders/checkout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Order" in resp.data

    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        order_count = con.execute("SELECT COUNT(*) FROM orders WHERE user_id = 3").fetchone()[0]
        cart_count = con.execute("SELECT COUNT(*) FROM cart_items WHERE user_id = 3").fetchone()[0]
    finally:
        con.close()

    assert order_count == 1
    assert cart_count == 0


def test_checkout_page_redirects_to_cart_when_empty(client):
    login(client)
    resp = client.get("/orders/checkout", follow_redirects=False)
    assert resp.status_code == 302
    assert "/cart/" in resp.headers["Location"]


def test_reset_clears_session_and_db(client):
    login(client)
    client.post("/cart/add", data={"product_id": "1", "quantity": "1"})

    resp = client.post("/reset", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")

    resp = client.get("/products/", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/auth/login")


def test_api_products_available_logged_out(client):
    resp = client.get("/api/products")
    assert resp.status_code == 200
    data = resp.get_json()
    assert isinstance(data, dict)
    assert "products" in data


def test_api_cart_requires_login(client):
    resp = client.get("/api/cart")
    assert resp.status_code == 401
