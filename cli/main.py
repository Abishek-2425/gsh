"""
main.py - entrypoint wiring Typer app and subcommands
"""

from __future__ import annotations
import typer
from .commands import show as show_cmd
from .commands import run as run_cmd
from .commands import exp as exp_cmd
from .commands import config_cmd as config_cmd_mod

app = typer.Typer(help="flyn — natural language to shell command generator & runner")

# mount commands
app.add_typer(show_cmd.app, name="show")
app.add_typer(run_cmd.app, name="run")
app.add_typer(exp_cmd.app, name="exp")
app.add_typer(config_cmd_mod.app, name="config")

@app.callback(invoke_without_command=True)
def main(ctx: typer.Context):
    if ctx.invoked_subcommand is None:
        typer.echo(app.help)
