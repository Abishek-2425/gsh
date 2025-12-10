"""
config_cmd.py - simple config command wrapper
"""

from __future__ import annotations
import typer
from flyn.config.loader import get_config

app = typer.Typer()

@app.command("get")
def get(key: str):
    cfg = get_config()
    val = cfg.get(key)
    typer.echo(val if val is not None else "")

@app.command("set")
def set_key(key: str, value: str):
    cfg = get_config()
    cfg.set(key, _coerce(value))
    cfg.save()
    typer.echo("saved")

@app.command("reset")
def reset():
    cfg = get_config()
    cfg.reset()
    cfg.save()
    typer.echo("reset to defaults")

@app.command("list")
def list_all():
    cfg = get_config()
    # naive printing
    import toml
    from pathlib import Path
    merged = cfg._merged  # small convenience
    typer.echo(toml.dumps(merged))

def _coerce(v: str):
    # try JSON decode to allow booleans/numbers/lists
    import json
    try:
        return json.loads(v)
    except Exception:
        return v
