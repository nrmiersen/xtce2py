"""Testing."""

from pathlib import Path
from typing import Optional

from xtce2py.xtce_1_1.parser import XtceParser


def parser_test():
    """Test package."""
    parser = XtceParser(Path("tests/xtces/CONKSAT_XTCE.xml"))
    parser.generate_parser_context()


if __name__ == "__main__":
    parser_test()
