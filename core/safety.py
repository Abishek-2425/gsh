"""
safety.py
Basic detection for dangerous commands and risk scoring.
"""

from __future__ import annotations
import re
from typing import List
from flyn.config.loader import get_config

DEFAULT_BLACKLIST = ["rm -rf", "rm -r", "rm", "dd", "mkfs", ">:","chmod 777", "chown 0:0", "sudo rm"]

def get_blacklist() -> List[str]:
    cfg = get_config()
    bl = cfg.get("safety.blacklist")
    if isinstance(bl, list) and bl:
        return bl
    return DEFAULT_BLACKLIST

def is_dangerous(cmd: str) -> bool:
    cmd_low = cmd.lower()
    for token in get_blacklist():
        if token.lower() in cmd_low:
            return True
    # pattern: redirect to device or raw disk
    if re.search(r"/dev/sd|/dev/nvme|mkfs\.", cmd_low):
        return True
    return False

def risk_level(cmd: str) -> str:
    if is_dangerous(cmd):
        return "high"
    # network ops
    if re.search(r"curl\s+http|wget\s+http|scp\s+", cmd):
        return "medium"
    return "low"

def requires_confirmation(cmd: str) -> bool:
    cfg = get_config()
    if cfg.get("general.confirm_on_danger", True) and is_dangerous(cmd):
        return True
    # also require if risk is high or confidence threshold not met is handled elsewhere
    return False
