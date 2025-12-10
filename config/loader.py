"""
config/loader.py
Simple config loader with defaults.toml + user overrides.
Provides: get(key), set(key,value), reset(), save()
"""

from __future__ import annotations
import toml
from pathlib import Path
import os
import json
from typing import Any
from copy import deepcopy

DEFAULTS_PATH = Path(__file__).parent / "defaults.toml"
USER_CONFIG_PATH = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config")) / "flyn" / "config.toml"

class Config:
    def __init__(self, defaults_path: Path = DEFAULTS_PATH, user_path: Path = USER_CONFIG_PATH):
        self.defaults_path = defaults_path
        self.user_path = Path(user_path)
        self._defaults = self._load_toml(defaults_path)
        self._user = self._load_user()
        self._merged = self._merge(deepcopy(self._defaults), deepcopy(self._user))

    def _load_toml(self, path: Path) -> dict:
        try:
            with open(path, "r", encoding="utf-8") as f:
                return toml.load(f)
        except FileNotFoundError:
            return {}

    def _load_user(self) -> dict:
        try:
            with open(self.user_path, "r", encoding="utf-8") as f:
                return toml.load(f)
        except FileNotFoundError:
            return {}

    def _merge(self, base: dict, override: dict) -> dict:
        # simple deep merge
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                base[k] = self._merge(base[k], v)
            else:
                base[k] = v
        return base

    def get(self, dotted_key: str, default: Any = None) -> Any:
        parts = dotted_key.split(".")
        cur = self._merged
        for p in parts:
            if isinstance(cur, dict) and p in cur:
                cur = cur[p]
            else:
                return default
        return cur

    def set(self, dotted_key: str, value: Any) -> None:
        parts = dotted_key.split(".")
        cur = self._merged
        for p in parts[:-1]:
            if p not in cur or not isinstance(cur[p], dict):
                cur[p] = {}
            cur = cur[p]
        cur[parts[-1]] = value

    def reset(self) -> None:
        self._user = {}
        self._merged = deepcopy(self._defaults)

    def save(self) -> None:
        # ensure directory
        self.user_path.parent.mkdir(parents=True, exist_ok=True)
        # save only user overrides by computing diff (naive)
        # Simpler: overwrite whole config with merged (acceptable)
        with open(self.user_path, "w", encoding="utf-8") as f:
            toml.dump(self._merged, f)

# singleton instance convenience
_config_singleton: Config | None = None

def get_config() -> Config:
    global _config_singleton
    if _config_singleton is None:
        _config_singleton = Config()
    return _config_singleton
