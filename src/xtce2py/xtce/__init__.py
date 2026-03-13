"""XTCE module."""

from .context import (
    BaseExecutionStep,
    CodecRecipeItem,
    CommandViewModel,
    EncodingInfo,
    EnumViewModel,
    PydanticField,
    XtceMetadataContext,
)
from .parser import BaseXtceParser
from .processor import BaseProcessor
from .system_context import SystemContext
from .utils import sanitize_enum_label, unwrap
from .validation import get_xtce_parser, validate_xtce_file
from .validator import BaseXtceValidator, XtceValidationError
from .version import XtceVersion, get_xtce_version

ExecutionStep = BaseExecutionStep

__all__ = [
    "BaseExecutionStep",
    "CodecRecipeItem",
    "CommandViewModel",
    "EncodingInfo",
    "EnumViewModel",
    "ExecutionStep",
    "PydanticField",
    "XtceMetadataContext",
    "BaseXtceParser",
    "BaseProcessor",
    "SystemContext",
    "sanitize_enum_label",
    "unwrap",
    "get_xtce_parser",
    "validate_xtce_file",
    "BaseXtceValidator",
    "XtceValidationError",
    "XtceVersion",
    "get_xtce_version",
]
