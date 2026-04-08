import json
from pathlib import Path


BUGS_PATH = Path(__file__).resolve().parent / "bugs.json"


def load_bugs(path: str | Path = BUGS_PATH) -> dict:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    return data if isinstance(data, dict) else {}


def is_bug_enabled(bug_id: str, bugs: dict | None = None) -> bool:
    bugs_data = bugs if bugs is not None else load_bugs()
    bug = bugs_data.get(bug_id, {})
    if not isinstance(bug, dict):
        return False
    return bool(bug.get("enabled", False))

