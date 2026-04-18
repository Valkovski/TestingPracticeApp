import json
import os

import pytest


@pytest.fixture(autouse=True)
def disable_bugs_by_default(monkeypatch):
    if os.environ.get("BUGS_JSON") is None:
        monkeypatch.setenv("BUGS_JSON", json.dumps({"all_enabled": False}))
    yield
