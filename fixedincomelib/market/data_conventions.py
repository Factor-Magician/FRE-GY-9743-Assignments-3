"""Compounding method labels."""

from enum import Enum

__all__ = ["CompoundingMethod"]


class CompoundingMethod(Enum):
    SIMPLE = "simple"
    ARITHMETIC = "arithmetic"
    COMPOUND = "compound"

    @classmethod
    def from_string(cls, value: str) -> "CompoundingMethod":
        if not isinstance(value, str):
            raise TypeError("value must be a string")
        try:
            return cls(value.lower())
        except ValueError:
            raise ValueError(f"Invalid token: {value}") from None

    def to_string(self) -> str:
        return self.value
