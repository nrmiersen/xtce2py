"""Validation-related data structures and exceptions."""

import enum
from dataclasses import dataclass
from typing import List


class ValidationSeverity(enum.Enum):
    """Enumeration for the severity of a validation issue."""

    ERROR = "ERROR"
    WARNING = "WARNING"


@dataclass
class ValidationResult:
    """A structured container for a single validation finding."""

    severity: ValidationSeverity
    message: str
    location: str


class XtceSemanticValidationError(Exception):
    """Custom exception raised when fatal semantic errors are found."""

    def __init__(self, errors: List[ValidationResult]):
        """Initialize with a list of validation errors."""
        self.errors = errors
        error_list = "\n".join(f"  - [in {e.location}]: {e.message}" for e in errors)
        super().__init__(f"XTCE file has semantic validation errors:\n{error_list}")
