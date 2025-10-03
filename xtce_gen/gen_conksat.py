"""Generating test XTCEs."""

from pathlib import Path

from lxml import etree
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from xtce2py.xtce_1_1 import *
from xtce2py.xtce_1_1 import dtc_06_11_06

# Create parameter types
integer_parameter_type_set = []
for i in range(1, 33):
    integer_parameter_type_set.append(
        ParameterTypeSetType.IntegerParameterType(
            name=f"UInt{i}",
            unit_set=BaseDataType.UnitSet(),
            size_in_bits=i,
            signed=False,
        )
    )
for i in range(1, 33):
    integer_parameter_type_set.append(
        ParameterTypeSetType.IntegerParameterType(
            name=f"Int{i}",
            unit_set=BaseDataType.UnitSet(),
            size_in_bits=i,
            signed=True,
        )
    )

integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordLength_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["meter"])]),
        size_in_bits=16,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=1),
                    ByteOrderType.Byte(byte_significance=0),
                ],
            ),
        ),
    )
)

# Create parameters that reference each type
parameter_set = ParameterSetType()
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="PacketVersion",
        parameter_type_ref="UInt3",
        short_description="Packet Version Number (PVN)",
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="PacketType", parameter_type_ref="UInt1")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="SecondaryHeaderFlag", parameter_type_ref="UInt1")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ApplicationIdentifier", parameter_type_ref="UInt11"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="SequenceFlags", parameter_type_ref="UInt2")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="SequenceCount", parameter_type_ref="UInt14")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="PacketDataLength", parameter_type_ref="UInt16")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="ExtensionFlag", parameter_type_ref="UInt1")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="TimeCodeID", parameter_type_ref="UInt3")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="BasicTimeUnitOctets", parameter_type_ref="UInt2")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="FractionalTimeUnitOctets", parameter_type_ref="UInt2"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(name="TimestampSeconds", parameter_type_ref="UInt32")
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="TimestampFractionalSeconds", parameter_type_ref="UInt24"
    )
)

parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordLength", parameter_type_ref="ExtensionCordLength_Type"
    )
)

# Create a container set
container_set = ContainerSetType(
    sequence_container=[
        SequenceContainerType(
            name="SpacePacket",
            short_description="CCSDS Space Packet Primary Header",
            long_description="This is the top level packet container.",
            abstract=True,
            entry_list=EntryListType(
                parameter_ref_entry=[
                    ParameterRefEntryType(
                        parameter_ref="PacketVersion",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="PacketType",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="SecondaryHeaderFlag",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ApplicationIdentifier",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="SequenceFlags",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="SequenceCount",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="PacketDataLength",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionFlag",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="TimeCodeID",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="BasicTimeUnitOctets",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="FractionalTimeUnitOctets",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="TimestampSeconds",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="TimestampFractionalSeconds",
                    ),
                ]
            ),
        ),
        SequenceContainerType(
            name="EPS_HOUSEKEEPING",
            short_description="EPS Housekeeping Telemetry",
            long_description="This container holds housekeeping telemetry data for the EPS subsystem.",
            abstract=False,
            entry_list=EntryListType(
                parameter_ref_entry=[
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordLength",
                    ),
                ]
            ),
            base_container=SequenceContainerType.BaseContainer(
                container_ref="SpacePacket",
                restriction_criteria=SequenceContainerType.BaseContainer.RestrictionCriteria(
                    comparison=ComparisonType(
                        parameter_ref="ApplicationIdentifier",
                        comparison_operator=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
                        value="1",
                    )
                ),
            ),
        ),
    ]
)

# Create the SpaceSystem
space_system = SpaceSystem(
    name="ConkSat-1",
    short_description="ConkSat-1 XTCE Version 1.1",
    long_description="The first semi-functional ConkSat satellite, ConkSat-1, is a testbed for various technologies.",
    header=HeaderType(
        author_set=HeaderType.AuthorSet(
            author=[
                "John Conk",
                "Bill Sat",
            ]
        ),
        note_set=HeaderType.NoteSet(
            note=[
                "This is a test XTCE for ConkSat-1.",
                "It includes various parameters and commands for testing purposes.",
            ]
        ),
        history_set=HeaderType.HistorySet(
            history=[
                "RIP ConkSat-0, and the 17 interns it took with it.",
            ]
        ),
        version="1.0.0",
        date="2025-07-11T12:00:00Z",
        classification="NotClassified",
        validation_status=HeaderTypeValidationStatus.VALIDATED,
    ),
    telemetry_meta_data=TelemetryMetaDataType(
        parameter_type_set=ParameterTypeSetType(
            integer_parameter_type=integer_parameter_type_set
        ),
        parameter_set=parameter_set,
        container_set=container_set,
    ),
    service_set=SpaceSystem.ServiceSet(
        service=[
            ServiceType(
                name="ConkSatService",
                short_description="Service for ConkSat operations",
                long_description="This service handles various operations for the ConkSat satellite.",
                container_ref_set=ServiceType.ContainerRefSet(
                    container_ref=[
                        ContainerRefType(
                            container_ref="ConkSatTestContainer",
                        )
                    ]
                ),
            )
        ]
    ),
)

# Configure the serializer
config = SerializerConfig(pretty_print=True, pretty_print_indent="    ")
serializer = XmlSerializer(config=config)

# Serialize the object to a file
output_file = Path("./xtce_gen/xtces/CONKSAT_1_XTCE.xml")
with open(output_file, "w", encoding="utf-8") as f:
    serializer.write(f, space_system, ns_map={"xtce": dtc_06_11_06.__NAMESPACE__})

print(f"Successfully created XTCE: {output_file}")


# Validate the generated XTCE file
def validate_xtce_file(xml_file: Path, xsd_file: Path) -> tuple[bool, str]:
    """Validate an XML file against an XSD schema."""
    from lxml import etree

    try:
        with open(xsd_file, "rb") as f:
            schema_doc = etree.parse(f)
        xmlschema = etree.XMLSchema(schema_doc)

        with open(xml_file, "rb") as f:
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


# Validate against the XTCE 1.1 schema
xsd_file = Path("./src/xtce2py/xtce_1_1/dtc-06-11-06.xsd")
if xsd_file.exists():
    is_valid, error_msg = validate_xtce_file(output_file, xsd_file)
    if is_valid:
        print("XTCE validation passed")
    else:
        print(f"XTCE validation failed: {error_msg}")
else:
    print(f"Warning: XSD schema not found at {xsd_file}")
