"""Parses an XTCE file."""

import re
from typing import Optional, TypeVar

T = TypeVar("T")


def unwrap(value: Optional[T]) -> T:
    """Return the value if it is not None, otherwise raises a ValueError.

    This is for fields that are defined as Optional in the xsdata bindings but are strictly required by the XTCE XSD. Because XSD validation is performed prior to any XTCE parsing, it is effectively impossible for these fields to be None at runtime, so this function allows us to treat them as non-optional in the code while still satisfying the type checker.

    Args:
        value: The value to check.

    Returns:
        The unwrapped value if it is not None.

    """
    if value is None:
        raise ValueError("Unexpected None for required XTCE field")

    return value


def sanitize_enum_label(label: str) -> Optional[str]:
    """Sanitize an enumeration label to be a valid Python identifier.

    This function replaces invalid characters with underscores and ensures the label does not start with a digit.

    Args:
        label: The original enumeration label from the XTCE file.

    Returns:
        A sanitized string that can be used as a Python identifier.

    """
    # Replace non-alphanumeric chars with underscores and make uppercase
    clean = re.sub(r"\W+", "_", label).strip("_").upper()

    # Python variables cannot start with a number
    if clean and clean[0].isdigit():
        clean = f"VAL_{clean}"

    return clean
