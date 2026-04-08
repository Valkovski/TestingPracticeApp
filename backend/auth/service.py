from datetime import datetime

from backend.auth import repository
from bugs.bug_loader import is_bug_enabled


def register_user(email: str, password: str, full_name: str) -> tuple[bool, str]:
    email = (email or "").strip().lower()
    full_name = (full_name or "").strip()
    password = password or ""

    if not email or not password or not full_name:
        return False, "All fields are required."

    if not is_bug_enabled("bug_auth_duplicate_email_allowed"):
        existing_user = repository.get_user_by_email(email)
        if existing_user:
            return False, "Email is already registered."

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    repository.create_user(email=email, password=password, full_name=full_name, created_at=created_at)
    return True, "Registration successful."


def authenticate(email: str, password: str) -> dict | None:
    email = (email or "").strip().lower()
    password = password or ""

    user = repository.get_user_by_email(email)
    if not user:
        return None

    if not is_bug_enabled("bug_auth_login_wrong_password") and user["password_hash"] != password:
        return None

    return {"id": user["id"], "email": user["email"], "full_name": user["full_name"]}
