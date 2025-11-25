import typer
from rich import print

from core.generator import generate_command
from core.safety import analyze_risk
from core.executor import execute_command
from core.history import save_history
from core.config_loader import load_config, update_config, DEFAULT_CONFIG
from core.version import __version__

import json
import os

app = typer.Typer(help="Gensh — Natural-language to shell command converter")

# --------------------------
# Subgroup: gensh config ...
# --------------------------
config_app = typer.Typer(help="View or change configuration")
app.add_typer(config_app, name="config")

# --------------------------
# Subgroup: gensh history ...
# --------------------------
history_app = typer.Typer(help="View or manage command history")
app.add_typer(history_app, name="history")

# --------------------------
# Subgroup: gensh os ...
# --------------------------
os_app = typer.Typer(help="Quick OS selection")
app.add_typer(os_app, name="os")


# =====================================================================
# MAIN COMMAND: gensh run "<instruction>"
# =====================================================================
@app.command()
def run(
    prompt: str = typer.Argument(..., help="Natural language instruction"),
    dry_run: bool = typer.Option(True, "--dry-run/--run", help="Preview or execute")
):
    config = load_config()
    result = generate_command(prompt, config)
    command = result["command"]
    explanation = result["explanation"]

    print(f"[bold cyan]Generated command:[/bold cyan] {command}")
    print(f"[yellow]Explanation:[/yellow] {explanation}")

    risk = analyze_risk(command)
    print(f"[magenta]Risk level:[/magenta] {risk}")

    if dry_run:
        print("[green]Dry run: Command not executed.[/green]")
    else:
        print("[bold green]Executing...[/bold green]")
        execute_command(command)

    save_history(prompt, command, risk)


@app.command("version")
def show_version():
    """
    Show the current gensh version.
    """
    print(f"[bold cyan]gensh version:[/bold cyan] {__version__}")

# =====================================================================
# config subgroup
# =====================================================================

@config_app.command("show")
def config_show():
    """
    Show all the available configuration keys and their values.
    """
    config = load_config()
    print("[bold cyan]Current configuration:[/bold cyan]")
    for k, v in config.items():
        print(f"  [green]{k}[/green]: {v}")


@config_app.command("get")
def config_get(key: str):
    """
    Show the value of a specific configuration key.
    """
    config = load_config()
    if key not in config:
        print(f"[red]Key '{key}' not found in config[/red]")
        raise typer.Exit()
    print(f"[bold cyan]{key}[/bold cyan] = {config[key]}")


@config_app.command("set")
def config_set(key: str, value: str):
    """
    Set the value of a specific configuration key.
    """
    allowed_os = ["windows", "linux", "mac"]

    if key.lower() == "os" and value.lower() not in allowed_os:
        print(f"[red]Invalid OS. Choose from {allowed_os}[/red]")
        raise typer.Exit()

        # Coerce certain keys to float
    if key.lower() == "temperature":
        try:
            value = float(value)
        except ValueError:
            print("[red]Temperature must be a numeric value[/red]")
            raise typer.Exit()
        
    update_config(key, value)
    print(f"[bold green]Updated {key} = {value}[/bold green]")


@config_app.command("reset")
def config_reset():
    """
    Reset the configuration to default values.
    """
    from core.config_loader import CONFIG_PATH

    with open(CONFIG_PATH, "w") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)

    print("[bold green]Configuration reset to defaults[/bold green]")


# =====================================================================
# os subgroup
# =====================================================================

@os_app.command("set")
def os_set(os_name: str):
    allowed = ["windows", "linux", "mac"]

    if os_name.lower() not in allowed:
        print(f"[red]Invalid OS. Choose from {allowed}[/red]")
        raise typer.Exit()

    update_config("os", os_name.lower())
    print(f"[bold green]OS set to {os_name}[/bold green]")


# Convenience commands: gensh os windows / linux / mac
@os_app.command("windows")
def os_windows():
    os_set("windows")


