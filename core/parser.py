"""
parser.py
Clean raw model output and extract the command string.
This is intentionally defensive.
"""

from __future__ import annotations
import json
import re
from typing import Optional, Dict, Any

def extract_json_like(text: str) -> Optional[Dict[str, Any]]:
    """
    Try to find a JSON object in text. Return parsed dict or None.
    """
    text = text.strip()
    # Attempt direct JSON parse
    try:
        return json.loads(text)
    except Exception:
        pass
    # Attempt to locate first {...} block
    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if m:
        candidate = m.group(0)
        try:
            return json.loads(candidate)
        except Exception:
            pass
    return None

def parse_command_from_model(text: str) -> Optional[str]:
    """
    Parse the 'command' field from model text.
    If no JSON found, try to heuristically extract last code-ish line.
    """
    obj = extract_json_like(text)
    if obj and "command" in obj and isinstance(obj["command"], str):
        cmd = obj["command"].strip()
        return _normalize_whitespace(cmd)
    # Fallback: heuristics - look for lines with backticks or starting with common commands
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    # prefer last line that looks like a shell command
    candidate = None
    for line in reversed(lines):
        if line.startswith("```") or line.startswith("```sh"):
            # skip fences
            continue
        if re.search(r"[a-zA-Z0-9\-\_/\.]+\s", line) or line.startswith("echo") or line.startswith("ls"):
            candidate = line
            break
    if candidate:
        # strip fences and code markers
        candidate = re.sub(r"^`+|`+$", "", candidate).strip()
        return _normalize_whitespace(candidate)
    return None

def _normalize_whitespace(cmd: str) -> str:
    # remove leading/trailing spaces and collapse multiple spaces
    return re.sub(r"\s+", " ", cmd).strip()
