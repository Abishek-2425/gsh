"""
history.py
Append and read simple history file entries.
"""

from __future__ import annotations
from pathlib import Path
from datetime import datetime
from flyn.config.loader import get_config
import json

def _history_path() -> Path:
    cfg = get_config()
    p = Path(cfg.get("general.history_file") or "~/.local/share/flyn/history.log").expanduser()
    p.parent.mkdir(parents=True, exist_ok=True)
    return p

def append_entry(entry: dict) -> None:
    p = _history_path()
    data = {"ts": datetime.utcnow().isoformat() + "Z", **entry}
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")

def read_entries(limit: int = 100) -> list[dict]:
    p = _history_path()
    if not p.exists():
        return []
    lines = p.read_text(encoding="utf-8").strip().splitlines()
    lines = lines[-limit:]
    out = []
    for l in lines:
        try:
            out.append(json.loads(l))
        except Exception:
            continue
    return out
