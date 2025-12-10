"""
Base interface for generation backends.
All backends must implement `generate(instruction: str) -> str`
which returns the raw model text output.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Protocol

class GenerationBackend(ABC):
    @abstractmethod
    def generate(self, instruction: str) -> str:
        """
        Given a natural language instruction, return the raw model text (string).
        The generator does not parse or validate the output; that is done by parser/validator.
        """
        raise NotImplementedError
