"""
colors.py
Minimal ANSI helpers (Rich recommended for production).
"""

from __future__ import annotations

class Colors:
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    RESET = "\033[0m"

def color_text(s: str, color: str) -> str:
    return f"{color}{s}{Colors.RESET}"
