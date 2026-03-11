"""Base XTCE Validator."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Literal


@dataclass
class XtceValidationError:
    """Container for a single semantic validation error."""

    location: str
    message: str
    severity: Literal["WARNING", "ERROR"] = "ERROR"


class BaseXtceValidator(ABC):
    """Abstract base XTCE semantic validator."""

    @abstractmethod
    def validate(self) -> tuple[bool, list[XtceValidationError]]:
        """Run all semantic validation.

        Returns:
            tuple[bool, list[XtceValidationError]]: A tuple containing a boolean indicating if the data is valid and a list of validation errors if not.

        """
        pass
