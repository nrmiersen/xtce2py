"""XTCE validation utilities."""

import importlib.resources
import tempfile
from pathlib import Path

from lxml import etree

from xtce2py.xtce.parser import BaseXtceParser
from xtce2py.xtce.version import XtceVersion, get_xtce_version


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
        # Get the XTCE version to access the package
        version = get_xtce_version(xml)

        # Write XSD files to a temporary directory for proper resolution
        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)

            # Write main XSD
            main_xsd_path = tmpdir_path / version.xsd_filename
            main_xsd_path.write_bytes(xsd_bytes)

            # Write xml.xsd dependency
            files = importlib.resources.files(version.xsd_package)
            xml_xsd_resource = files / "xml.xsd"
            xml_xsd_path = tmpdir_path / "xml.xsd"
            xml_xsd_path.write_bytes(xml_xsd_resource.read_bytes())

            # Parse XSD with file-based resolution
            schema_doc = etree.parse(str(main_xsd_path))
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


def get_xtce_parser(xml: Path) -> BaseXtceParser | None:
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
        # from xtce2py.xtce_1_1 import XtceParser

        # return XtceParser(xml)
        raise NotImplementedError("XTCE 1.1 support is not implemented yet.")

    elif version == XtceVersion.V1_2:
        from xtce2py.xtce_1_2 import XtceParser

        return XtceParser(xml)

    elif version == XtceVersion.V1_3:
        # from xtce2py.xtce_1_3 import XtceParser

        # return XtceParser(xml)
        raise NotImplementedError("XTCE 1.3 support is not implemented yet.")
