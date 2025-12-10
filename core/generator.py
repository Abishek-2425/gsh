"""
generator.py
High-level pipeline: select backend -> generate -> parse -> validate -> return structured result
"""

from __future__ import annotations
from typing import Dict, Any, Optional
from flyn.config.loader import get_config
from flyn.core.engine.parser import parse_command_from_model, extract_json_like
from flyn.core.engine.validator import validate_generated
from flyn.core.generation_backends.google_genai import GoogleGenAIBackend
from flyn.core.generation_backends.base import GenerationBackend

# Map provider names to backend classes (add more providers here)
_BACKEND_REGISTRY: dict[str, type[GenerationBackend]] = {
    "google": GoogleGenAIBackend,
}

def _choose_backend(name: str | None = None) -> GenerationBackend:
    cfg = get_config()
    provider = name or cfg.get("backend.provider", "google")
    cls = _BACKEND_REGISTRY.get(provider)
    if cls is None:
        # fallback to google placeholder
        cls = GoogleGenAIBackend
    return cls()

def generate_structured(instruction: str, backend_name: Optional[str] = None) -> Dict[str, Any]:
    backend = _choose_backend(backend_name)
    raw = backend.generate(instruction)
    # parse out JSON if possible
    parsed_json = extract_json_like(raw)
    if parsed_json is None:
        # try to extract a heuristic command and wrap into minimal JSON
        cmd = parse_command_from_model(raw)
        parsed_json = {
            "command": cmd or "",
            "explanation": "Parsed heuristically from model output",
            "confidence": 0.0,
            "risk_tags": []
        }
    validated = validate_generated(parsed_json)
    # include raw model output for debugging
    validated["model_raw"] = raw
    return validated
