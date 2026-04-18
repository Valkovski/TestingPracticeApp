import sqlite3
import sys
from pathlib import Path

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


def test_checkout_decrements_stock_when_bug_disabled(client):

    login(client)

    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        before_1 = con.execute("SELECT stock_qty FROM products WHERE id = 1").fetchone()[0]
        before_2 = con.execute("SELECT stock_qty FROM products WHERE id = 2").fetchone()[0]
    finally:
        con.close()

    client.post("/cart/add", data={"product_id": "1", "quantity": "1"})
    client.post("/cart/add", data={"product_id": "2", "quantity": "2"})
    resp = client.post("/orders/checkout", follow_redirects=False)
    assert resp.status_code == 302

    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        after_1 = con.execute("SELECT stock_qty FROM products WHERE id = 1").fetchone()[0]
        after_2 = con.execute("SELECT stock_qty FROM products WHERE id = 2").fetchone()[0]
    finally:
        con.close()

    assert after_1 == before_1 - 1
    assert after_2 == before_2 - 2


def test_checkout_blocks_oversell_when_bug_disabled(client):

    login(client)

    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        con.execute("UPDATE products SET stock_qty = 1 WHERE id = 1")
        con.commit()
    finally:
        con.close()

    client.post("/cart/add", data={"product_id": "1", "quantity": "2"})
    resp = client.post("/orders/checkout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"Not enough stock" in resp.data

    con = sqlite3.connect(str(ROOT_DIR / "app.db"))
    try:
        order_count = con.execute("SELECT COUNT(*) FROM orders WHERE user_id = 3").fetchone()[0]
        cart_count = con.execute("SELECT COUNT(*) FROM cart_items WHERE user_id = 3").fetchone()[0]
        stock_qty = con.execute("SELECT stock_qty FROM products WHERE id = 1").fetchone()[0]
    finally:
        con.close()

    assert order_count == 0
    assert cart_count == 1
    assert stock_qty == 1