@os_app.command("linux")
def os_linux():
    os_set("linux")


@os_app.command("mac")
def os_mac():
    os_set("mac")


# =====================================================================
# history subgroup
# =====================================================================

HISTORY_FILE = os.path.expanduser("~/.genshpilot_history.json")

@history_app.command("show")
def history_show():
    """
    Show the top 50 command history entries.
    """
    if not os.path.exists(HISTORY_FILE):
        print("[yellow]No history found.[/yellow]")
        return

    data = json.load(open(HISTORY_FILE))

    print("[bold cyan]Command History:[/bold cyan]")
    for entry in data[-50:]:  # show last 50
        print(f"[green]{entry['timestamp']}[/green] — {entry['command']}  ([blue]{entry['risk']}[/blue])")
        print(f"  prompt: {entry['prompt']}")


@history_app.command("clear")
def history_clear():
    """
    Clear the entire command history.
    """
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
        print("[bold green]History cleared.[/bold green]")
    else:
        print("[yellow]History is already empty.[/yellow]")


# =====================================================================
# tools subgroup
# =====================================================================

tools_app = typer.Typer(help="Extra diagnostic and reverse-analysis tools")
app.add_typer(tools_app, name="tools")

# --------------------------------------------------------------
# gensh tools diagnose
# --------------------------------------------------------------
@tools_app.command("diagnose")
def tools_diagnose():
    """
    Diagnose gensh configuration and API connectivity.
    """

    config = load_config()
    print("[bold cyan]gensh Diagnostics[/bold cyan]")
    # 1. Check config keys
    print("\n[green]✔ Loaded configuration[/green]")
    for k, v in config.items():
        print(f"  {k}: {v}")

    # 2. Check API key
    api_key = config.get("api_key") or config.get("gemini_api_key")
    if not api_key:
        print("[red]✘ No Gemini API key configured[/red]")
    else:
        print("[green]✔ API key present[/green]")

    # 3. Attempt model initialization
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(config["model"])
        print(f"[green]✔ Model '{config['model']}' is valid[/green]")
    except Exception as e:
        print(f"[red]✘ Model initialization failed:[/red] {e}")

    # 4. OS check
    print(f"[green]✔ Using OS mode:[/green] {config.get('os')}")


# --------------------------------------------------------------
# gensh tools models
# --------------------------------------------------------------
@tools_app.command("models")
def tools_models():
    """
    List available Gemini models for the configured API key.
    """
    config = load_config()
    api_key = config.get("api_key") or config.get("gemini_api_key")

    if not api_key:
        print("[red]Missing API key. Configure using gensh config set api_key <key>[/red]")
        raise typer.Exit()

    import google.generativeai as genai

    try:
        genai.configure(api_key=api_key)
        models = genai.list_models()
    except Exception as e:
        print(f"[red]Failed to fetch models:[/red] {e}")
        raise typer.Exit()

    print("[bold cyan]Available Gemini models:[/bold cyan]")
    for m in models:
        print(f"  [green]{m.name}[/green]")


# --------------------------------------------------------------
# gensh tools explain "<command>"
# --------------------------------------------------------------
@tools_app.command("explain")
def tools_explain(cmd: str):
    """
    Ask Gemini to explain what a given shell command does.
    """
    config = load_config()
    api_key = config.get("api_key") or config.get("gemini_api_key")
    model_name = config.get("model", "gemini-2.0-flash")

    if not api_key:
        print("[red]Missing API key.[/red]")
        raise typer.Exit()

    import google.generativeai as genai

    # Build reverse prompt
    from core.prompts import build_explain_prompt

    prompt = build_explain_prompt(cmd)

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name)
        res = model.generate_content(prompt)
        text = res.text.strip()
    except Exception as e:
        print(f"[red]Gemini error:[/red] {e}")
        raise typer.Exit()

    print("[bold cyan]Explanation:[/bold cyan]")
    print(text)


def main():
    app()

if __name__ == "__main__":
    app()
