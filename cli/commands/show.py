"""
show.py - generate and display the proposed command, risk, and explanation
"""

from __future__ import annotations
import typer
from flyn.core import generator
from flyn.cli.render.blocks import command_block, risk_block, notes_block

app = typer.Typer()

@app.command("show")
def show(instruction: str):
    """
    Generate a command from natural language and display parsed result.
    """
    res = generator.generate_structured(instruction)
    if not res.get("ok"):
        typer.secho(f"Generation not accepted: {res.get('reason')}", fg=typer.colors.RED)
        # still show model_raw for debug
        typer.echo(res.get("model_raw", ""))
        raise typer.Exit(code=1)

    typer.echo(command_block(res["command"]))
    typer.echo(risk_block(res.get("risk", "low"), res.get("confidence", 0.0)))
    typer.echo(notes_block(res.get("raw", {}).get("explanation", "")))
