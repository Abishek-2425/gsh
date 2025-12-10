"""
exp.py - explain a raw command using parser + safety (lightweight)
"""

from __future__ import annotations
import typer
from flyn.core.parser import parse_command_from_model
from flyn.core import safety
from flyn.cli.render.blocks import command_block, risk_block, notes_block

app = typer.Typer()

@app.command("exp")
def explain(raw_text: str):
    """
    Explain a raw command or model text: show command + risk.
    """
    cmd = parse_command_from_model(raw_text) or raw_text
    typer.echo(command_block(cmd))
    typer.echo(risk_block(safety.risk_level(cmd), 0.0))
    typer.echo(notes_block("Explanation not available (use generator for full explanation)"))
