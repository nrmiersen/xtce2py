"""xtce2py utilities."""

import keyword
import re
from typing import Optional

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


def sanitize_description(description: str | None) -> Optional[str]:
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


def sanitize_class_name(name: str, is_abstract: bool = False) -> str:
    """Sanitize a string to be a valid Python class name."""
    clean = name.replace(" ", "").replace("-", "_")
    base = clean[0].upper() + clean[1:]
    return f"_{base}" if is_abstract else base


def path_to_package(xtce_path: str) -> str:
    """Convert an XTCE path to a Python package name.

    Args:
        xtce_path: The XTCE path string (e.g., /A/B/C).

    Returns:
        A Python package name derived from the path (e.g., a.b).

    """
    parts = xtce_path.strip("/").split("/")[:-1]
    clean_parts = [p.lower().replace("-", "_").replace(" ", "_") for p in parts]

    return ".".join(clean_parts)


def format_identifier(name: str | None, override_style: str | None = None) -> str:
    """Convert a string into a valid Python identifier, preserving acronyms.

    Args:
        name: The raw string name from the XTCE file.
        override_style: Force a specific style, ignoring the global config.

    Returns:
        A sanitized, syntax-compliant string.

    """
    if not name:
        return "unknown"

    # 1. Get user preferences
    settings = config.get_settings()
    style = (override_style or settings.naming_convention.style).lower()
    acronyms = settings.naming_convention.acronyms

    # 2. Clean invalid chars to underscores
    clean_name = name.replace("-", "_").replace(" ", "_")
    clean_name = re.sub(r"[^a-zA-Z0-9_]", "_", clean_name)

    if style != "keep":
        # 3. Smartly split the string into parts (handles PascalCase and camelCase)
        # e.g., "ParseCCSDSHeader" -> "Parse_CCSDS_Header"
        clean_name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", clean_name)
        clean_name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", clean_name)

        parts = [p for p in clean_name.split("_") if p]

        # Helper to check if a part is in the acronym list (case-insensitive check)
        def get_acronym(part: str) -> str | None:
            for acr in acronyms:
                if part.lower() == acr.lower():
                    return acr  # Return the exact configured casing (e.g., "CCSDS")
            return None

        formatted_parts = []
        for i, part in enumerate(parts):
            acr = get_acronym(part)
            if acr:
                # If it's an acronym, append it EXACTLY as configured
                formatted_parts.append(acr)
            else:
                # Otherwise, apply standard casing
                if style == "snake":
                    formatted_parts.append(part.lower())
                elif style == "pascal":
                    formatted_parts.append(part.capitalize())
                elif style == "camel":
                    if i == 0:
                        formatted_parts.append(part.lower())
                    else:
                        formatted_parts.append(part.capitalize())

        # 4. Rejoin the parts based on the style
        if style == "snake":
            clean_name = "_".join(formatted_parts)
        else:
            clean_name = "".join(formatted_parts)

    # 5. Final Python Syntax Enforcement
    clean_name = clean_name.strip("_")

    # Cannot start with a number
    if clean_name and clean_name[0].isdigit():
        clean_name = f"_{clean_name}"

    # Cannot be a Python reserved keyword
    if keyword.iskeyword(clean_name):
        clean_name = f"{clean_name}_"

    return clean_name or "unknown"
