"""Context models for XTCE objects."""

from dataclasses import dataclass, field
from typing import Any, Generic, Optional, TypeVar

T_Argument = TypeVar("T_Argument")
T_ExecutionStep = TypeVar("T_ExecutionStep", bound="BaseExecutionStep[Any]")


@dataclass
class XtceMetadataContext:
    """Container for XTCE metadata information."""

    name: str = "unknown"
    description: Optional[str] = ""
    version: Optional[str] = "1.0.0"
    date: Optional[str] = ""
    classification: Optional[str] = ""
    authors: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    history: list[str] = field(default_factory=list)


@dataclass
class BaseExecutionStep(Generic[T_Argument]):
    """Container for a single execution step in a command's execution sequence."""

    item: T_Argument
    python_condition: Optional[str] = None


@dataclass
class BaseEffectiveCommand(Generic[T_Argument, T_ExecutionStep]):
    """Base container for the effective command definition, including all inherited arguments and execution steps."""

    name: str
    path: str
    parent_path: Optional[str] = None
    is_abstract: bool = False
    all_arguments: list[T_Argument] = field(default_factory=list)
    own_arguments: list[T_Argument] = field(default_factory=list)
    execution_steps: list[T_ExecutionStep] = field(default_factory=list)
    argument_assignments: dict[str, str] = field(default_factory=dict)


@dataclass
class CodecRecipeItem:
    """A single entry in an encoding recipe."""

    name: str
    value_src: str
    bits: int
    encoding: str
    byte_order: str
    condition: Optional[str] = None


@dataclass
class PydanticField:
    """A field definition for a Pydantic model."""

    name: str
    type_hint: str
    default: str | None = None
    is_fixed: bool = False
    required_import: Optional[str] = None


@dataclass
class CommandViewModel:
    """A view model representing the data needed to generate a command class."""

    class_name: str
    parent_class: str
    docstring: str
    fields: list[PydanticField]
    encode_steps: list[CodecRecipeItem]
    inherited_defaults: dict[str, str] = field(default_factory=dict)
    required_enums: set[str] = field(default_factory=set)


@dataclass
class EnumViewModel:
    """A view model representing the data needed to generate an enum class."""

    name: str
    description: str
    values: dict[str, int] = field(default_factory=dict)
