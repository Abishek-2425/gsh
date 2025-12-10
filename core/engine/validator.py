"""
validator.py
Validate parsed command and combine model-provided risk/confidence with internal checks.
"""

from __future__ import annotations
from typing import Dict, Any
from pydantic import BaseModel, Field, confloat
from flyn.core import safety
from flyn.config.loader import get_config

class GenOutput(BaseModel):
    command: str
    explanation: str
    confidence: confloat(ge=0.0, le=1.0) = Field(default=0.5)
    risk_tags: list[str] = Field(default_factory=list)

def validate_generated(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Accepts raw parsed dict (from parser.extract_json_like), returns structured dict:
    { ok: bool, reason: str | None, command, confidence, risk, needs_confirmation }
    """
    cfg = get_config()
    try:
        g = GenOutput(**obj)
    except Exception as e:
        return {"ok": False, "reason": f"invalid model output: {e}"}

    cmd = g.command.strip()
    model_conf = float(g.confidence or 0.0)
    internal_risk = safety.risk_level(cmd)
    needs_confirmation = safety.requires_confirmation(cmd)

    # If model confidence is low, mark it for review
    min_conf = float(cfg.get("safety.min_confidence_to_auto_run", 0.9))
    low_confidence = model_conf < min_conf

    ok = True
    reason = None
    if safety.is_dangerous(cmd):
        ok = False
        reason = "command flagged as dangerous by internal policy"
    elif low_confidence:
        ok = False
        reason = "model confidence below threshold"

    return {
        "ok": ok,
        "reason": reason,
        "command": cmd,
        "confidence": model_conf,
        "risk": internal_risk,
        "need_confirmation": needs_confirmation or low_confidence,
        "raw": g.dict()
    }
