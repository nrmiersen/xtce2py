from pathlib import Path
from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from xtce11 import SpaceSystem

config = ParserConfig(fail_on_unknown_properties=False)
parser = XmlParser(config=config)

xml = Path("/home/nrmiersen/xtce2py/resources/BogusSAT-1-Bad.xml")

try:
    space_system = parser.from_path(xml, SpaceSystem)

    for parameter in space_system.telemetry_meta_data.parameter_set.parameter:
        print(parameter, "\n")

except Exception as e:
    print(e)
