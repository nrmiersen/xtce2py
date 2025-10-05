"""Context models for XTCE objects."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from xtce2py._enums import BitstreamInterpretationToken, Endianness, FinalDataType


@dataclass
class EncodingContext:
    """Container for encoding context information."""

    signed: bool
    size_in_bits: int
    format_specifier: str
    final_type: FinalDataType
    interpretation_token: BitstreamInterpretationToken
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
        return sum(p.encoding.size_in_bits for p in self.parameters)
