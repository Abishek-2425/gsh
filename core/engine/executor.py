"""
executor.py
Safe command execution: dry-run, timeouts, safe_workdir, capture output.
"""

from __future__ import annotations
import shlex
import subprocess
from typing import Dict, Any
from pathlib import Path
import os
from flyn.config.loader import get_config

def _get_safe_workdir() -> Path:
    cfg = get_config()
    p = Path(cfg.get("general.safe_workdir") or "~/.local/share/flyn/sandbox").expanduser()
    p.mkdir(parents=True, exist_ok=True)
    return p

def run_command(cmd: str, timeout: int | None = None, dry_run: bool = True) -> Dict[str, Any]:
    """
    Execute the command in a restricted working directory.
    Returns dict with keys: ok, rc, stdout, stderr, dry_run, error
    """
    cfg = get_config()
    if timeout is None:
        timeout = int(cfg.get("safety.max_timeout_seconds", 30))
    safe_dir = _get_safe_workdir()
    result: Dict[str, Any] = {"dry_run": bool(dry_run), "cmd": cmd}

    if dry_run or cfg.get("general.dry_run_default", True):
        result.update({"ok": True, "rc": None, "stdout": "", "stderr": ""})
        return result

    args = shlex.split(cmd)
    try:
        proc = subprocess.run(args, capture_output=True, text=True, cwd=str(safe_dir), timeout=timeout)
        result.update({
            "ok": proc.returncode == 0,
            "rc": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr
        })
    except subprocess.TimeoutExpired as e:
        result.update({"ok": False, "rc": None, "stdout": e.stdout or "", "stderr": f"timeout: {e}"})
    except FileNotFoundError as e:
        result.update({"ok": False, "rc": None, "stderr": f"executable not found: {e}"})
    except Exception as e:
        result.update({"ok": False, "rc": None, "stderr": str(e)})
    return result
