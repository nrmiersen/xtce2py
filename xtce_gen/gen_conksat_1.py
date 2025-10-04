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
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["m"])]),
        size_in_bits=16,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=16,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordWidth_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["cm"])]),
        size_in_bits=16,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp1_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=16,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp2_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp3_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.ONES_COMPLIMENT,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp4_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.ONES_COMPLIMENT,
            size_in_bits=16,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp5_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.TWOS_COMPLIMENT,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp6_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.TWOS_COMPLIMENT,
            size_in_bits=16,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp7_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=13,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.TWOS_COMPLIMENT,
            size_in_bits=13,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp8_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=19,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.ONES_COMPLIMENT,
            size_in_bits=19,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp9_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=32,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.UNSIGNED,
            size_in_bits=32,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=3),
                    ByteOrderType.Byte(byte_significance=2),
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp10_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=32,
        signed=True,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.ONES_COMPLIMENT,
            size_in_bits=32,
            byte_order_list=ByteOrderType(
                byte=[
                    ByteOrderType.Byte(byte_significance=0),
                    ByteOrderType.Byte(byte_significance=2),
                    ByteOrderType.Byte(byte_significance=3),
                    ByteOrderType.Byte(byte_significance=1),
                ],
            ),
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp11_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=12,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.PACKED_BCD,
            size_in_bits=12,
        ),
    )
)
integer_parameter_type_set.append(
    ParameterTypeSetType.IntegerParameterType(
        name="ExtensionCordTemp12_Type",
        unit_set=BaseDataType.UnitSet(unit=[UnitType(content=["degC"])]),
        size_in_bits=16,
        signed=False,
        integer_data_encoding=IntegerDataEncodingType(
            bit_order=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
            encoding=IntegerDataEncodingTypeEncoding.BCD,
            size_in_bits=16,
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
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordWidth", parameter_type_ref="ExtensionCordWidth_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp1", parameter_type_ref="ExtensionCordTemp1_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp2", parameter_type_ref="ExtensionCordTemp2_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp3", parameter_type_ref="ExtensionCordTemp3_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp4", parameter_type_ref="ExtensionCordTemp4_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp5", parameter_type_ref="ExtensionCordTemp5_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp6", parameter_type_ref="ExtensionCordTemp6_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp7", parameter_type_ref="ExtensionCordTemp7_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp8", parameter_type_ref="ExtensionCordTemp8_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp9", parameter_type_ref="ExtensionCordTemp9_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp10", parameter_type_ref="ExtensionCordTemp10_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp11", parameter_type_ref="ExtensionCordTemp11_Type"
    )
)
parameter_set.parameter.append(
    ParameterSetType.Parameter(
        name="ExtensionCordTemp12", parameter_type_ref="ExtensionCordTemp12_Type"
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
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordWidth",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp1",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp2",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp3",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp4",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp5",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp6",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp7",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp8",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp9",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp10",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp11",
                    ),
                    ParameterRefEntryType(
                        parameter_ref="ExtensionCordTemp12",
                    ),
                ]
            ),
            base_container=SequenceContainerType.BaseContainer(
                container_ref="SpacePacket",
                restriction_criteria=SequenceContainerType.BaseContainer.RestrictionCriteria(
                    comparison_list=MatchCriteriaType.ComparisonList(
                        comparison=[
                            ComparisonType(
                                parameter_ref="PacketVersion",
                                comparison_operator=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
                                value="0",
                            ),
                            ComparisonType(
                                parameter_ref="ApplicationIdentifier",
                                comparison_operator=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
                                value="1",
                            ),
                        ]
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
output_file = Path("./xtce_gen/xtces/CONKSAT-1-XTCE.xml")
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
