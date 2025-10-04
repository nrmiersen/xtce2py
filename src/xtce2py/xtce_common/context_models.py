"""Context models for XTCE objects."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Endianness(str, Enum):
    """Enumeration for byte order (endianness)."""

    BIG = "be"
    LITTLE = "le"

    def __str__(self) -> str:
        """Return the string representation of the enum value."""
        return self.value


class FinalDataType(str, Enum):
    """Enumeration for the final Python data types a parameter can represent."""

    INT = "int"
    FLOAT = "float"
    STRING = "str"
    BINARY = "bytes"
    BOOLEAN = "bool"

    def __str__(self) -> str:
        """Return the string representation of the enum value."""
        return self.value


@dataclass
class EncodingContext:
    """Container for encoding context information."""

    signed: bool
    size_in_bits: int
    format_specifier: str
    final_type: FinalDataType
    byte_significance_list: list[int]
    needs_byte_reordering: bool = False
    endianness: Endianness = Endianness.BIG
    needs_transform: bool = False
    reverse_bits: bool = False
    custom_byte_order: bool = False
    custom_decoder: str | None = None


@dataclass
class RestrictionContext:
    """Context for a single RestrictionCriteria."""

    parameter_ref: str
    comparison_operator: str
    value: Any


@dataclass
class ParameterContext:
    """Context for a single Parameter."""

    name: str
    python_type: Any
    encoding: EncodingContext
    description: str | None = None


@dataclass
class ContainerDetailsContext:
    """Context holding all details for a single container."""

    python_name: str
    is_abstract: bool
    has_children: bool
    restrictions: list[RestrictionContext] = field(default_factory=list)
    parameters: list[ParameterContext] = field(default_factory=list)

    @property
    def param_formats(self) -> list[str]:
        """Helper to get just the format strings for the template."""
        return [p.encoding.format_specifier for p in self.parameters]

    @property
    def param_names(self) -> list[str]:
        """Helper to get just the parameter names for the template."""
        return [p.name for p in self.parameters]

    @property
    def total_bits_at_this_level(self) -> int:
        """Calculates total bits for all parameters defined at this level."""
        total = 0
        for p in self.parameters:
            # Assumes format_specifier is like "uint:16", "pad:4", etc.
            try:
                spec_parts = p.encoding.format_specifier.split(":")
                if len(spec_parts) == 2:
                    total += int(spec_parts[1])
            except (ValueError, IndexError):
                pass  # Handle cases with no ':'
        return total
