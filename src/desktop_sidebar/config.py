import json
from pathlib import Path
from typing import List, Dict

CONFIG_FILE = Path.home() / ".desktop_sidebar_clocks.json"


def load_clocks() -> List[Dict[str, str]]:
    """Return list of clocks as dicts: {"label": str, "tz": str}

    If the config file doesn't exist or is invalid, return an empty list.
    """
    try:
        if CONFIG_FILE.exists():
            with CONFIG_FILE.open("r", encoding="utf-8") as fh:
                data = json.load(fh)
                if isinstance(data, list):
                    return data
    except Exception:
        pass
    return []


def save_clocks(clocks: List[Dict[str, str]]):
    """Save clocks to the config file (atomically)."""
    tmp = CONFIG_FILE.with_suffix(".tmp")
    tmp.parent.mkdir(parents=True, exist_ok=True)
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(clocks, fh, indent=2)
    tmp.replace(CONFIG_FILE)
