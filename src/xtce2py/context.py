"""Context models for Jinja2 templates."""

from dataclasses import dataclass

from xtce2py.xtce.context import (
    XtceMetadataContext,
)


@dataclass
class PackageContext:
    """Container for the data needed by the package template."""

    package_version: str
    package_name: str


@dataclass
class ReadMeContext:
    """Container for the data needed by the README.md template."""

    dist_name: str
    package_name: str
    xtce_version: str
    metadata: XtceMetadataContext


@dataclass
class PyprojectContext:
    """Container for the data needed by the pyproject.toml template."""

    dist_name: str
    package_name: str
    version: str
    metadata: XtceMetadataContext
