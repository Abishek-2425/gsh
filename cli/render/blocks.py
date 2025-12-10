"""
blocks.py
Small reusable CLI output blocks.
"""

from __future__ import annotations
from .colors import Colors, color_text

def command_block(cmd: str) -> str:
    return f"{color_text('Command:', Colors.BLUE)}\n  {cmd}\n"

def risk_block(risk: str, confidence: float) -> str:
    level = risk.upper()
    color = Colors.YELLOW if risk == "medium" else (Colors.RED if risk == "high" else Colors.GREEN)
    return f"{color_text('Risk:', color)} {level} (confidence: {confidence:.2f})\n"

def output_block(stdout: str, stderr: str) -> str:
    out = ""
    if stdout:
        out += f"{color_text('STDOUT:', Colors.GREEN)}\n{stdout}\n"
    if stderr:
        out += f"{color_text('STDERR:', Colors.RED)}\n{stderr}\n"
    return out or "No output\n"

def notes_block(notes: str) -> str:
    return f"{color_text('Notes:', Colors.BOLD)}\n{notes}\n"
