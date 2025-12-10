"""
run.py - generate, validate and (optionally) execute the command
"""

from __future__ import annotations
import typer
from flyn.core import generator, executor
from flyn.cli.render.blocks import command_block, risk_block, output_block, notes_block
from flyn.core import safety
from flyn.config.loader import get_config
from flyn.core.history import append_entry

app = typer.Typer()

@app.command("run")
def run(instruction: str, confirm: bool = typer.Option(False, "--confirm", "-y"), no_dry: bool = typer.Option(False, "--no-dry", "--execute")):
    """
    Generate a command and execute it (subject to safety rules).
    By default this will be a dry-run. Use --confirm and --no-dry to actually run.
    """
    cfg = get_config()
    res = generator.generate_structured(instruction)
    if not res.get("ok"):
        typer.secho(f"Rejected: {res.get('reason')}", fg=typer.colors.RED)
        typer.echo(res.get("model_raw", ""))
        raise typer.Exit(code=2)

    cmd = res["command"]
    typer.echo(command_block(cmd))
    typer.echo(risk_block(res.get("risk", "low"), res.get("confidence", 0.0)))
    typer.echo(notes_block(res.get("raw", {}).get("explanation", "")))

    needs_confirm = bool(res.get("need_confirmation"))
    effective_dry = True if not no_dry else False
    # if config forces dry-run default
    if cfg.get("general.dry_run_default", True) and not no_dry:
        effective_dry = True

    if needs_confirm and not confirm:
        typer.secho("Command requires confirmation (danger/low confidence). Use --confirm to proceed.", fg=typer.colors.YELLOW)
        raise typer.Exit(code=3)

    # final check: safety blacklist
    if safety.is_dangerous(cmd) and not confirm:
        typer.secho("Refusing to run dangerous command without --confirm.", fg=typer.colors.RED)
        raise typer.Exit(code=4)

    result = executor.run_command(cmd, dry_run=effective_dry)
    typer.echo(output_block(result.get("stdout", ""), result.get("stderr", "")))
    append_entry({"instruction": instruction, "command": cmd, "executed": not effective_dry, "result": {"ok": result.get("ok"), "rc": result.get("rc")}})
