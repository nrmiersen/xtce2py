"""XTCE version 1.2 parser module."""

from pathlib import Path

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from . import *


class XtceParser:
    """Parser for XTCE version 1.2 files."""

    def __init__(self, xml: Path):
        """Initialize the parser with default configuration."""
        self.space_system = self.parse_xtce(xml)

    def parse_xtce(self, xml: Path) -> SpaceSystem:
        """Parse the XTCE file and returns a SpaceSystem object."""
        config = ParserConfig(fail_on_unknown_properties=False)
        parser = XmlParser(config=config)
        return parser.from_path(xml, SpaceSystem)

    def get_metadata(self) -> dict:
        """Extract metadata from the SpaceSystem object."""
        return {"name": self.space_system.name}
