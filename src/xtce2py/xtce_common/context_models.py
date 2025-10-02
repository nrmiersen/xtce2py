"""Context models for XTCE objects."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EncodingContext:
    """Container for encoding context information."""

    signed: bool
    size_in_bits: int
    format_specifier: str
    byte_order_list: list[int]
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
    format_specifier: str
    python_type: Any
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
        return [p.format_specifier for p in self.parameters]

    @property
    def param_names(self) -> list[str]:
        """Helper to get just the parameter names for the template."""
        return [p.name for p in self.parameters]

    @property
    def total_bits_at_this_level(self) -> int:
        """Calculates total bits for pre-flight checks."""
        # A real implementation would parse this from the format specifiers.
        total = 0
        for p in self.parameters:
            try:
                # Extracts the number from a format like "uint:16"
                total += int(p.format_specifier.split(":")[1])
            except (ValueError, IndexError):
                pass  # Handle cases like 'pad' or invalid formats
        return total
