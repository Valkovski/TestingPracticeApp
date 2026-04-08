from flask import Blueprint, redirect, render_template, request, session

from backend.auth import service


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    message = ""
    if request.method == "POST":
        ok, message = service.register_user(
            email=request.form.get("email", ""),
            password=request.form.get("password", ""),
            full_name=request.form.get("full_name", ""),
        )
        if ok:
            return redirect("/auth/login")

    return render_template("auth/register.html", message=message)


@bp.route("/login", methods=["GET", "POST"])
def login():
    message = ""
    if request.method == "POST":
        user = service.authenticate(
            email=request.form.get("email", ""),
            password=request.form.get("password", ""),
        )
        if user:
            session["user_id"] = user["id"]
            return redirect("/products")
        message = "Invalid email or password."

    return render_template("auth/login.html", message=message)


@bp.get("/logout")
def logout():
    session.clear()
    return redirect("/")
