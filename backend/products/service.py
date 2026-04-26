from backend.products import repository
from bugs.bug_loader import is_bug_enabled


def get_product_list(category: str | None, sort: str | None) -> dict:
    chosen_sort = sort if sort in {"price_asc", "price_desc", "name_asc", "name_desc"} else "price_asc"
    categories = repository.list_categories()

    effective_category = category
    if effective_category and is_bug_enabled("bug_products_wrong_filter_results"):
        effective_category = None

    effective_sort = chosen_sort
    if is_bug_enabled("bug_products_broken_sorting") or is_bug_enabled("bug_products_sort_desc_ignored"):
        if chosen_sort == "price_desc":
            effective_sort = "price_asc"

    products = repository.list_products(category=effective_category, sort=effective_sort)
    return {"products": products, "categories": categories, "sort": chosen_sort}


def get_product_detail(product_id: int) -> dict | None:
    effective_id = product_id
    if is_bug_enabled("bug_products_incorrect_details"):
        effective_id = product_id - 1 if product_id > 1 else product_id + 1
    return repository.get_product(effective_id)
