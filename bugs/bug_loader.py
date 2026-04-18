import os
import json
from pathlib import Path


BUGS_PATH = Path(__file__).resolve().parent / "bugs.json"


def load_bugs(path: str | Path = BUGS_PATH) -> dict:
    env_json = os.environ.get("BUGS_JSON")
    if env_json:
        try:
            data = json.loads(env_json)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}

    file_path = Path(path)
    try:
        with file_path.open("r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, dict) else {}
    except FileNotFoundError:
        return {}


def is_bug_enabled(bug_id: str, bugs: dict | None = None) -> bool:
    bugs_data = bugs if bugs is not None else load_bugs()
    if bool(bugs_data.get("all_enabled", False)):
        return True

    bug_map = bugs_data.get("bugs")
    if isinstance(bug_map, dict) and bug_id in bug_map:
        bug_value = bug_map.get(bug_id)
        if isinstance(bug_value, dict):
            return bool(bug_value.get("enabled", False))
        return bool(bug_value)

    bug = bugs_data.get(bug_id, {})
    if isinstance(bug, dict):
        return bool(bug.get("enabled", False))
    return bool(bug)
