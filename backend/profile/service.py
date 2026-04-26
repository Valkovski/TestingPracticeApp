from backend.profile import repository


def get_profile_summary(user_id: int | None) -> dict | None:
    if user_id is None:
        return None

    profile = repository.get_profile(user_id)
    if not profile:
        return None

    return {"full_name": profile["full_name"], "email": profile["email"]}
