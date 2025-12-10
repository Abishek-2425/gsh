"""
layout.py
Simple layout helpers for CLI sections.
"""

from __future__ import annotations

def divider(char: str = "-", width: int = 60) -> str:
    return char * width

def header(title: str) -> str:
    return f"\n=== {title} ===\n"
