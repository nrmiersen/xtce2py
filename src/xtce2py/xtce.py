"""Parses an XTCE file."""

import importlib.resources
import io
from enum import Enum
from pathlib import Path

from lxml import etree

from xtce2py import xtce_1_1, xtce_1_2, xtce_1_3


class XtceVersion(Enum):
    """Enumeration for supported XTCE standard versions."""

    V1_1 = (
        "1.1",
        xtce_1_1.dtc_06_11_06.__NAMESPACE__,
        "xtce2py.xtce_1_1",
        "dtc-06-11-06.xsd",
    )
    V1_2 = (
        "1.2",
        xtce_1_2.dtc_18_02_04.__NAMESPACE__,
        "xtce2py.xtce_1_2",
        "dtc-18-02-04.xsd",
    )
    V1_3 = (
        "1.3",
        xtce_1_3.dtc_25_02_18.__NAMESPACE__,
        "xtce2py.xtce_1_3",
        "dtc-25-02-18.xsd",
    )

    def __str__(self) -> str:
        """Return the string representation when printing."""
        return self.value[0]

    @property
    def namespace(self) -> str:
        """A convenient property to get the namespace URI."""
        return self.value[1]

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
        raise ValueError(f"Unsupported XTCE namespace: {namespace}")


def get_namespace(xml: Path) -> str | None:
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
    namespace = get_namespace(xml)
    if not namespace:
        raise ValueError(f"Could not determine namespace for '{xml}'")
    return XtceVersion.from_namespace(namespace)


def validate_xtce_file(xml: Path, xsd_bytes: bytes) -> tuple[bool, str]:
    """Validate an XML file against an XSD schema using lxml.

    Args:
        xml: The path to the XTCE (.xml) file to validate.
        xsd_bytes: The XSD schema content as bytes.

    Returns:
        A tuple containing:
        - A boolean indicating if the validation was successful.
        - A string containing error messages, or an empty string on success.

    """
    try:
        schema_doc = etree.parse(io.BytesIO(xsd_bytes))
        xmlschema = etree.XMLSchema(schema_doc)

        with open(xml, "rb") as f:
            xml_doc = etree.parse(f)

        is_valid = xmlschema.validate(xml_doc)

        if is_valid:
            return True, ""
        else:
            error_log = str(xmlschema.error_log)
            return False, error_log

    except etree.XMLSchemaParseError as e:
        return False, f"XSD Schema Error: {e}"
    except etree.XMLSyntaxError as e:
        return False, f"XML Syntax Error: {e}"


def get_xtce_parser(
    xml: Path,
) -> xtce_1_1.XtceParser | None:  # | xtce_1_2.XtceParser | xtce_1_3.XtceParser :
    """Determine the XTCE version, validates the file, and returns the appropriate parser instance."""
    # Determine the version
    version = get_xtce_version(xml)

    # Validate the file against that version's schema
    xsd_bytes = version.get_xsd_bytes()
    is_valid, errors = validate_xtce_file(xml, xsd_bytes)
    if not is_valid:
        raise ValueError(f"XTCE file '{xml}' failed validation:\n{errors}")

    # If valid, return the correct parser instance
    if version == XtceVersion.V1_1:
        return xtce_1_1.XtceParser(xml)
    # elif version == XtceVersion.V1_2:
    #     return xtce_1_2.XtceParser(xml)
    # elif version == XtceVersion.V1_3:
    #     return xtce_1_3.XtceParser(xml)
