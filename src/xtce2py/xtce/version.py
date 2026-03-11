"""XTCE version definitions and utilities."""

import importlib
import importlib.resources
from enum import Enum
from pathlib import Path

from lxml import etree


class XtceVersion(Enum):
    """Enumeration for supported XTCE standard versions."""

    V1_1 = (
        "1.1",
        "xtce_1_1",
        "xtce2py.xtce_1_1",
        "dtc-06-11-06.xsd",
    )
    V1_2 = (
        "1.2",
        "xtce_1_2",
        "xtce2py.xtce_1_2",
        "dtc-18-02-04.xsd",
    )
    V1_3 = (
        "1.3",
        "xtce_1_3",
        "xtce2py.xtce_1_3",
        "dtc-25-02-18.xsd",
    )

    def __str__(self) -> str:
        """Return the string representation when printing."""
        return self.value[0]

    @property
    def _module_name(self) -> str:
        """Get the short module name (e.g., 'xtce_1_2')."""
        return self.value[1]

    @property
    def namespace(self) -> str:
        """A convenient property to get the namespace URI (lazy-loaded)."""
        module = importlib.import_module(f"xtce2py.{self._module_name}.bindings")
        return module.NAMESPACE

    @property
    def xsd_package(self) -> str:
        """A convenient property to get the package containing the XSD file."""
        return self.value[2]

    @property
    def xsd_filename(self) -> str:
        """A convenient property to get the XSD filename."""
        return self.value[3]

    def get_xsd_bytes(self) -> bytes:
        """Get the XSD file content as bytes using importlib.resources."""
        files = importlib.resources.files(self.xsd_package)
        xsd_resource = files / self.xsd_filename
        return xsd_resource.read_bytes()

    @classmethod
    def from_namespace(cls, namespace: str) -> "XtceVersion":
        """Look up the enum member from a namespace string."""
        for member in cls:
            if member.namespace == namespace:
                return member
        raise NotImplementedError(f"Unsupported XTCE namespace: {namespace}")


def _get_namespace(xml: Path) -> str | None:
    """Efficiently gets the namespace of the root element from an XML file."""
    try:
        for event, element in etree.iterparse(str(xml), events=("start",)):
            if "}" in element.tag:
                return element.tag.split("}")[0][1:]
            else:
                return None
    except etree.XMLSyntaxError:
        return None


def get_xtce_version(xml: Path) -> XtceVersion:
    """Parse the XML file and return the corresponding XtceVersion enum member."""
    namespace = _get_namespace(xml)
    if not namespace:
        raise ValueError(f"Could not determine namespace for '{xml}'")

    return XtceVersion.from_namespace(namespace)
