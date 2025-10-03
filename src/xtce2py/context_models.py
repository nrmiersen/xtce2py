"""Context models for Jinja2 templates."""

from dataclasses import dataclass, field
from typing import Any, Optional

from xtce2py.xtce_common.context_models import ContainerDetailsContext


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
class PyprojectContext:
    """Container for the data needed by the pyproject.toml template."""

    dist_name: str
    package_name: str
    version: str
    metadata: XtceMetadataContext


@dataclass
class ReadMeContext:
    """Container for the data needed by the README.md template."""

    dist_name: str
    package_name: str
    xtce_version: str
    metadata: XtceMetadataContext


@dataclass
class InitContext:
    """Container for the data needed by the __init__.py template."""

    metadata: XtceMetadataContext


@dataclass
class ModelContext:
    """Container for the data needed by a model within the models.py template."""

    name: str
    parent: str = "PacketBase"
    entries: list[dict[str, Any]] = field(default_factory=list)
    description: Optional[str] = ""


@dataclass
class ModelsContext:
    """Container for the data needed by the models.py template."""

    imports: dict[str, list[str]] = field(default_factory=dict)
    containers: list[ModelContext] = field(default_factory=list)


@dataclass
class ParserContext:
    """Container for the data needed by the parser template."""

    container_tree: dict[str, Any] = field(default_factory=dict)
    concrete_container_names: set[str] = field(default_factory=set)
    container_details_map: dict[str, ContainerDetailsContext] = field(
        default_factory=dict
    )
