"""Parses an XTCE file."""

import xml.etree.ElementTree as ET
from pathlib import Path

from . import xtce11, xtce12, xtce13


def get_namespace(xml: Path) -> str | None:
    """Get the namespace from the XTCE XML file."""
    try:
        for event, elem in ET.iterparse(xml, events=("start",)):
            if "}" in elem.tag:
                return elem.tag.split("}")[0][1:]  # [1:] to remove the opening '{'
            else:
                return None
    except ET.ParseError:
        return None


def get_xtce_parser(
    xml: Path,
) -> xtce11.XtceParser | xtce12.XtceParser | xtce13.XtceParser:
    """Parse the XML file and return an XTCE parser."""
    namespace = get_namespace(xml)
    if namespace == xtce11.dtc_06_11_06.__NAMESPACE__:
        return xtce11.XtceParser(xml)
    elif namespace == xtce12.dtc_18_02_04.__NAMESPACE__:
        return xtce12.XtceParser(xml)
    elif namespace == xtce13.dtc_25_02_18.__NAMESPACE__:
        return xtce13.XtceParser(xml)
    else:
        raise ValueError(f"Unsupported XTCE namespace: {namespace}")
