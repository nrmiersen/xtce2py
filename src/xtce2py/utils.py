"""xtce2py utilities."""

import re

from . import config


def to_pascal_case(name: str) -> str:
    """Convert a string into a valid, PEP 8 compliant PascalCase class name.

    Handles separators, acronyms, and removes invalid characters.

    Args:
        name: The raw string name from the XTCE file.

    Returns:
        A sanitized PascalCase string.

    """
    settings = config.get_settings()

    name = name.replace("-", " ").replace("_", " ")
    name = name.title()
    name = re.sub(r"[^a-zA-Z0-9]", "", name)

    # Keep any known acronyms in all caps
    for acronym in settings.naming_convention.acronyms:
        name = name.replace(acronym.title(), acronym)

    return name


def sanitize_description(description: str) -> str:
    """Verify a description is formatted correctly.

    Args:
        description: The string description.

    Returns:
        A sanitized description string.

    """
    if description:
        stripped_description = description.rstrip()
        if stripped_description and not stripped_description.endswith("."):
            return stripped_description + "."

    return description


def get_field_name(name: str | None) -> str:
    """Convert a string into a valid, PEP 8 compliant field name.

    Handles separators, acronyms, and removes invalid characters.

    Args:
        name: The raw string name from the XTCE file.

    Returns:
        A sanitized field name string.

    """
    settings = config.get_settings()

    if not name:
        return "unknown"

    if settings.naming_convention.use_existing_names:
        # If the user wants to keep existing names, just sanitize invalid characters
        name = re.sub(r"[^a-zA-Z0-9_]", "", name)
        if name and name[0].isdigit():
            name = "_" + name
        return name.lower()

    name = name.replace("-", "_").replace(" ", "_")
    name = re.sub(r"[^a-zA-Z0-9_]", "", name)
    return name.lower()
