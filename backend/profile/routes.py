from flask import Blueprint


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/ping")
def ping():
    return "profile ok"

