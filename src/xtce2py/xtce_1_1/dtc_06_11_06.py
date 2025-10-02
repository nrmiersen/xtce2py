from dataclasses import dataclass, field
from decimal import Decimal
from enum import Enum
from typing import Optional, Union

from xsdata.models.datatype import XmlDate, XmlDateTime, XmlDuration

__NAMESPACE__ = "http://www.omg.org/space/xtce"


class AlarmLevels(Enum):
    """
    An enumerated list of the possible alarm levels.
    """

    NORMAL = "normal"
    WATCH = "watch"
    WARNING = "warning"
    DISTRESS = "distress"
    CRITICAL = "critical"
    SEVERE = "severe"


@dataclass
class AliasSetType:
    """
    Contains an unordered collection of Alias's.

    :ivar alias: Used to contain an alias (alternate) name or ID for the
        object.   For example, a parameter may have a mnemonic, an on-
        board id, and special IDs used by various ground software
        applications; all of these are alias's.  Some ground system
        processing equipment has some severe naming restrictions on
        parameters (e.g., names must less then 12 characters, single
        case or integral id's only); their alias's provide a means of
        capturing each name in a "nameSpace".
    """

    alias: list["AliasSetType.Alias"] = field(
        default_factory=list,
        metadata={
            "name": "Alias",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 1,
        },
    )

    @dataclass
    class Alias:
        name_space: Optional[str] = field(
            default=None,
            metadata={
                "name": "nameSpace",
                "type": "Attribute",
                "required": True,
            },
        )
        alias: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass
class ByteOrderType:
    """An ordered list of bytes where the order of the bytes is in stream
    order.

    Each byte has an attribute giving its significance.
    """

    byte: list["ByteOrderType.Byte"] = field(
        default_factory=list,
        metadata={
            "name": "Byte",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
        },
    )

    @dataclass
    class Byte:
        byte_significance: Optional[int] = field(
            default=None,
            metadata={
                "name": "byteSignificance",
                "type": "Attribute",
                "required": True,
            },
        )


class CrcReference(Enum):
    START = "start"
    END = "end"


class ChangeAlarmRangesChangeBasis(Enum):
    ABSOLUTE_CHANGE = "absoluteChange"
    PERCENTAGE_CHANGE = "percentageChange"


class ChangeAlarmRangesChangeType(Enum):
    CHANGE_PER_SECOND = "changePerSecond"
    CHANGE_PER_SAMPLE = "changePerSample"


class CheckWindowTimeWindowIsRelativeTo(Enum):
    COMMAND_RELEASE = "commandRelease"
    TIME_LAST_VERIFIER_PASSED = "timeLastVerifierPassed"


class ComparisonOperatorsType(Enum):
    """
    Operators to use when testing a boolean condition for a validity check.
    """

    EQUALS_SIGN_EQUALS_SIGN = "=="
    EXCLAMATION_MARK_EQUALS_SIGN = "!="
    LESS_THAN_SIGN = "<"
    LESS_THAN_SIGN_EQUALS_SIGN = "<="
    GREATER_THAN_SIGN = ">"
    GREATER_THAN_SIGN_EQUALS_SIGN = ">="


@dataclass
class ContainerRefType:
    """
    Holds a reference to a container.

    :ivar container_ref: name of container
    """

    container_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "required": True,
        },
    )


class DataEncodingTypeBitOrder(Enum):
    LEAST_SIGNIFICANT_BIT_FIRST = "leastSignificantBitFirst"
    MOST_SIGNIFICANT_BIT_FIRST = "mostSignificantBitFirst"


class EpochTypeValue(Enum):
    TAI = "TAI"


class FlagFlagBitType(Enum):
    ZEROS = "zeros"
    ONES = "ones"


class FloatDataEncodingTypeEncoding(Enum):
    IEEE754_1985 = "IEEE754_1985"
    MILSTD_1750_A = "MILSTD_1750A"


class FloatDataEncodingTypeSizeInBits(Enum):
    VALUE_32 = 32
    VALUE_64 = 64
    VALUE_128 = 128


class FloatDataTypeSizeInBits(Enum):
    VALUE_32 = 32
    VALUE_64 = 64
    VALUE_128 = 128


@dataclass
class FloatRangeType:
    """A range of numbers.

    "minInclusive", "minExclusive", "maxInclusive" and "maxExclusive"
    attributes are borrowed from the W3C schema language.
    """

    min_inclusive: Optional[float] = field(
        default=None,
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
        },
    )
    min_exclusive: Optional[float] = field(
        default=None,
        metadata={
            "name": "minExclusive",
            "type": "Attribute",
        },
    )
    max_inclusive: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
        },
    )
    max_exclusive: Optional[float] = field(
        default=None,
        metadata={
            "name": "maxExclusive",
            "type": "Attribute",
        },
    )


class HeaderTypeValidationStatus(Enum):
    UNKNOWN = "Unknown"
    WORKING = "Working"
    DRAFT = "Draft"
    TEST = "Test"
    VALIDATED = "Validated"
    RELEASED = "Released"
    WITHDRAWN = "Withdrawn"


class IntegerDataEncodingTypeEncoding(Enum):
    UNSIGNED = "unsigned"
    SIGN_MAGNITUDE = "signMagnitude"
    TWOS_COMPLIMENT = "twosCompliment"
    ONES_COMPLIMENT = "onesCompliment"
    BCD = "BCD"
    PACKED_BCD = "packedBCD"


@dataclass
class IntegerRangeType:
    """An integral range of numbers.

    "min", and "max".
    """

    min_inclusive: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "name": "minInclusive",
            "type": "Attribute",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )
    max_inclusive: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "name": "maxInclusive",
            "type": "Attribute",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )


class LocationInContainerInBitsReferenceLocation(Enum):
    CONTAINER_START = "containerStart"
    CONTAINER_END = "containerEnd"
    PREVIOUS_ENTRY = "previousEntry"
    NEXT_ENTRY = "nextEntry"


class MathOperatorsType(Enum):
    """
    Mathematical operators.
    """

    PLUS_SIGN = "+"
    HYPHEN_MINUS = "-"
    ASTERISK = "*"
    SOLIDUS = "/"
    PERCENT_SIGN = "%"
    CIRCUMFLEX_ACCENT = "^"
    Y_X = "y^x"
    LN = "ln"
    LOG = "log"
    E_X = "e^x"
    VALUE_1_X = "1/x"
    X = "x!"
    TAN = "tan"
    COS = "cos"
    SIN = "sin"
    ATAN = "atan"
    ACOS = "acos"
    ASIN = "asin"
    TANH = "tanh"
    COSH = "cosh"
    SINH = "sinh"
    ATANH = "atanh"
    ACOSH = "acosh"
    ASINH = "asinh"
    SWAP = "swap"


@dataclass
class MessageRefType:
    """
    Holds a reference to a message.

    :ivar message_ref: name of message
    """

    message_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "messageRef",
            "type": "Attribute",
            "required": True,
        },
    )


class NumberFormatNotation(Enum):
    NORMAL = "normal"
    SCIENTIFIC = "scientific"
    ENGINEERING = "engineering"


class PcmstreamTypePcmType(Enum):
    NRZL = "NRZL"
    NRZM = "NRZM"
    NRZS = "NRZS"
    BI_PHASE_L = "BiPhaseL"
    BI_PHASE_M = "BiPhaseM"
    BI_PHASE_S = "BiPhaseS"


class ParameterPropertiesTypeDataSource(Enum):
    TELEMETERED = "telemetered"
    DERIVED = "derived"
    CONSTANT = "constant"
    LOCAL = "local"


@dataclass
class ParameterRefType:
    """A reference to a Parameter.

    Uses Unix ‘like’ naming across the SpaceSystem Tree (e.g.,
    SimpleSat/Bus/EPDS/BatteryOne/Voltage).  To reference an individual
    member of an array use the zero based bracket notation commonly used
    in languages like C, C++, and Java.
    """

    parameter_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
        },
    )


class ParityReference(Enum):
    START = "start"
    END = "end"


class ParityType(Enum):
    EVEN = "Even"
    ODD = "Odd"


@dataclass
class PhysicalAddressType:
    """
    When it's important to know the physical address(s) on the spacecraft
    that this parameter may be collected from, use this.
    """

    sub_address: Optional["PhysicalAddressType"] = field(
        default=None,
        metadata={
            "name": "SubAddress",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    source_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "sourceName",
            "type": "Attribute",
        },
    )
    source_address: Optional[str] = field(
        default=None,
        metadata={
            "name": "sourceAddress",
            "type": "Attribute",
        },
    )


@dataclass
class PolynomialType:
    """A polynomial expression.

    For example: 3 + 2x

    :ivar term: A term in a polynomial expression.
    """

    term: list["PolynomialType.Term"] = field(
        default_factory=list,
        metadata={
            "name": "Term",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 1,
        },
    )

    @dataclass
    class Term:
        coefficient: Optional[float] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )
        exponent: Optional[float] = field(
            default=None,
            metadata={
                "type": "Attribute",
                "required": True,
            },
        )


class RadixType(Enum):
    """
    Specifies the number base.
    """

    DECIMAL = "Decimal"
    HEXADECIMAL = "Hexadecimal"
    OCTAL = "Octal"
    BINARY = "Binary"


class RateInStreamTypeBasis(Enum):
    PER_SECOND = "perSecond"
    PER_CONTAINER_UPDATE = "perContainerUpdate"


@dataclass
class ServiceRefType:
    """
    A reference to a Service.
    """

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    service_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "serviceRef",
            "type": "Attribute",
            "required": True,
        },
    )


class SignificanceTypeConsequenceLevel(Enum):
    NONE = "none"
    WATCH = "watch"
    WARNING = "warning"
    DISTRESS = "distress"
    CRITICAL = "critical"
    SEVERE = "severe"


@dataclass
class SplinePointType:
    """
    A spline is a set on points from which a curve may be drawn to
    interpolate raw to calibrated values.
    """

    order: int = field(
        default=1,
        metadata={
            "type": "Attribute",
        },
    )
    raw: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    calibrated: Optional[float] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StreamRefType:
    """
    Holds a reference to a stream.

    :ivar stream_ref: name of reference stream
    """

    stream_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "required": True,
        },
    )


class StringDataEncodingTypeEncoding(Enum):
    UTF_8 = "UTF-8"
    UTF_16 = "UTF-16"


class StringDataTypeCharacterWidth(Enum):
    VALUE_8 = 8
    VALUE_16 = 16


class TimeUnits(Enum):
    """Base time units.

    days, months, years have obvoius ambiguity and should be avoided
    """

    SECONDS = "seconds"
    PICO_SECONDS = "picoSeconds"
    DAYS = "days"
    MONTHS = "months"
    YEARS = "years"


@dataclass
class TriggerSetType:
    """A trigger is used to initiate the processing of some algorithm.

    A trigger may be based on an update of a Parameter or on a time
    basis.  Triggers may also have a rate that limits their firing to a
    1/rate basis.

    :ivar on_parameter_update_trigger: Names a parameter that upon
        change will start the execution of the algorithm.  Holds a
        parameter reference name for a parameter that when it changes,
        will cause this algorithm to be executed.
    :ivar on_container_update_trigger:
    :ivar on_periodic_rate_trigger:
    :ivar name:
    :ivar trigger_rate:
    """

    on_parameter_update_trigger: list["TriggerSetType.OnParameterUpdateTrigger"] = (
        field(
            default_factory=list,
            metadata={
                "name": "OnParameterUpdateTrigger",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    on_container_update_trigger: list["TriggerSetType.OnContainerUpdateTrigger"] = (
        field(
            default_factory=list,
            metadata={
                "name": "OnContainerUpdateTrigger",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    on_periodic_rate_trigger: list["TriggerSetType.OnPeriodicRateTrigger"] = field(
        default_factory=list,
        metadata={
            "name": "OnPeriodicRateTrigger",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    trigger_rate: int = field(
        default=1,
        metadata={
            "name": "triggerRate",
            "type": "Attribute",
        },
    )

    @dataclass
    class OnParameterUpdateTrigger:
        parameter_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "parameterRef",
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class OnContainerUpdateTrigger:
        container_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "containerRef",
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class OnPeriodicRateTrigger:
        fire_rate_in_seconds: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "fireRateInSeconds",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass
class UnitType:
    """
    Used to hold the unit(s) plus possibly the exponent and factor for the
    units.
    """

    power: Decimal = field(
        default=Decimal("1"),
        metadata={
            "type": "Attribute",
        },
    )
    factor: str = field(
        default="1",
        metadata={
            "type": "Attribute",
        },
    )
    description: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    content: list[object] = field(
        default_factory=list,
        metadata={
            "type": "Wildcard",
            "namespace": "##any",
            "mixed": True,
        },
    )


@dataclass
class ValueEnumerationType:
    """
    Contains a value and an associated string label.
    """

    value: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )
    label: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


class VerifierEnumerationType(Enum):
    """
    An enumerated list of verifier types.
    """

    RELEASE = "release"
    TRANSFERRED_TO_RANGE = "transferredToRange"
    SENT_FROM_RANGE = "sentFromRange"
    RECEIVED = "received"
    ACCEPTED = "accepted"
    QUEUED = "queued"
    EXECUTING = "executing"
    COMPLETE = "complete"
    FAILED = "failed"


@dataclass
class AlarmRangesType:
    """Contains five ranges: Watch, Warning, Distress, Critical, and Severe each in increasing severity.  Normally, only the Warning and Critical ranges are used and the color yellow is associated with Warning and the color red is associated with Critical.   The ranges given are valid for numbers lower than the min and higher than the max values.   These ranges should not overlap, but if they do, assume the most severe range is to be applied.  All ranges are optional and it is quite allowed for there to be only one end of the range.  Range values are in calibrated engineering units."""

    watch_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "WatchRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    warning_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "WarningRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    distress_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "DistressRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    critical_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "CriticalRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    severe_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "SevereRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class DescriptionType:
    """An abstract type definition used as the base for NameDescriptionType
    or OptionalNameDescriptionType.

    The short description is intended to be used for quick "memory
    jogger" descriptions of the object.

    :ivar long_description: The Long Description is intended to be used
        for explanatory descriptions of the object and may include HTML
        markup.  Long Descriptions are of unbounded length
    :ivar alias_set:
    :ivar ancillary_data_set:
    :ivar short_description: It is strongly recommended that the short
        description be kept under 80 characters in length
    """

    long_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "LongDescription",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    alias_set: Optional[AliasSetType] = field(
        default=None,
        metadata={
            "name": "AliasSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    ancillary_data_set: Optional["DescriptionType.AncillaryDataSet"] = field(
        default=None,
        metadata={
            "name": "AncillaryDataSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    short_description: Optional[str] = field(
        default=None,
        metadata={
            "name": "shortDescription",
            "type": "Attribute",
        },
    )

    @dataclass
    class AncillaryDataSet:
        """
        :ivar ancillary_data: Use for any other data associated with
            each named object.  May be used to include administrative
            data (e.g., version, CM or tags) or potentially any MIME
            type.  Data may be included  or given as an href.
        """

        ancillary_data: list["DescriptionType.AncillaryDataSet.AncillaryData"] = field(
            default_factory=list,
            metadata={
                "name": "AncillaryData",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class AncillaryData:
            value: str = field(
                default="",
                metadata={
                    "required": True,
                },
            )
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )
            mime_type: str = field(
                default="text/plain",
                metadata={
                    "name": "mimeType",
                    "type": "Attribute",
                },
            )
            href: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass
class ErrorDetectCorrectType:
    """
    A simple element that provides for simple, but common error checking and
    detection.

    :ivar parity: Bit position starts with 'zero'.
    :ivar crc: Cyclic Redundancy Check (CRC) definition. Legal values
        for coefficient's are 0 or 1. Exponents must be integer values.
    """

    parity: Optional["ErrorDetectCorrectType.Parity"] = field(
        default=None,
        metadata={
            "name": "Parity",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    crc: Optional["ErrorDetectCorrectType.Crc"] = field(
        default=None,
        metadata={
            "name": "CRC",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class Parity:
        type_value: Optional[ParityType] = field(
            default=None,
            metadata={
                "name": "type",
                "type": "Attribute",
                "required": True,
            },
        )
        bits_from_reference: Optional[int] = field(
            default=None,
            metadata={
                "name": "bitsFromReference",
                "type": "Attribute",
                "required": True,
            },
        )
        reference: ParityReference = field(
            default=ParityReference.START,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class Crc:
        polynomial: Optional[PolynomialType] = field(
            default=None,
            metadata={
                "name": "Polynomial",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        bits_from_reference: Optional[int] = field(
            default=None,
            metadata={
                "name": "bitsFromReference",
                "type": "Attribute",
            },
        )
        reference: CrcReference = field(
            default=CrcReference.START,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass
class HeaderType:
    """Schema for a Header record.

    A header contains general information about the system or subsystem.
    """

    author_set: Optional["HeaderType.AuthorSet"] = field(
        default=None,
        metadata={
            "name": "AuthorSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    note_set: Optional["HeaderType.NoteSet"] = field(
        default=None,
        metadata={
            "name": "NoteSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    history_set: Optional["HeaderType.HistorySet"] = field(
        default=None,
        metadata={
            "name": "HistorySet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    version: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    date: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    classification: str = field(
        default="NotClassified",
        metadata={
            "type": "Attribute",
        },
    )
    classification_instructions: Optional[str] = field(
        default=None,
        metadata={
            "name": "classificationInstructions",
            "type": "Attribute",
        },
    )
    validation_status: Optional[HeaderTypeValidationStatus] = field(
        default=None,
        metadata={
            "name": "validationStatus",
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class AuthorSet:
        author: list[str] = field(
            default_factory=list,
            metadata={
                "name": "Author",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

    @dataclass
    class NoteSet:
        note: list[str] = field(
            default_factory=list,
            metadata={
                "name": "Note",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

    @dataclass
    class HistorySet:
        history: list[str] = field(
            default_factory=list,
            metadata={
                "name": "History",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )


@dataclass
class ParameterInstanceRefType(ParameterRefType):
    """A reference to an instance of a Parameter.

    Used when the value of a parameter is required for a calculation or
    as an index value.  A positive value for instance is forward in
    time, a negative value for count is backward in time, a 0 value for
    count means use the current value of the parameter or the first
    value in a container.
    """

    instance: int = field(
        default=0,
        metadata={
            "type": "Attribute",
        },
    )
    use_calibrated_value: bool = field(
        default=True,
        metadata={
            "name": "useCalibratedValue",
            "type": "Attribute",
        },
    )


@dataclass
class RateInStreamType:
    """
    Used in packaging to define the expected rate that any individual
    container will be in a Stream.
    """

    basis: RateInStreamTypeBasis = field(
        default=RateInStreamTypeBasis.PER_SECOND,
        metadata={
            "type": "Attribute",
        },
    )
    minimum_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "minimumValue",
            "type": "Attribute",
        },
    )
    maximum_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "maximumValue",
            "type": "Attribute",
        },
    )


@dataclass
class SignificanceType:
    """
    Significance provides some cautionary information about the potential
    consequence of each MetaCommand.

    :ivar space_system_at_risk: If none is supplied, then the current
        SpaceSystem is assumed to be the one at risk by the issuance of
        this command
    :ivar reason_for_warning:
    :ivar consequence_level: No specific meanings have been assigned to
        these different levels, but they mirror the Alarm levels of
        Telemetry.
    """

    space_system_at_risk: Optional[str] = field(
        default=None,
        metadata={
            "name": "spaceSystemAtRisk",
            "type": "Attribute",
        },
    )
    reason_for_warning: Optional[str] = field(
        default=None,
        metadata={
            "name": "reasonForWarning",
            "type": "Attribute",
        },
    )
    consequence_level: Optional[SignificanceTypeConsequenceLevel] = field(
        default=None,
        metadata={
            "name": "consequenceLevel",
            "type": "Attribute",
        },
    )


@dataclass
class ComparisonCheckType:
    """
    A ParameterInstanceRef to a value or another parameter instance.

    :ivar parameter_instance_ref:
    :ivar comparison_operator:
    :ivar value: Value is assumed to be of the same type as the
        comparison Parameter
    """

    parameter_instance_ref: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
            "max_occurs": 2,
        },
    )
    comparison_operator: Optional[ComparisonOperatorsType] = field(
        default=None,
        metadata={
            "name": "ComparisonOperator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "name": "Value",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )


@dataclass
class ComparisonType(ParameterInstanceRefType):
    """A simple ParameterInstanceRef to value comparison.

    The string supplied in the value attribute needs to be converted to
    a type matching the Parameter being compared to.  Numerical values
    are assumed to be base 10 unless proceeded by 0x (hexadecimal), 0o
    (octal), or 0b (binary).  The value is truncated  to use the least
    significant bits that match the bit size of the Parameter being
    compared to.
    """

    comparison_operator: ComparisonOperatorsType = field(
        default=ComparisonOperatorsType.EQUALS_SIGN_EQUALS_SIGN,
        metadata={
            "name": "comparisonOperator",
            "type": "Attribute",
        },
    )
    value: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class DataEncodingType:
    """Describes how a particular piece of data is sent or received from
    some non-native, off-platform device.

    (e.g. a spacecraft)

    :ivar error_detect_correct:
    :ivar byte_order_list: Used to describe an arbitrary byte order in
        multibyte parameters.  First byte in list is the first in the
        stream.  Byte significance is the highest for most significant
        bytes.  If not included, it is assumed that the most significant
        byte is first, least significant byte last.
    :ivar bit_order:
    """

    error_detect_correct: Optional[ErrorDetectCorrectType] = field(
        default=None,
        metadata={
            "name": "ErrorDetectCorrect",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    byte_order_list: Optional[ByteOrderType] = field(
        default=None,
        metadata={
            "name": "ByteOrderList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    bit_order: DataEncodingTypeBitOrder = field(
        default=DataEncodingTypeBitOrder.MOST_SIGNIFICANT_BIT_FIRST,
        metadata={
            "name": "bitOrder",
            "type": "Attribute",
        },
    )


@dataclass
class DecimalValueType:
    """
    Contains a Numeric value; value may be provided directly or via the
    value in a parameter.

    :ivar fixed_value:
    :ivar dynamic_value: Uses a parameter instance to obtain the value.
        The parameter value may be optionally adjusted by a Linear
        function or use a series of boolean expressions to lookup the
        value.  Anything more complex and a DynamicValue with a
        CustomAlgorithm may be used
    """

    fixed_value: Optional[Decimal] = field(
        default=None,
        metadata={
            "name": "FixedValue",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    dynamic_value: Optional["DecimalValueType.DynamicValue"] = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class DynamicValue:
        """
        :ivar parameter_instance_ref:
        :ivar linear_adjustment: A slope and intercept may be applied to
            scale or shift the value of the parameter in the dynamic
            value
        """

        parameter_instance_ref: Optional[ParameterInstanceRefType] = field(
            default=None,
            metadata={
                "name": "ParameterInstanceRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        linear_adjustment: Optional[
            "DecimalValueType.DynamicValue.LinearAdjustment"
        ] = field(
            default=None,
            metadata={
                "name": "LinearAdjustment",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class LinearAdjustment:
            slope: Decimal = field(
                default=Decimal("0"),
                metadata={
                    "type": "Attribute",
                },
            )
            intercept: Decimal = field(
                default=Decimal("0"),
                metadata={
                    "type": "Attribute",
                },
            )


@dataclass
class MathOperationType:
    """Postfix (aka Reverse Polish Notation (RPN)) notation is used to
    describe mathmatical equations.

    It uses a stack where operands (either fixed values or
    ParameterInstances) are pushed onto the stack from first to last in
    the XML. As the operators are specified, each pops off operands as
    it evaluates them, and pushes the result back onto the stack. In
    this case postfix is used to avoid having to specify parenthesis. To
    convert from infix to postfix, use Dijkstra's "shunting yard"
    algorithm.

    :ivar value_operand: Use a constant in the calculation
    :ivar this_parameter_operand: Use the value of this parameter in the
        calculation
    :ivar parameter_instance_ref_operand: Use the value of another
        Parameter in the calculation
    :ivar operator: Binary operators: +, -, *, /, %, ^ operate on the
        top two values in the stack, leaving the result on the top of
        the stack.  Unary operators: 1/x, x!, e^x, ln, log, and
        trigonometric operators operate on the top member of the stack
        also leaving the result on the top of the stack.  'ln' is a
        natural log where 'log' is a base 10 logarithm.  Trigonometric
        operators use degrees.  'swap' swaps the top two members of the
        stack.
    """

    value_operand: list[float] = field(
        default_factory=list,
        metadata={
            "name": "ValueOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    this_parameter_operand: list[object] = field(
        default_factory=list,
        metadata={
            "name": "ThisParameterOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_instance_ref_operand: list[ParameterInstanceRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterInstanceRefOperand",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    operator: list[MathOperatorsType] = field(
        default_factory=list,
        metadata={
            "name": "Operator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class NameDescriptionType(DescriptionType):
    """
    The type definition used by most elements that require a name with
    optional descriptions.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "required": True,
            "pattern": r"[a-zA-Z0-9_\-]*",
        },
    )


@dataclass
class OptionalNameDescriptionType(DescriptionType):
    """
    The type definition used by most elements that have an optional name
    with optional descriptions.
    """

    name: Optional[str] = field(
        default=None,
        metadata={
            "type": "Attribute",
            "pattern": r"[a-zA-Z0-9_\-]*",
        },
    )


@dataclass
class ReferenceTimeType:
    """Most time values are relative to another time e.g. seconds are
    relative to minutes, minutes are relative to hours.

    This type is used to describe this relationship starting with the
    least significant time Parameter to and progressing to the most
    significant time parameter.
    """

    offset_from: Optional[ParameterInstanceRefType] = field(
        default=None,
        metadata={
            "name": "OffsetFrom",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    epoch: Optional[Union[XmlDate, EpochTypeValue]] = field(
        default=None,
        metadata={
            "name": "Epoch",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class TimeAssociationType(ParameterInstanceRefType):
    """Telemetry parameter instances are oftentimes "time-tagged" with a
    timing signal either provided on the ground or on  the space system.

    This data element allows one to specify which of possibly many
    AbsoluteTimeParameters to use to "time-tag" parameter instances
    with.

    :ivar interpolate_time: If true, then the current value of the
        AbsoluteTime will be projected to current time.  In other words,
        if the value of the AbsoluteTime parameter was set 10 seconds
        ago, then 10 seconds will be added to its value before
        associating this time with the parameter.
    :ivar offset: The offset is used to supply a relative time offset
        from the time association and to this parameter
    """

    interpolate_time: bool = field(
        default=True,
        metadata={
            "name": "interpolateTime",
            "type": "Attribute",
        },
    )
    offset: Optional[XmlDate] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class AndedConditionsType:
    """A list of boolean comparisons, or boolean groups that are logically
    ANDed together.

    Any ORed conditions in the list are evaluated first.
    """

    class Meta:
        name = "ANDedConditionsType"

    condition: list[ComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
        },
    )
    ored_conditions: list["OredConditionsType"] = field(
        default_factory=list,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
        },
    )


@dataclass
class AggregateDataType(NameDescriptionType):
    """
    Contains multiple values (as members) of any type.

    :ivar member_list: Order is important only if the name of the
        AggregateParameter or Aggregate Argument is directly referenced
        in SequenceContainers.  In this case the members are assued to
        be added sequentially (in the order listed here) into the
        Container.
    """

    member_list: Optional["AggregateDataType.MemberList"] = field(
        default=None,
        metadata={
            "name": "MemberList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )

    @dataclass
    class MemberList:
        """
        :ivar member: Each member of the Aggregate Data has a name and a
            reference to another DataType.  The other DataType may be
            any other  DataType.  Circular references are not allowed.
        """

        member: list["AggregateDataType.MemberList.Member"] = field(
            default_factory=list,
            metadata={
                "name": "Member",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Member:
            name: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                    "pattern": r"[a-zA-Z0-9_\-]*",
                },
            )
            type_ref: Optional[str] = field(
                default=None,
                metadata={
                    "name": "typeRef",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class ArrayDataTypeType(NameDescriptionType):
    """
    An array of values of the type referenced in 'arrayTypeRef' and have the
    number of array dimensions as specified in 'numberOfDimensions'.
    """

    array_type_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "arrayTypeRef",
            "type": "Attribute",
            "required": True,
        },
    )
    number_of_dimensions: Optional[int] = field(
        default=None,
        metadata={
            "name": "numberOfDimensions",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class CalibratorType(OptionalNameDescriptionType):
    """
    Calibrators are normally used to convert to and from bit compacted
    numerical data.

    :ivar spline_calibrator: A calibration type where a segmented line
        in a raw vs calibrated plane is described using a set of points.
        Raw values are converted to calibrated values by finding a
        position on the line corresponding  to the raw value. The
        algorithm triggers on the input parameter.
    :ivar polynomial_calibrator: A calibration type where a curve in a
        raw vs calibrated plane is described using a set of polynomial
        coefficients.  Raw values are converted to calibrated values by
        finding a position on the curve corresponding to the raw value.
        The first coefficient belongs with the X^0 term, the next
        coefficient belongs to the X^1 term and so on.
    :ivar math_operation_calibrator:
    """

    spline_calibrator: Optional["CalibratorType.SplineCalibrator"] = field(
        default=None,
        metadata={
            "name": "SplineCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    polynomial_calibrator: Optional[PolynomialType] = field(
        default=None,
        metadata={
            "name": "PolynomialCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    math_operation_calibrator: Optional[MathOperationType] = field(
        default=None,
        metadata={
            "name": "MathOperationCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class SplineCalibrator:
        spline_point: list[SplinePointType] = field(
            default_factory=list,
            metadata={
                "name": "SplinePoint",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 2,
            },
        )
        order: int = field(
            default=1,
            metadata={
                "type": "Attribute",
            },
        )
        extrapolate: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass
class MathAlgorithmType(NameDescriptionType):
    """
    A simple mathematical operation.
    """

    math_operation: Optional["MathAlgorithmType.MathOperation"] = field(
        default=None,
        metadata={
            "name": "MathOperation",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )

    @dataclass
    class MathOperation(MathOperationType):
        trigger_set: Optional[TriggerSetType] = field(
            default=None,
            metadata={
                "name": "TriggerSet",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        output_parameter_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "outputParameterRef",
                "type": "Attribute",
                "required": True,
            },
        )


@dataclass
class NumberToStringType(OptionalNameDescriptionType):
    """There are two ways numeric data can be changed to string data: using a Java style NumberFormat, or using an enumerated list.   Enumerated lists can be assigned to a single value or a value range.

    :ivar value_enumeration: A number or range assigned to a string.
    :ivar range_enumeration: A string value associated with a numerical
        range.
    :ivar number_format:
    """

    value_enumeration: list[ValueEnumerationType] = field(
        default_factory=list,
        metadata={
            "name": "ValueEnumeration",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    range_enumeration: list[FloatRangeType] = field(
        default_factory=list,
        metadata={
            "name": "RangeEnumeration",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    number_format: Optional["NumberToStringType.NumberFormat"] = field(
        default=None,
        metadata={
            "name": "NumberFormat",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class NumberFormat:
        number_base: Optional[RadixType] = field(
            default=None,
            metadata={
                "name": "numberBase",
                "type": "Attribute",
            },
        )
        minimum_fraction_digits: Optional[int] = field(
            default=None,
            metadata={
                "name": "minimumFractionDigits",
                "type": "Attribute",
            },
        )
        maximum_fraction_digits: Optional[int] = field(
            default=None,
            metadata={
                "name": "maximumFractionDigits",
                "type": "Attribute",
            },
        )
        minimum_integer_digits: Optional[int] = field(
            default=None,
            metadata={
                "name": "minimumIntegerDigits",
                "type": "Attribute",
            },
        )
        maximum_integer_digits: Optional[int] = field(
            default=None,
            metadata={
                "name": "maximumIntegerDigits",
                "type": "Attribute",
            },
        )
        negative_suffix: Optional[str] = field(
            default=None,
            metadata={
                "name": "negativeSuffix",
                "type": "Attribute",
            },
        )
        positive_suffix: Optional[str] = field(
            default=None,
            metadata={
                "name": "positiveSuffix",
                "type": "Attribute",
            },
        )
        negative_prefix: str = field(
            default="-",
            metadata={
                "name": "negativePrefix",
                "type": "Attribute",
            },
        )
        positive_prefix: Optional[str] = field(
            default=None,
            metadata={
                "name": "positivePrefix",
                "type": "Attribute",
            },
        )
        show_thousands_grouping: bool = field(
            default=True,
            metadata={
                "name": "showThousandsGrouping",
                "type": "Attribute",
            },
        )
        notation: NumberFormatNotation = field(
            default=NumberFormatNotation.NORMAL,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass
class PcmstreamType(NameDescriptionType):
    """
    A PCM Stream Type is the high level definition for all Pulse Code
    Modulated (PCM) (i.e., binary) streams.
    """

    class Meta:
        name = "PCMStreamType"

    bit_rate_in_bps: Optional[float] = field(
        default=None,
        metadata={
            "name": "bitRateInBPS",
            "type": "Attribute",
        },
    )
    pcm_type: PcmstreamTypePcmType = field(
        default=PcmstreamTypePcmType.NRZL,
        metadata={
            "name": "pcmType",
            "type": "Attribute",
        },
    )
    inverted: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ParameterToSetType:
    """
    Used by Meta Command to indicate ground Parameters that should be set
    after completion of a command.
    """

    parameter_ref: Optional[ParameterRefType] = field(
        default=None,
        metadata={
            "name": "ParameterRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    derivation: Optional[MathOperationType] = field(
        default=None,
        metadata={
            "name": "Derivation",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )


@dataclass
class ServiceType(NameDescriptionType):
    """
    Holds a set of services, logical groups of containers  OR messages (not
    both).
    """

    message_ref_set: Optional["ServiceType.MessageRefSet"] = field(
        default=None,
        metadata={
            "name": "MessageRefSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_ref_set: Optional["ServiceType.ContainerRefSet"] = field(
        default=None,
        metadata={
            "name": "ContainerRefSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class MessageRefSet:
        message_ref: list[MessageRefType] = field(
            default_factory=list,
            metadata={
                "name": "MessageRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

    @dataclass
    class ContainerRefSet:
        container_ref: list[ContainerRefType] = field(
            default_factory=list,
            metadata={
                "name": "ContainerRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class SimpleAlgorithmType(NameDescriptionType):
    """The simplest form of algorithm, a SimpleAlgorithmType contains an
    area for a free-form pseudo code description of the algorithm plus a Set
    of references to external algorithms.

    External algorithms are usually unique to a ground system type.
    Multiple external algorithms are possible because XTCE documents may
    be used across multiple ground systems.

    :ivar algorithm_text: This optional element may be used to enter
        Pseudo or actual code for the algorithm.  The language for the
        algorithm is specified with the language attribute
    :ivar external_algorithm_set:
    """

    algorithm_text: Optional["SimpleAlgorithmType.AlgorithmText"] = field(
        default=None,
        metadata={
            "name": "AlgorithmText",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    external_algorithm_set: Optional["SimpleAlgorithmType.ExternalAlgorithmSet"] = (
        field(
            default=None,
            metadata={
                "name": "ExternalAlgorithmSet",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )

    @dataclass
    class AlgorithmText:
        value: str = field(
            default="",
            metadata={
                "required": True,
            },
        )
        language: str = field(
            default="pseudo",
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class ExternalAlgorithmSet:
        """
        :ivar external_algorithm: This is the external algorithm.
            Multiple entries are provided so that the same database may
            be used for multiple implementation s
        """

        external_algorithm: list[
            "SimpleAlgorithmType.ExternalAlgorithmSet.ExternalAlgorithm"
        ] = field(
            default_factory=list,
            metadata={
                "name": "ExternalAlgorithm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class ExternalAlgorithm:
            implementation_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "implementationName",
                    "type": "Attribute",
                    "required": True,
                },
            )
            algorithm_location: Optional[str] = field(
                default=None,
                metadata={
                    "name": "algorithmLocation",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class FrameStreamType(PcmstreamType):
    """
    The top level type definition for all data streams that are frame based.

    :ivar container_ref: This Container (usually abstract) is the
        container that is in the fixed frame stream.  Normally, this is
        a general container type from which many specific containers are
        inherited.
    :ivar service_ref:
    :ivar stream_ref: This is a reference to a connecting stream - say a
        custom stream.
    """

    container_ref: Optional[ContainerRefType] = field(
        default=None,
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    service_ref: Optional[ServiceRefType] = field(
        default=None,
        metadata={
            "name": "ServiceRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    stream_ref: Optional[StreamRefType] = field(
        default=None,
        metadata={
            "name": "StreamRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class InputAlgorithmType(SimpleAlgorithmType):
    """
    A set of labeled inputs is added to the SimpleAlgorithmType.
    """

    input_set: Optional["InputAlgorithmType.InputSet"] = field(
        default=None,
        metadata={
            "name": "InputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class InputSet:
        """
        :ivar parameter_instance_ref: Names an input parameter to the
            algorithm.  There are two attributes to InputParm, inputName
            and parameterName. parameterName is a parameter reference
            name for a parameter that will be used in this algorithm.
            inputName is an optional "friendly" name for the input
            parameter.
        :ivar constant: Names and provides a value for a constant input
            to the algorithm.  There are two attributes to Constant,
            constantName and value.  constantName is a variable name in
            the algorithm to be executed.  value is the value of the
            constant to be used.
        """

        parameter_instance_ref: list[
            "InputAlgorithmType.InputSet.ParameterInstanceRef"
        ] = field(
            default_factory=list,
            metadata={
                "name": "ParameterInstanceRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        constant: list["InputAlgorithmType.InputSet.Constant"] = field(
            default_factory=list,
            metadata={
                "name": "Constant",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ParameterInstanceRef(ParameterInstanceRefType):
            input_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "inputName",
                    "type": "Attribute",
                },
            )

        @dataclass
        class Constant:
            constant_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "constantName",
                    "type": "Attribute",
                },
            )
            value: Optional[str] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class OredConditionsType:
    """A list of boolean comparisons, or boolean groups that are logically
    ORed together.

    Any ANDed conditions in the list are evaluated first.
    """

    class Meta:
        name = "ORedConditionsType"

    condition: list[ComparisonCheckType] = field(
        default_factory=list,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
        },
    )
    anded_conditions: list[AndedConditionsType] = field(
        default_factory=list,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 2,
        },
    )


@dataclass
class BooleanExpressionType:
    """
    Holds an arbitrarily complex boolean expression.
    """

    condition: Optional[ComparisonCheckType] = field(
        default=None,
        metadata={
            "name": "Condition",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    anded_conditions: Optional[AndedConditionsType] = field(
        default=None,
        metadata={
            "name": "ANDedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    ored_conditions: Optional[OredConditionsType] = field(
        default=None,
        metadata={
            "name": "ORedConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class InputOutputAlgorithmType(InputAlgorithmType):
    """
    A set of labeled outputs are added to the SimpleInputAlgorithmType.
    """

    output_set: Optional["InputOutputAlgorithmType.OutputSet"] = field(
        default=None,
        metadata={
            "name": "OutputSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    thread: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class OutputSet:
        """
        :ivar output_parameter_ref: Names an output parameter to the
            algorithm.  There are two attributes to OutputParm,
            outputName and parameterName. parameterName is a parameter
            reference name for a parameter that will be updated by this
            algorithm.  outputName is an optional "friendly" name for
            the output parameter.
        """

        output_parameter_ref: list[
            "InputOutputAlgorithmType.OutputSet.OutputParameterRef"
        ] = field(
            default_factory=list,
            metadata={
                "name": "OutputParameterRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class OutputParameterRef(ParameterRefType):
            output_name: Optional[str] = field(
                default=None,
                metadata={
                    "name": "outputName",
                    "type": "Attribute",
                },
            )


@dataclass
class SyncStrategyType:
    """A Sync Strategy specifies the strategy on how to find frames within a
    stream of PCM data.

    The sync strategy is based upon a state machine that begins in the
    'Search' state until the first sync marker is found.  Then it goes
    into the 'Verify' state until a specified number of successive good
    sync markers are found.  Then, the state machine goes into the
    'Lock' state, in the 'Lock' state frames are considered good.
    Should a sync marker be missed in the 'Lock' state, the state
    machine will transition into the 'Check' state, if the next sync
    marker is where it's expected within a specified number of frames,
    then the state machine will transition back to the 'Lock' state, it
    not it will transition back to 'Search'.

    :ivar auto_invert: After searching for the frame sync marker for
        some number of bits, it may be desirable to invert the incoming
        data, and then look for frame sync.  In some cases this will
        require an external algorithm
    :ivar verify_to_lock_good_frames:
    :ivar check_to_lock_good_frames:
    :ivar max_bit_errors_in_sync_pattern: Maximum number of bit errors
        in the sync pattern (marker).
    """

    auto_invert: Optional["SyncStrategyType.AutoInvert"] = field(
        default=None,
        metadata={
            "name": "AutoInvert",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    verify_to_lock_good_frames: int = field(
        default=4,
        metadata={
            "name": "verifyToLockGoodFrames",
            "type": "Attribute",
        },
    )
    check_to_lock_good_frames: int = field(
        default=1,
        metadata={
            "name": "checkToLockGoodFrames",
            "type": "Attribute",
        },
    )
    max_bit_errors_in_sync_pattern: int = field(
        default=0,
        metadata={
            "name": "maxBitErrorsInSyncPattern",
            "type": "Attribute",
        },
    )

    @dataclass
    class AutoInvert:
        invert_algorithm: Optional[InputAlgorithmType] = field(
            default=None,
            metadata={
                "name": "InvertAlgorithm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        bad_frames_to_auto_invert: int = field(
            default=1024,
            metadata={
                "name": "badFramesToAutoInvert",
                "type": "Attribute",
            },
        )


@dataclass
class CommandVerifierType(OptionalNameDescriptionType):
    """A command verifier is used to check that the command has been
    successfully executed.

    Command Verifiers may be either a Custom Algorithm or a Boolean
    Check or the presence of a Container for a relative change in the
    value of a Parameter.  The CheckWindow is a time period where the
    verification must test true to pass.

    :ivar comparison_list: All comparisons must be true
    :ivar container_ref: When verification is a new instance the
        referenced Container
    :ivar parameter_value_change: Used to look for relative change in a
        Parameter value.  Only useful for numeric Parameters
    :ivar custom_algorithm:
    :ivar boolean_expression:
    :ivar comparison:
    :ivar check_window:
    :ivar check_window_algorithms: Used when times must be calculated
    """

    comparison_list: Optional["CommandVerifierType.ComparisonList"] = field(
        default=None,
        metadata={
            "name": "ComparisonList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_ref: Optional[ContainerRefType] = field(
        default=None,
        metadata={
            "name": "ContainerRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_value_change: Optional["CommandVerifierType.ParameterValueChange"] = (
        field(
            default=None,
            metadata={
                "name": "ParameterValueChange",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    custom_algorithm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    boolean_expression: Optional[BooleanExpressionType] = field(
        default=None,
        metadata={
            "name": "BooleanExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    comparison: Optional[ComparisonType] = field(
        default=None,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    check_window: Optional["CommandVerifierType.CheckWindow"] = field(
        default=None,
        metadata={
            "name": "CheckWindow",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    check_window_algorithms: Optional["CommandVerifierType.CheckWindowAlgorithms"] = (
        field(
            default=None,
            metadata={
                "name": "CheckWindowAlgorithms",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )

    @dataclass
    class ComparisonList:
        comparison: list[ComparisonType] = field(
            default_factory=list,
            metadata={
                "name": "Comparison",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

    @dataclass
    class ParameterValueChange:
        parameter_ref: Optional[ParameterRefType] = field(
            default=None,
            metadata={
                "name": "ParameterRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        change: Optional["CommandVerifierType.ParameterValueChange.Change"] = field(
            default=None,
            metadata={
                "name": "Change",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )

        @dataclass
        class Change:
            value: Optional[Decimal] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )

    @dataclass
    class CheckWindow:
        time_to_start_checking: Optional[XmlDuration] = field(
            default=None,
            metadata={
                "name": "timeToStartChecking",
                "type": "Attribute",
            },
        )
        time_to_stop_checking: Optional[XmlDuration] = field(
            default=None,
            metadata={
                "name": "timeToStopChecking",
                "type": "Attribute",
                "required": True,
            },
        )
        time_window_is_relative_to: CheckWindowTimeWindowIsRelativeTo = field(
            default=CheckWindowTimeWindowIsRelativeTo.TIME_LAST_VERIFIER_PASSED,
            metadata={
                "name": "timeWindowIsRelativeTo",
                "type": "Attribute",
            },
        )

    @dataclass
    class CheckWindowAlgorithms:
        start_check: Optional[InputAlgorithmType] = field(
            default=None,
            metadata={
                "name": "StartCheck",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        stop_time: Optional[InputAlgorithmType] = field(
            default=None,
            metadata={
                "name": "StopTime",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )


@dataclass
class CustomStreamType(PcmstreamType):
    """A stream type where some level of custom processing (e.g.
    convolutional, encryption, compression) is performed.

    Has a reference to external algorithms for encoding and decoding
    algorithms.

    :ivar encoding_algorithm:
    :ivar decoding_algorithm: Algorithm outputs may be used to set
        decoding quality parameters.
    :ivar encoded_stream_ref:
    :ivar decoded_stream_ref:
    """

    encoding_algorithm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "EncodingAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    decoding_algorithm: Optional[InputOutputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "DecodingAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    encoded_stream_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "encodedStreamRef",
            "type": "Attribute",
            "required": True,
        },
    )
    decoded_stream_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "decodedStreamRef",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class FixedFrameStreamType(FrameStreamType):
    """For streams that contain a series of frames with a fixed frame length
    where the frames are found by looking for a marker in the data.

    This marker is sometimes called the frame sync pattern and sometimes
    the Asynchronous Sync Marker (ASM).  This marker need not be
    contiguous although it usually is.

    :ivar sync_strategy:
    :ivar sync_aperture_in_bits: Allowed slip (in bits) in either
        direction for the sync pattern
    :ivar frame_length_in_bits:
    """

    sync_strategy: Optional["FixedFrameStreamType.SyncStrategy"] = field(
        default=None,
        metadata={
            "name": "SyncStrategy",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    sync_aperture_in_bits: int = field(
        default=0,
        metadata={
            "name": "syncApertureInBits",
            "type": "Attribute",
        },
    )
    frame_length_in_bits: Optional[int] = field(
        default=None,
        metadata={
            "name": "frameLengthInBits",
            "type": "Attribute",
            "required": True,
        },
    )

    @dataclass
    class SyncStrategy(SyncStrategyType):
        """
        :ivar sync_pattern: The pattern of bits used to look for frame
            synchronization.
        """

        sync_pattern: Optional["FixedFrameStreamType.SyncStrategy.SyncPattern"] = field(
            default=None,
            metadata={
                "name": "SyncPattern",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )

        @dataclass
        class SyncPattern:
            """
            :ivar pattern: CCSDS ASM for non-turbocoded frames =
                1acffc1d
            :ivar bit_location_from_start_of_container:
            :ivar mask:
            :ivar mask_length_in_bits: truncate the mask from the left
            :ivar pattern_length_in_bits: truncate the pattern from the
                left
            """

            pattern: Optional[bytes] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                    "format": "base16",
                },
            )
            bit_location_from_start_of_container: int = field(
                default=0,
                metadata={
                    "name": "bitLocationFromStartOfContainer",
                    "type": "Attribute",
                },
            )
            mask: Optional[bytes] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "format": "base16",
                },
            )
            mask_length_in_bits: Optional[int] = field(
                default=None,
                metadata={
                    "name": "maskLengthInBits",
                    "type": "Attribute",
                },
            )
            pattern_length_in_bits: Optional[int] = field(
                default=None,
                metadata={
                    "name": "patternLengthInBits",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class InputOutputTriggerAlgorithmType(InputOutputAlgorithmType):
    """
    A set of labeled triggers is added to the
    SimpleInputOutputAlgorithmType.

    :ivar trigger_set:
    :ivar trigger_container: First telemetry container from which the
        output parameter should be calculated.
    :ivar priority: Algorithm processing priority.
    """

    trigger_set: Optional[TriggerSetType] = field(
        default=None,
        metadata={
            "name": "TriggerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    trigger_container: Optional[str] = field(
        default=None,
        metadata={
            "name": "triggerContainer",
            "type": "Attribute",
            "pattern": r"[a-zA-Z0-9_\-]*",
        },
    )
    priority: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class MatchCriteriaType:
    """
    Contains either a simple Comparison, a ComparisonList, an arbitrarily
    complex BooleanExpression or an escape to an externally defined
    algorithm.

    :ivar comparison: A simple comparison check
    :ivar comparison_list: All comparisons must be true
    :ivar boolean_expression: An arbitrarily complex boolean expression
    :ivar custom_algorithm: An escape to an externally defined algorithm
    """

    comparison: Optional[ComparisonType] = field(
        default=None,
        metadata={
            "name": "Comparison",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    comparison_list: Optional["MatchCriteriaType.ComparisonList"] = field(
        default=None,
        metadata={
            "name": "ComparisonList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    boolean_expression: Optional[BooleanExpressionType] = field(
        default=None,
        metadata={
            "name": "BooleanExpression",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    custom_algorithm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class ComparisonList:
        comparison: list[ComparisonType] = field(
            default_factory=list,
            metadata={
                "name": "Comparison",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class VariableFrameStreamType(FrameStreamType):
    """For streams that contain a series of frames with a variable frame
    length where the frames are found by looking for a series of one's or
    zero's (usually one's).

    The series is called the flag.   in the PCM stream that are usually
    made to be illegal in the PCM stream by zero or one bit insertion.
    """

    sync_strategy: Optional["VariableFrameStreamType.SyncStrategy"] = field(
        default=None,
        metadata={
            "name": "SyncStrategy",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )

    @dataclass
    class SyncStrategy(SyncStrategyType):
        """
        :ivar flag: The pattern of bits used to look for frame
            synchronization.
        """

        flag: Optional["VariableFrameStreamType.SyncStrategy.Flag"] = field(
            default=None,
            metadata={
                "name": "Flag",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )

        @dataclass
        class Flag:
            flag_size_in_bits: int = field(
                default=6,
                metadata={
                    "name": "flagSizeInBits",
                    "type": "Attribute",
                },
            )
            flag_bit_type: FlagFlagBitType = field(
                default=FlagFlagBitType.ONES,
                metadata={
                    "name": "flagBitType",
                    "type": "Attribute",
                },
            )


@dataclass
class AlarmConditionsType:
    """
    When the alarm is determined by boolean logic.
    """

    watch_alarm: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "WatchAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    warning_alarm: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "WarningAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    distress_alarm: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "DistressAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    critical_alarm: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "CriticalAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    severe_alarm: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "SevereAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class AlgorithmSetType:
    """
    An unordered collection of algorithms.
    """

    custom_algorithm: list[InputOutputTriggerAlgorithmType] = field(
        default_factory=list,
        metadata={
            "name": "CustomAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    math_algorithm: list[MathAlgorithmType] = field(
        default_factory=list,
        metadata={
            "name": "MathAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class ContextCalibratorType:
    """Context calibrations are applied when the ContextMatch is true.

    Context calibrators overide Default calibrators
    """

    context_match: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    calibrator: Optional[CalibratorType] = field(
        default=None,
        metadata={
            "name": "Calibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )


@dataclass
class IntegerValueType:
    """
    Contains an Integer value; value may be provided directly or via the
    value in a parameter.

    :ivar fixed_value:
    :ivar dynamic_value: Uses a parameter instance to obtain the value.
        The parameter value may be optionally adjusted by a Linear
        function or use a series of boolean expressions to lookup the
        value.  Anything more complex and a DynamicValue with a
        CustomAlgorithm may be used
    :ivar discrete_lookup_list: Lookup a value using the lookup list
        supplied.  Use the first match found.
    """

    fixed_value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "name": "FixedValue",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )
    dynamic_value: Optional["IntegerValueType.DynamicValue"] = field(
        default=None,
        metadata={
            "name": "DynamicValue",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    discrete_lookup_list: Optional["IntegerValueType.DiscreteLookupList"] = field(
        default=None,
        metadata={
            "name": "DiscreteLookupList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class DynamicValue:
        """
        :ivar parameter_instance_ref:
        :ivar linear_adjustment: A slope and intercept may be applied to
            scale or shift the value of the parameter in the dynamic
            value
        """

        parameter_instance_ref: Optional[ParameterInstanceRefType] = field(
            default=None,
            metadata={
                "name": "ParameterInstanceRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        linear_adjustment: Optional[
            "IntegerValueType.DynamicValue.LinearAdjustment"
        ] = field(
            default=None,
            metadata={
                "name": "LinearAdjustment",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class LinearAdjustment:
            slope: int = field(
                default=0,
                metadata={
                    "type": "Attribute",
                },
            )
            intercept: int = field(
                default=0,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class DiscreteLookupList:
        discrete_lookup: list["IntegerValueType.DiscreteLookupList.DiscreteLookup"] = (
            field(
                default_factory=list,
                metadata={
                    "name": "DiscreteLookup",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )
        )

        @dataclass
        class DiscreteLookup(MatchCriteriaType):
            value: Optional[int] = field(
                default=None,
                metadata={
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class ParameterPropertiesType:
    """
    A wrapper for those properties that are unique to telemetry parameters.

    :ivar system_name: Optional.  Normally used when the database is
        built in a flat, non-hierarchical format
    :ivar validity_condition: Optional condition that must be true for
        this Parameter to be valid
    :ivar physical_address_set: One or more physical addresses may be
        associated with each Parameter.  Examples of physical addresses
        include a location on the spacecraft or a location on a data
        collection bus.
    :ivar time_association: This time will override any Default value
        for TimeAssociation.
    :ivar data_source: A telemetered Parameter is one that will have
        values in telemetry.  A derived Parameter is one that is
        calculated, usually be an Algorithm.  A constant Parameter is
        one that is used as a constant in the system (e.g. a vehicle
        id).  A local Parameter is one that is used purely on the ground
        (e.g. a ground command counter).
    :ivar read_only: A Parameter marked as 'readOnly' true is constant
        and non-settable
    """

    system_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SystemName",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    validity_condition: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "ValidityCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    physical_address_set: Optional["ParameterPropertiesType.PhysicalAddressSet"] = (
        field(
            default=None,
            metadata={
                "name": "PhysicalAddressSet",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    time_association: Optional[TimeAssociationType] = field(
        default=None,
        metadata={
            "name": "TimeAssociation",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    data_source: Optional[ParameterPropertiesTypeDataSource] = field(
        default=None,
        metadata={
            "name": "dataSource",
            "type": "Attribute",
        },
    )
    read_only: bool = field(
        default=False,
        metadata={
            "name": "readOnly",
            "type": "Attribute",
        },
    )

    @dataclass
    class PhysicalAddressSet:
        """
        :ivar physical_address: Contains the address (e.g., channel
            information) required to process the spacecraft telemetry
            streams. May be an onboard  id, a mux address, or a physical
            location. Contains the address (channel information)
            required to process the spacecraft telemetry streams
        """

        physical_address: list[PhysicalAddressType] = field(
            default_factory=list,
            metadata={
                "name": "PhysicalAddress",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )


@dataclass
class StreamSetType:
    """
    Contains an unordered set of Streams.
    """

    fixed_frame_stream: list[FixedFrameStreamType] = field(
        default_factory=list,
        metadata={
            "name": "FixedFrameStream",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    variable_frame_stream: list[VariableFrameStreamType] = field(
        default_factory=list,
        metadata={
            "name": "VariableFrameStream",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    custom_stream: list[CustomStreamType] = field(
        default_factory=list,
        metadata={
            "name": "CustomStream",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class AlarmType:
    """
    Alarms associated with numeric data types.

    :ivar alarm_conditions: A MatchCriteria may be specified for each of
        the 5 alarm levels.  Each level is optional and the alarm should
        be the highest level to test true.
    :ivar custom_alarm: An escape for ridiculously complex alarm
        conditions.  Will trigger on changes to the  containing
        Parameter.
    :ivar min_violations: Number of successive instances that meet the
        alarm conditions for the Alarm to trigger.
    """

    alarm_conditions: Optional[AlarmConditionsType] = field(
        default=None,
        metadata={
            "name": "AlarmConditions",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    custom_alarm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "CustomAlarm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    min_violations: int = field(
        default=1,
        metadata={
            "name": "minViolations",
            "type": "Attribute",
        },
    )


@dataclass
class BinaryDataEncodingType(DataEncodingType):
    """For binary data or for integer, float, string, or time data that is
    not in any of the known encoding formats.

    For any data that is not encoded in any of the known integer, float,
    string, or time data formats use a To/From transform algorithm.

    :ivar size_in_bits:
    :ivar from_binary_transform_algorithm: Used to convert binary data
        to an application data type
    :ivar to_binary_transform_algorithm: Used to convert binary data
        from an application data type to binary data
    """

    size_in_bits: Optional[IntegerValueType] = field(
        default=None,
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    from_binary_transform_algorithm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "FromBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    to_binary_transform_algorithm: Optional[InputAlgorithmType] = field(
        default=None,
        metadata={
            "name": "ToBinaryTransformAlgorithm",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class FloatDataEncodingType(DataEncodingType):
    """
    For common encodings of floating point data.

    :ivar default_calibrator:
    :ivar context_calibrator_list: Use when different calibrations must
        be used on the Parameter in different contexts.  Use the first
        one that tests true
    :ivar encoding:
    :ivar size_in_bits:
    """

    default_calibrator: Optional[CalibratorType] = field(
        default=None,
        metadata={
            "name": "DefaultCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    context_calibrator_list: Optional["FloatDataEncodingType.ContextCalibratorList"] = (
        field(
            default=None,
            metadata={
                "name": "ContextCalibratorList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    encoding: FloatDataEncodingTypeEncoding = field(
        default=FloatDataEncodingTypeEncoding.IEEE754_1985,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: FloatDataEncodingTypeSizeInBits = field(
        default=FloatDataEncodingTypeSizeInBits.VALUE_32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )

    @dataclass
    class ContextCalibratorList:
        context_calibrator: list[ContextCalibratorType] = field(
            default_factory=list,
            metadata={
                "name": "ContextCalibrator",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class IntegerDataEncodingType(DataEncodingType):
    """
    For all major encodings of integer data.

    :ivar default_calibrator:
    :ivar context_calibrator_list: Use when different calibrations must
        be used on the Parameter in different contexts.  Use the first
        one that tests true
    :ivar encoding:
    :ivar size_in_bits:
    """

    default_calibrator: Optional[CalibratorType] = field(
        default=None,
        metadata={
            "name": "DefaultCalibrator",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    context_calibrator_list: Optional[
        "IntegerDataEncodingType.ContextCalibratorList"
    ] = field(
        default=None,
        metadata={
            "name": "ContextCalibratorList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    encoding: IntegerDataEncodingTypeEncoding = field(
        default=IntegerDataEncodingTypeEncoding.UNSIGNED,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: int = field(
        default=8,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )

    @dataclass
    class ContextCalibratorList:
        context_calibrator: list[ContextCalibratorType] = field(
            default_factory=list,
            metadata={
                "name": "ContextCalibrator",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class ParameterSetType:
    """
    Used by both the TelemetryMetaData and the CommandMetaData components
    each may be built independently.

    :ivar parameter:
    :ivar parameter_ref: Used to include a Parameter defined in another
        sub-system in this sub-system.
    """

    parameter: list["ParameterSetType.Parameter"] = field(
        default_factory=list,
        metadata={
            "name": "Parameter",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_ref: list[ParameterRefType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRef",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class Parameter(NameDescriptionType):
        """
        :ivar parameter_properties:
        :ivar parameter_type_ref:
        :ivar initial_value: Used to set the initial calibrated values
            of Parameters.  Will overwrite an initial value defined for
            the ParameterType.  For integer types base 10 (decimal) form
            is assumed unless: if proceeded by a 0b or 0B, value is in
            base two (binary form, if proceeded by a 0o or 0O, values is
            in base 8 (octal) form, or if proceeded by a 0x or 0X, value
            is in base 16 (hex) form.  Floating point types may be
            specified in normal (100.0) or scientific (1.0e2) form.
            Time types are specified using the ISO 8601 formats
            described for XTCE time data types.  Initial values for
            string types, may include C language style (\\n, \\t, \\",
            \\\\, etc.) escape sequences.  Initial values for Array or
            Aggregate types may not be set.
        """

        parameter_properties: Optional[ParameterPropertiesType] = field(
            default=None,
            metadata={
                "name": "ParameterProperties",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        parameter_type_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "parameterTypeRef",
                "type": "Attribute",
                "required": True,
            },
        )
        initial_value: Optional[str] = field(
            default=None,
            metadata={
                "name": "initialValue",
                "type": "Attribute",
            },
        )


@dataclass
class RepeatType:
    """
    Hold a structure that can be repeated X times, where X is the Count.

    :ivar count: Value (either fixed or dynamic) that contains the count
        of repeated structures.
    :ivar offset: Indicates the distance between repeating entries (the
        last bit of one entry to the start bit of the next entry)
    """

    count: Optional[IntegerValueType] = field(
        default=None,
        metadata={
            "name": "Count",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    offset: Optional["RepeatType.Offset"] = field(
        default=None,
        metadata={
            "name": "Offset",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class Offset(IntegerValueType):
        offset_size_in_bits: int = field(
            default=1,
            metadata={
                "name": "offsetSizeInBits",
                "type": "Attribute",
            },
        )


@dataclass
class StringDataEncodingType(DataEncodingType):
    """
    For common encodings of string data.
    """

    size_in_bits: Optional["StringDataEncodingType.SizeInBits"] = field(
        default=None,
        metadata={
            "name": "SizeInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    encoding: StringDataEncodingTypeEncoding = field(
        default=StringDataEncodingTypeEncoding.UTF_8,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class SizeInBits:
        """
        :ivar fixed:
        :ivar termination_char: Like C strings, they are terminated with
            a special string, usually a null character.
        :ivar leading_size: Like PASCAL strings, the size of the string
            is given as an integer at the start of the string.  SizeTag
            must be an unsigned Integer
        """

        fixed: Optional[IntegerValueType] = field(
            default=None,
            metadata={
                "name": "Fixed",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        termination_char: Optional[bytes] = field(
            default=None,
            metadata={
                "name": "TerminationChar",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "format": "base16",
            },
        )
        leading_size: Optional["StringDataEncodingType.SizeInBits.LeadingSize"] = field(
            default=None,
            metadata={
                "name": "LeadingSize",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class LeadingSize:
            size_in_bits_of_size_tag: int = field(
                default=16,
                metadata={
                    "name": "sizeInBitsOfSizeTag",
                    "type": "Attribute",
                },
            )


@dataclass
class BaseDataType(NameDescriptionType):
    """
    An abstract type used by within the schema to derive other data types by
    the ground system.

    :ivar unit_set:
    :ivar binary_data_encoding:
    :ivar float_data_encoding:
    :ivar integer_data_encoding:
    :ivar string_data_encoding:
    :ivar base_type: Used to derive one Data Type from another - will
        inherit all the attributes from the baseType any of which may be
        redefined in this type definition.
    """

    unit_set: Optional["BaseDataType.UnitSet"] = field(
        default=None,
        metadata={
            "name": "UnitSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    binary_data_encoding: Optional[BinaryDataEncodingType] = field(
        default=None,
        metadata={
            "name": "BinaryDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    float_data_encoding: Optional[FloatDataEncodingType] = field(
        default=None,
        metadata={
            "name": "FloatDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    integer_data_encoding: Optional[IntegerDataEncodingType] = field(
        default=None,
        metadata={
            "name": "IntegerDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    string_data_encoding: Optional[StringDataEncodingType] = field(
        default=None,
        metadata={
            "name": "StringDataEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    base_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "baseType",
            "type": "Attribute",
        },
    )

    @dataclass
    class UnitSet:
        unit: list[UnitType] = field(
            default_factory=list,
            metadata={
                "name": "Unit",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )


@dataclass
class BaseTimeDataType(NameDescriptionType):
    """
    An abstract type used by within the schema to describe derive other data
    types by the ground system.

    :ivar encoding: Scale and offset are used in a y =mx +b type
        relationship (m is the scale and b is the offset) to make
        adjustments to the encoded value to that it matches the time
        units.  Binary Encoded time is typically used with a user
        supplied transform algorithm to convert time data formats that
        are too difficult to describe in XTCE.
    :ivar reference_time:
    """

    encoding: Optional["BaseTimeDataType.Encoding"] = field(
        default=None,
        metadata={
            "name": "Encoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    reference_time: Optional[ReferenceTimeType] = field(
        default=None,
        metadata={
            "name": "ReferenceTime",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class Encoding:
        binary_data_encoding: Optional[BinaryDataEncodingType] = field(
            default=None,
            metadata={
                "name": "BinaryDataEncoding",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        float_data_encoding: Optional[FloatDataEncodingType] = field(
            default=None,
            metadata={
                "name": "FloatDataEncoding",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        integer_data_encoding: Optional[IntegerDataEncodingType] = field(
            default=None,
            metadata={
                "name": "IntegerDataEncoding",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        string_data_encoding: Optional[StringDataEncodingType] = field(
            default=None,
            metadata={
                "name": "StringDataEncoding",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        units: TimeUnits = field(
            default=TimeUnits.SECONDS,
            metadata={
                "type": "Attribute",
            },
        )
        scale: float = field(
            default=1.0,
            metadata={
                "type": "Attribute",
            },
        )
        offset: float = field(
            default=0.0,
            metadata={
                "type": "Attribute",
            },
        )


@dataclass
class BinaryAlarmConditionType(AlarmType):
    """
    Alarm conditions for Binary types.
    """


@dataclass
class BooleanAlarmType(AlarmType):
    """
    Alarm conditions for Boolean types.
    """


@dataclass
class ContainerType(NameDescriptionType):
    """
    An abstract block of data; used as the base type for more specific
    container types.

    :ivar default_rate_in_stream:
    :ivar rate_in_stream_set:
    :ivar binary_encoding: May be used to indicate error detection and
        correction, change byte order,  provide the size (when it can't
        be derived), or perform some custom processing.
    """

    default_rate_in_stream: Optional[RateInStreamType] = field(
        default=None,
        metadata={
            "name": "DefaultRateInStream",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    rate_in_stream_set: Optional["ContainerType.RateInStreamSet"] = field(
        default=None,
        metadata={
            "name": "RateInStreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    binary_encoding: Optional[BinaryDataEncodingType] = field(
        default=None,
        metadata={
            "name": "BinaryEncoding",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class RateInStreamSet:
        rate_in_stream: list["ContainerType.RateInStreamSet.RateInStream"] = field(
            default_factory=list,
            metadata={
                "name": "RateInStream",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class RateInStream(RateInStreamType):
            stream_ref: Optional[str] = field(
                default=None,
                metadata={
                    "name": "streamRef",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class EnumerationAlarmType(AlarmType):
    """
    Alarm conditions for Enumerations.
    """

    enumeration_alarm_list: Optional["EnumerationAlarmType.EnumerationAlarmList"] = (
        field(
            default=None,
            metadata={
                "name": "EnumerationAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
    )
    default_alarm_level: AlarmLevels = field(
        default=AlarmLevels.NORMAL,
        metadata={
            "name": "defaultAlarmLevel",
            "type": "Attribute",
        },
    )

    @dataclass
    class EnumerationAlarmList:
        enumeration_alarm: list[
            "EnumerationAlarmType.EnumerationAlarmList.EnumerationAlarm"
        ] = field(
            default_factory=list,
            metadata={
                "name": "EnumerationAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class EnumerationAlarm:
            alarm_level: Optional[AlarmLevels] = field(
                default=None,
                metadata={
                    "name": "alarmLevel",
                    "type": "Attribute",
                    "required": True,
                },
            )
            enumeration_value: Optional[str] = field(
                default=None,
                metadata={
                    "name": "enumerationValue",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class NumericAlarmType(AlarmType):
    """
    Alarms associated with numeric data types.

    :ivar static_alarm_ranges: StaticAlarmRanges are used to trigger
        alarms when the parameter value passes some threshold value
    :ivar change_alarm_ranges: ChangeAlarmRanges are used to trigger
        alarms when the parameter value's rate-of-change is either too
        fast or too slow.   The change may be with respect to time (the
        default) or with respect to samples (delta alarms) - the
        changeType attribute determines this.  The change may also be
        ether relative (as a percentage change) or absolute as set by
        the changeBasis attribute.  The alarm also requires the
        spanOfInterest in both samples and seconds to have passed before
        it is to trigger.  For time based rate of change alarms, the
        time specified in spanOfInterestInSeconds is used to calculate
        the change.  For sample based rate of change alarms, the change
        is calulated over the number of samples specified in
        spanOfInterestInSeconds.
    """

    static_alarm_ranges: Optional[AlarmRangesType] = field(
        default=None,
        metadata={
            "name": "StaticAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    change_alarm_ranges: Optional["NumericAlarmType.ChangeAlarmRanges"] = field(
        default=None,
        metadata={
            "name": "ChangeAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class ChangeAlarmRanges(AlarmRangesType):
        change_type: ChangeAlarmRangesChangeType = field(
            default=ChangeAlarmRangesChangeType.CHANGE_PER_SECOND,
            metadata={
                "name": "changeType",
                "type": "Attribute",
            },
        )
        change_basis: ChangeAlarmRangesChangeBasis = field(
            default=ChangeAlarmRangesChangeBasis.ABSOLUTE_CHANGE,
            metadata={
                "name": "changeBasis",
                "type": "Attribute",
            },
        )
        span_of_interest_in_samples: int = field(
            default=1,
            metadata={
                "name": "spanOfInterestInSamples",
                "type": "Attribute",
            },
        )
        span_of_interest_in_seconds: Decimal = field(
            default=Decimal("0"),
            metadata={
                "name": "spanOfInterestInSeconds",
                "type": "Attribute",
            },
        )


@dataclass
class SequenceEntryType:
    """An abstract type used by sequence containers.

    An entry contains a location in the container.  The location may be
    either fixed or dynamic, absolute (to the start or end of the
    enclosing container, or relative (to either the previous or
    subsequent entry).  Entries may also repeat.

    :ivar location_in_container_in_bits: If no LocationInContainer value
        is given, the entry is assumed to begin immediately after the
        previous entry.
    :ivar repeat_entry: May be used when this entry repeats itself in
        the sequence container.  If not supplied, the entry does not
        repeat.
    :ivar include_condition: This entry will only be included in the
        sequence when this condition is true.  If no IncludeCondition is
        given, then it is will be included.  A parameter that is not
        included will be treated as if it did not exist in the sequence
        at all.
    """

    location_in_container_in_bits: Optional[
        "SequenceEntryType.LocationInContainerInBits"
    ] = field(
        default=None,
        metadata={
            "name": "LocationInContainerInBits",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    repeat_entry: Optional[RepeatType] = field(
        default=None,
        metadata={
            "name": "RepeatEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    include_condition: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "IncludeCondition",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class LocationInContainerInBits(IntegerValueType):
        """
        :ivar reference_location: The location may be relative to the
            start of the container (containerStart), relative to the end
            of the previous entry (previousEntry), relative to the end
            of the container (containerEnd), or relative to the entry
            that follows this one (nextEntry).  If going forward
            (containerStart and previousEntry) then the location refers
            to the start of the Entry.  If going backwards (containerEnd
            and nextEntry) then, the location refers to the end of the
            entry.
        """

        reference_location: LocationInContainerInBitsReferenceLocation = field(
            default=LocationInContainerInBitsReferenceLocation.PREVIOUS_ENTRY,
            metadata={
                "name": "referenceLocation",
                "type": "Attribute",
            },
        )


@dataclass
class StringAlarmType(AlarmType):
    """
    Alarm conditions for Strings.
    """

    string_alarm_list: Optional["StringAlarmType.StringAlarmList"] = field(
        default=None,
        metadata={
            "name": "StringAlarmList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    default_alarm_level: AlarmLevels = field(
        default=AlarmLevels.NORMAL,
        metadata={
            "name": "defaultAlarmLevel",
            "type": "Attribute",
        },
    )

    @dataclass
    class StringAlarmList:
        """
        :ivar string_alarm: Pattern may be a regular expression
        """

        string_alarm: list["StringAlarmType.StringAlarmList.StringAlarm"] = field(
            default_factory=list,
            metadata={
                "name": "StringAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class StringAlarm:
            alarm_level: Optional[AlarmLevels] = field(
                default=None,
                metadata={
                    "name": "alarmLevel",
                    "type": "Attribute",
                    "required": True,
                },
            )
            match_pattern: Optional[str] = field(
                default=None,
                metadata={
                    "name": "matchPattern",
                    "type": "Attribute",
                    "required": True,
                },
            )


@dataclass
class TimeAlarmConditionType(AlarmType):
    """
    Alarm conditions for Time types.
    """


@dataclass
class TimeAlarmType(AlarmType):
    """
    Alarms associated with time data types.

    :ivar static_alarm_ranges: StaticAlarmRanges are used to trigger
        alarms when the parameter value passes some threshold value
    :ivar change_per_second_alarm_ranges: ChangePerSecondAlarmRanges are
        used to trigger alarms when the parameter value's rate-of-change
        passes some threshold value.  An alarm condition that triggers
        when the value changes too fast (or too slow)
    """

    static_alarm_ranges: Optional["TimeAlarmType.StaticAlarmRanges"] = field(
        default=None,
        metadata={
            "name": "StaticAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    change_per_second_alarm_ranges: Optional[
        "TimeAlarmType.ChangePerSecondAlarmRanges"
    ] = field(
        default=None,
        metadata={
            "name": "ChangePerSecondAlarmRanges",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class StaticAlarmRanges(AlarmRangesType):
        time_units: TimeUnits = field(
            default=TimeUnits.SECONDS,
            metadata={
                "name": "timeUnits",
                "type": "Attribute",
            },
        )

    @dataclass
    class ChangePerSecondAlarmRanges(AlarmRangesType):
        time_units: TimeUnits = field(
            default=TimeUnits.SECONDS,
            metadata={
                "name": "timeUnits",
                "type": "Attribute",
            },
        )


@dataclass
class AbsoluteTimeDataType(BaseTimeDataType):
    """Used to contain an absolute time.

    Contains an absolute (to a known epoch) time.  Use the [ISO 8601] extended format CCYY-MM-DDThh:mm:ss where "CC" represents the century, "YY" the year, "MM" the month and "DD" the day, preceded by an optional leading "-" sign to indicate a negative number. If the sign is omitted, "+" is assumed. The letter "T" is the date/time separator and "hh", "mm", "ss" represent hour, minute and second respectively. Additional digits can be used to increase the precision of fractional seconds if desired i.e. the format ss.ss... with any number of digits after the decimal point is supported.
    """

    initial_value: Optional[XmlDateTime] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass
class ArrayParameterRefEntryType(SequenceEntryType):
    """An entry that is an array parameter.

    This entry is somewhat special because the entry may represent only
    a part of the Array and it's important to describe which dimensions
    of the array come first in the sequence as well as the size of the
    array.

    :ivar dimension_list: Where the Dimension list is in this form:
        Array[1stDim][2ndDim][lastDim].  The last dimension is assumed
        to be the least significant - that is this dimension will cycle
        through its combination before the next to last dimension
        changes.  The order MUST ascend or the array will need to be
        broken out entry by entry.
    :ivar parameter_ref:
    :ivar last_entry_for_this_array_instance:
    """

    dimension_list: Optional["ArrayParameterRefEntryType.DimensionList"] = field(
        default=None,
        metadata={
            "name": "DimensionList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    parameter_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
        },
    )
    last_entry_for_this_array_instance: bool = field(
        default=False,
        metadata={
            "name": "lastEntryForThisArrayInstance",
            "type": "Attribute",
        },
    )

    @dataclass
    class DimensionList:
        """
        :ivar dimension: For partial entries of an array, the starting
            and ending index for each dimension, OR the Size must be
            specified.  Indexes are zero based.
        """

        dimension: list["ArrayParameterRefEntryType.DimensionList.Dimension"] = field(
            default_factory=list,
            metadata={
                "name": "Dimension",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Dimension:
            """
            :ivar starting_index: zero based index
            :ivar ending_index:
            """

            starting_index: Optional[IntegerValueType] = field(
                default=None,
                metadata={
                    "name": "StartingIndex",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )
            ending_index: Optional[IntegerValueType] = field(
                default=None,
                metadata={
                    "name": "EndingIndex",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )


@dataclass
class BinaryDataType(BaseDataType):
    """
    Contains an arbitrarily large binary value.

    :ivar initial_value: Extra bits are truncated from the MSB
        (leftmost)
    """

    initial_value: Optional[bytes] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
            "format": "base16",
        },
    )


@dataclass
class BooleanDataType(BaseDataType):
    """
    Contains a boolean value.

    :ivar initial_value: Initial value is always given in calibrated
        form.
    :ivar one_string_value:
    :ivar zero_string_value:
    """

    initial_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    one_string_value: str = field(
        default="True",
        metadata={
            "name": "oneStringValue",
            "type": "Attribute",
        },
    )
    zero_string_value: str = field(
        default="False",
        metadata={
            "name": "zeroStringValue",
            "type": "Attribute",
        },
    )


@dataclass
class ContainerRefEntryType(SequenceEntryType):
    """
    An entry that is simply a reference to another container.
    """

    container_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ContainerSegmentRefEntryType(SequenceEntryType):
    """An entry that is only a portion of a container indicating that the
    entire container must be assembled from other container segments.

    It is assumed that container segments happen sequentially in time,
    that is the first part of a container is first, however (and there's
    always a however), if this is not the case the order of this
    container segment may be supplied with the order attribute where the
    first segment order="0".  Each instance of a container cannot
    overlap in the overall sequence with another instance
    """

    container_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "containerRef",
            "type": "Attribute",
            "required": True,
        },
    )
    order: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: Optional[int] = field(
        default=None,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class EnumeratedDataType(BaseDataType):
    """Contains an enumerated value - a value that has both an integral and a string representation.

    :ivar enumeration_list:
    :ivar initial_value: Initial value is always given in calibrated
        form.
    """

    enumeration_list: Optional["EnumeratedDataType.EnumerationList"] = field(
        default=None,
        metadata={
            "name": "EnumerationList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    initial_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )

    @dataclass
    class EnumerationList:
        enumeration: list[ValueEnumerationType] = field(
            default_factory=list,
            metadata={
                "name": "Enumeration",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class IndirectParameterRefEntryType(SequenceEntryType):
    """An entry whose name is given by the value of a ParamameterInstance.

    This entry may be used to implement dwell telemetry streams.  The
    value of the parameter in ParameterInstance must use either the name
    of the Parameter or its alias.  If it's an alias name, the alias
    namespace is supplied as an attribute.
    """

    parameter_instance: Optional[ParameterInstanceRefType] = field(
        default=None,
        metadata={
            "name": "ParameterInstance",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    alias_name_space: Optional[str] = field(
        default=None,
        metadata={
            "name": "aliasNameSpace",
            "type": "Attribute",
        },
    )


@dataclass
class NumericContextAlarmType(NumericAlarmType):
    """Context alarms are applied when the ContextMatch is true.

    Context alarms override Default alarms
    """

    context_match: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )


@dataclass
class NumericDataType(BaseDataType):
    """
    An abstract type that is a super type of either an Integer or Float Data
    type.
    """

    to_string: Optional[NumberToStringType] = field(
        default=None,
        metadata={
            "name": "ToString",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    valid_range_applies_to_calibrated: bool = field(
        default=True,
        metadata={
            "name": "validRangeAppliesToCalibrated",
            "type": "Attribute",
        },
    )


@dataclass
class ParameterRefEntryType(SequenceEntryType):
    """
    An entry that is a single Parameter.
    """

    parameter_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class ParameterSegmentRefEntryType(SequenceEntryType):
    """An entry that is only a portion of a parameter value indicating that
    the entire parameter value must be assembled from other parameter
    segments.

    It is assumed that parameter segments happen sequentially in time,
    that is the first part if a telemetry parameter first, however (and
    there's always a however), if this is not the case the order of this
    parameter segment may be supplied with the order attribute where the
    first segment order="0".
    """

    parameter_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "parameterRef",
            "type": "Attribute",
            "required": True,
        },
    )
    order: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: Optional[int] = field(
        default=None,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class RelativeTimeDataType(BaseTimeDataType):
    """Used to contain a relative time value.

    Used to describe a relative time.  Normally used for time offsets.
    A Relative time is expressed as PnYn MnDTnH nMnS, where nY
    represents the number of years, nM the number of months, nD the
    number of days, 'T' is the date/time separator, nH the number of
    hours, nM the number of minutes and nS the number of seconds. The
    number of seconds can include decimal digits to arbitrary precision.
    For example, to indicate a duration of 1 year, 2 months, 3 days, 10
    hours, and 30 minutes, one would write: P1Y2M3DT10H30M. One could
    also indicate a duration of minus 120 days as: -P120D.  An extension
    of Schema duration type.
    """

    initial_value: Optional[XmlDuration] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )


@dataclass
class StreamSegmentEntryType(SequenceEntryType):
    """
    An entry that is a portion of a stream (streams are by definition,
    assumed continuous)   It is assumed that stream segments happen
    sequentially in time, that is the first part if a steam first, however,
    if this is not the case the order of the stream segments may be supplied
    with the order attribute where the first segment order="0".
    """

    stream_ref: Optional[str] = field(
        default=None,
        metadata={
            "name": "streamRef",
            "type": "Attribute",
            "required": True,
        },
    )
    order: Optional[int] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    size_in_bits: Optional[int] = field(
        default=None,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
            "required": True,
        },
    )


@dataclass
class StringDataType(BaseDataType):
    """
    Contains a String Value.

    :ivar size_range_in_characters:
    :ivar initial_value: Initial values for string types, may include C
        language style (\\n, \\t, \\", \\\\, etc.) escape sequences.
    :ivar restriction_pattern: restriction pattern is a regular
        expression
    :ivar character_width:
    """

    size_range_in_characters: Optional[IntegerRangeType] = field(
        default=None,
        metadata={
            "name": "SizeRangeInCharacters",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    initial_value: Optional[str] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    restriction_pattern: Optional[str] = field(
        default=None,
        metadata={
            "name": "restrictionPattern",
            "type": "Attribute",
        },
    )
    character_width: Optional[StringDataTypeCharacterWidth] = field(
        default=None,
        metadata={
            "name": "characterWidth",
            "type": "Attribute",
        },
    )


@dataclass
class TimeContextAlarmType(TimeAlarmType):
    """Context alarms are applied when the ContextMatch is true.

    Context alarms override Default alarms
    """

    context_match: Optional[MatchCriteriaType] = field(
        default=None,
        metadata={
            "name": "ContextMatch",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )


@dataclass
class CommandContainerEntryListType:
    """Similar to an EntryList type but also may include command arguments or -as a convenience - fixed value entries."""

    parameter_ref_entry: list[ParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_segment_ref_entry: list[ParameterSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_ref_entry: list[ContainerRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_segment_ref_entry: list[ContainerSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    stream_segment_entry: list[StreamSegmentEntryType] = field(
        default_factory=list,
        metadata={
            "name": "StreamSegmentEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    indirect_parameter_ref_entry: list[IndirectParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "IndirectParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    array_parameter_ref_entry: list[ArrayParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    argument_ref_entry: list["CommandContainerEntryListType.ArgumentRefEntry"] = field(
        default_factory=list,
        metadata={
            "name": "ArgumentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    array_argument_ref_entry: list[ArrayParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayArgumentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    fixed_value_entry: list["CommandContainerEntryListType.FixedValueEntry"] = field(
        default_factory=list,
        metadata={
            "name": "FixedValueEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class ArgumentRefEntry(SequenceEntryType):
        argument_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "argumentRef",
                "type": "Attribute",
                "required": True,
            },
        )

    @dataclass
    class FixedValueEntry(SequenceEntryType):
        binary_value: Optional[bytes] = field(
            default=None,
            metadata={
                "name": "binaryValue",
                "type": "Attribute",
                "required": True,
                "format": "base16",
            },
        )
        size_in_bits: Optional[int] = field(
            default=None,
            metadata={
                "name": "sizeInBits",
                "type": "Attribute",
            },
        )


@dataclass
class EntryListType:
    """Contains an ordered list of Entries.

    Used in Sequence Container
    """

    parameter_ref_entry: list[ParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_segment_ref_entry: list[ParameterSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ParameterSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_ref_entry: list[ContainerRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_segment_ref_entry: list[ContainerSegmentRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ContainerSegmentRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    stream_segment_entry: list[StreamSegmentEntryType] = field(
        default_factory=list,
        metadata={
            "name": "StreamSegmentEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    indirect_parameter_ref_entry: list[IndirectParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "IndirectParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    array_parameter_ref_entry: list[ArrayParameterRefEntryType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterRefEntry",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )


@dataclass
class FloatDataType(NumericDataType):
    """
    Contains a floating point value.

    :ivar valid_range: The Valid Range bounds the universe of possible
        values this Parameter may have.
    :ivar initial_value: Initial value is always given in calibrated
        form
    :ivar size_in_bits:
    """

    valid_range: Optional[FloatRangeType] = field(
        default=None,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    initial_value: Optional[float] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
        },
    )
    size_in_bits: FloatDataTypeSizeInBits = field(
        default=FloatDataTypeSizeInBits.VALUE_32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )


@dataclass
class IntegerDataType(NumericDataType):
    """
    Contains an integral value.

    :ivar valid_range: The Valid Range bounds the universe of possible
        values this Parameter may have.
    :ivar initial_value: Initial value is always given in calibrated
        form.  Default is base 10 form; binary, octal, or hexadecimal
        values may be given by preceding value with 0[b|B], 0[o|O|,
        0[x|X] respectively.
    :ivar size_in_bits:
    :ivar signed:
    """

    valid_range: Optional[IntegerRangeType] = field(
        default=None,
        metadata={
            "name": "ValidRange",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    initial_value: Optional[Union[int, str]] = field(
        default=None,
        metadata={
            "name": "initialValue",
            "type": "Attribute",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )
    size_in_bits: int = field(
        default=32,
        metadata={
            "name": "sizeInBits",
            "type": "Attribute",
        },
    )
    signed: bool = field(
        default=True,
        metadata={
            "type": "Attribute",
        },
    )


@dataclass
class ArgumentTypeSetType:
    """
    Holds the list of argument type definitions.
    """

    string_argument_type: list[StringDataType] = field(
        default_factory=list,
        metadata={
            "name": "StringArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    enumerated_argument_type: list[EnumeratedDataType] = field(
        default_factory=list,
        metadata={
            "name": "EnumeratedArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    integer_argument_type: list["ArgumentTypeSetType.IntegerArgumentType"] = field(
        default_factory=list,
        metadata={
            "name": "IntegerArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    binary_argument_type: list[BinaryDataType] = field(
        default_factory=list,
        metadata={
            "name": "BinaryArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    float_argument_type: list["ArgumentTypeSetType.FloatArgumentType"] = field(
        default_factory=list,
        metadata={
            "name": "FloatArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    boolean_argument_type: list[BooleanDataType] = field(
        default_factory=list,
        metadata={
            "name": "BooleanArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    relative_time_agument_type: list[RelativeTimeDataType] = field(
        default_factory=list,
        metadata={
            "name": "RelativeTimeAgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    absolute_time_argument_type: list[AbsoluteTimeDataType] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteTimeArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    array_argument_type: list[ArrayDataTypeType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    aggregate_argument_type: list[AggregateDataType] = field(
        default_factory=list,
        metadata={
            "name": "AggregateArgumentType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class IntegerArgumentType(IntegerDataType):
        """
        :ivar valid_range_set: Numerical ranges that define the universe
            of valid values for this argument.  Used to further bound
            argument values inside the ValidRange for the overall Data
            Type
        """

        valid_range_set: Optional[
            "ArgumentTypeSetType.IntegerArgumentType.ValidRangeSet"
        ] = field(
            default=None,
            metadata={
                "name": "ValidRangeSet",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ValidRangeSet:
            valid_range: list[IntegerRangeType] = field(
                default_factory=list,
                metadata={
                    "name": "ValidRange",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )
            valid_range_applies_to_calibrated: bool = field(
                default=True,
                metadata={
                    "name": "validRangeAppliesToCalibrated",
                    "type": "Attribute",
                },
            )

    @dataclass
    class FloatArgumentType(FloatDataType):
        """
        :ivar valid_range_set: Numerical ranges that define the universe
            of valid values for this argument.  Used to further bound
            argument values inside the ValidRange for the overall Data
            Type
        """

        valid_range_set: Optional[
            "ArgumentTypeSetType.FloatArgumentType.ValidRangeSet"
        ] = field(
            default=None,
            metadata={
                "name": "ValidRangeSet",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ValidRangeSet:
            valid_range: list[FloatRangeType] = field(
                default_factory=list,
                metadata={
                    "name": "ValidRange",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )
            valid_range_applies_to_calibrated: bool = field(
                default=True,
                metadata={
                    "name": "validRangeAppliesToCalibrated",
                    "type": "Attribute",
                },
            )


@dataclass
class CommandContainerType(ContainerType):
    """The Key = Command Op Code.

    Each MetaCommand may have one CommandContainer.  The sequence may
    now contain command fields
    """

    entry_list: Optional[CommandContainerEntryListType] = field(
        default=None,
        metadata={
            "name": "EntryList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    base_container: Optional["CommandContainerType.BaseContainer"] = field(
        default=None,
        metadata={
            "name": "BaseContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class BaseContainer:
        """
        :ivar restriction_criteria: Given that this Container is the
            Base container type, RestrictionCriteria lists conditions
            that must be true for this Container to be 'this'
            subContainer type.  May be a simple Comparison List, a
            Boolean Expression, and/or in a Graph of containers
            established by the NextContainer
        :ivar container_ref:
        """

        restriction_criteria: Optional[
            "CommandContainerType.BaseContainer.RestrictionCriteria"
        ] = field(
            default=None,
            metadata={
                "name": "RestrictionCriteria",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        container_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "containerRef",
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class RestrictionCriteria(MatchCriteriaType):
            next_container: Optional[ContainerRefType] = field(
                default=None,
                metadata={
                    "name": "NextContainer",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )


@dataclass
class ParameterTypeSetType:
    """Holds the list of parameter type definitions.

    A Parameter is a description of something that can have a value; it
    is not the value itself.

    :ivar string_parameter_type:
    :ivar enumerated_parameter_type:
    :ivar integer_parameter_type:
    :ivar binary_parameter_type:
    :ivar float_parameter_type:
    :ivar boolean_parameter_type:
    :ivar relative_time_parameter_type:
    :ivar absolute_time_parameter_type:
    :ivar array_parameter_type: An array type.  Will be an array of
        parameters of the type referenced in 'arrayTypeRef' and have the
        number of array dimensions as specified in 'numberOfDimensions'
    :ivar aggregate_parameter_type: AggegateParameters are analogous to
        a C struc, they are an aggregation of related data items.  Each
        of these data items is defined here as a 'Member'
    """

    string_parameter_type: list["ParameterTypeSetType.StringParameterType"] = field(
        default_factory=list,
        metadata={
            "name": "StringParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    enumerated_parameter_type: list["ParameterTypeSetType.EnumeratedParameterType"] = (
        field(
            default_factory=list,
            metadata={
                "name": "EnumeratedParameterType",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    integer_parameter_type: list["ParameterTypeSetType.IntegerParameterType"] = field(
        default_factory=list,
        metadata={
            "name": "IntegerParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    binary_parameter_type: list["ParameterTypeSetType.BinaryParameterType"] = field(
        default_factory=list,
        metadata={
            "name": "BinaryParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    float_parameter_type: list["ParameterTypeSetType.FloatParameterType"] = field(
        default_factory=list,
        metadata={
            "name": "FloatParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    boolean_parameter_type: list["ParameterTypeSetType.BooleanParameterType"] = field(
        default_factory=list,
        metadata={
            "name": "BooleanParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    relative_time_parameter_type: list[
        "ParameterTypeSetType.RelativeTimeParameterType"
    ] = field(
        default_factory=list,
        metadata={
            "name": "RelativeTimeParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    absolute_time_parameter_type: list[AbsoluteTimeDataType] = field(
        default_factory=list,
        metadata={
            "name": "AbsoluteTimeParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    array_parameter_type: list[ArrayDataTypeType] = field(
        default_factory=list,
        metadata={
            "name": "ArrayParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    aggregate_parameter_type: list[AggregateDataType] = field(
        default_factory=list,
        metadata={
            "name": "AggregateParameterType",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class StringParameterType(StringDataType):
        default_alarm: Optional[StringAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.StringParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[
                "ParameterTypeSetType.StringParameterType.ContextAlarmList.ContextAlarm"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class ContextAlarm(StringAlarmType):
                context_match: Optional[MatchCriteriaType] = field(
                    default=None,
                    metadata={
                        "name": "ContextMatch",
                        "type": "Element",
                        "namespace": "http://www.omg.org/space/xtce",
                        "required": True,
                    },
                )

    @dataclass
    class EnumeratedParameterType(EnumeratedDataType):
        default_alarm: Optional[EnumerationAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.EnumeratedParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: Optional[
                "ParameterTypeSetType.EnumeratedParameterType.ContextAlarmList.ContextAlarm"
            ] = field(
                default=None,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )

            @dataclass
            class ContextAlarm(EnumerationAlarmType):
                context_match: Optional[MatchCriteriaType] = field(
                    default=None,
                    metadata={
                        "name": "ContextMatch",
                        "type": "Element",
                        "namespace": "http://www.omg.org/space/xtce",
                        "required": True,
                    },
                )

    @dataclass
    class IntegerParameterType(IntegerDataType):
        default_alarm: Optional[NumericAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.IntegerParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[NumericContextAlarmType] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

    @dataclass
    class BinaryParameterType(BinaryDataType):
        default_alarm: Optional[AlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.BinaryParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[
                "ParameterTypeSetType.BinaryParameterType.ContextAlarmList.ContextAlarm"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class ContextAlarm(AlarmType):
                context_match: Optional[MatchCriteriaType] = field(
                    default=None,
                    metadata={
                        "name": "ContextMatch",
                        "type": "Element",
                        "namespace": "http://www.omg.org/space/xtce",
                        "required": True,
                    },
                )

    @dataclass
    class FloatParameterType(FloatDataType):
        default_alarm: Optional[NumericAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.FloatParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[NumericContextAlarmType] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

    @dataclass
    class BooleanParameterType(BooleanDataType):
        default_alarm: Optional[BooleanAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.BooleanParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[
                "ParameterTypeSetType.BooleanParameterType.ContextAlarmList.ContextAlarm"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class ContextAlarm(BooleanAlarmType):
                context_match: Optional[MatchCriteriaType] = field(
                    default=None,
                    metadata={
                        "name": "ContextMatch",
                        "type": "Element",
                        "namespace": "http://www.omg.org/space/xtce",
                        "required": True,
                    },
                )

    @dataclass
    class RelativeTimeParameterType(RelativeTimeDataType):
        default_alarm: Optional[TimeAlarmType] = field(
            default=None,
            metadata={
                "name": "DefaultAlarm",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        context_alarm_list: Optional[
            "ParameterTypeSetType.RelativeTimeParameterType.ContextAlarmList"
        ] = field(
            default=None,
            metadata={
                "name": "ContextAlarmList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ContextAlarmList:
            context_alarm: list[TimeContextAlarmType] = field(
                default_factory=list,
                metadata={
                    "name": "ContextAlarm",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )


@dataclass
class SequenceContainerType(ContainerType):
    """A list of raw parameters, parameter segments, stream segments,
    containers, or container segments.

    Sequence containers may inherit from other sequence containers; when
    they do, the sequence in the parent SequenceContainer is 'inherited'
    and if the location of entries in the child sequence is not
    specified, it is assumed to start where the parent sequence ended.
    Parent sequence containers may be marked as "abstract".  The idle
    pattern is part of any unallocated space in the Container.
    """

    entry_list: Optional[EntryListType] = field(
        default=None,
        metadata={
            "name": "EntryList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    base_container: Optional["SequenceContainerType.BaseContainer"] = field(
        default=None,
        metadata={
            "name": "BaseContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    abstract: Optional[bool] = field(
        default=None,
        metadata={
            "type": "Attribute",
        },
    )
    idle_pattern: Union[int, str] = field(
        default="0x0",
        metadata={
            "name": "idlePattern",
            "type": "Attribute",
            "pattern": r"0[xX][0-9a-fA-F]+",
        },
    )

    @dataclass
    class BaseContainer:
        """
        :ivar restriction_criteria: Given that this Container is the
            Base container type, RestrictionCriteria lists conditions
            that must be true for this Container to be 'this'
            subContainer type.  May be a simple Comparison List, a
            Boolean Expression, and/or in a Graph of containers
            established by the NextContainer
        :ivar container_ref:
        """

        restriction_criteria: Optional[
            "SequenceContainerType.BaseContainer.RestrictionCriteria"
        ] = field(
            default=None,
            metadata={
                "name": "RestrictionCriteria",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "required": True,
            },
        )
        container_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "containerRef",
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class RestrictionCriteria(MatchCriteriaType):
            next_container: Optional[ContainerRefType] = field(
                default=None,
                metadata={
                    "name": "NextContainer",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )


@dataclass
class CommandContainerSetType:
    """
    Contains an unordered Set of Command Containers.
    """

    command_container: list[SequenceContainerType] = field(
        default_factory=list,
        metadata={
            "name": "CommandContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 1,
        },
    )


@dataclass
class ContainerSetType:
    """
    Unordered Set of Containers.

    :ivar sequence_container: SequenceContainers define sequences of
        parameters or other containers.
    """

    sequence_container: list[SequenceContainerType] = field(
        default_factory=list,
        metadata={
            "name": "SequenceContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "min_occurs": 1,
        },
    )


@dataclass
class MetaCommandType(NameDescriptionType):
    """
    A type definition used as the base type for a CommandDefinition.

    :ivar base_meta_command: The MetaCommand is derived from this Base.
        Arguments of the base MetaCommand are further specified.
    :ivar system_name: Optional.  Normally used when the database is
        built in a flat, non-hierarchical format
    :ivar argument_list: Many commands have one or more options.  These
        are called command arguments.  Command arguments may be of any
        of the standard data types.  MetaCommand arguments are local to
        the MetaCommand.
    :ivar command_container: Tells how to package this command
    :ivar transmission_constraint_list: Appended to the
        TramsmissionConstraint List of the base command.  Constraints
        are checked in order.
    :ivar default_significance: Some Command and Control Systems may
        require special user access or confirmations before transmitting
        commands with certain levels.  The level is inherited from the
        Base MetaCommand.
    :ivar context_significance_list: Used when the significance
        (possible consequence) of a command varies by the operating
        context
    :ivar interlock: An Interlock is a type of Constraint, but not on
        Command instances of this MetaCommand; Interlocks apply instead
        to the next command.  An Interlock will block successive
        commands until this command has reached a certain stage (through
        verifications).  Interlocks are scoped to a SpaceSystem basis.
    :ivar verifier_set: A Command Verifier is a conditional check on the
        telemetry from a SpaceSystem that that provides positive
        indication on the processing state of a command.  There are
        eight different verifiers each associated with difference states
        in command processing: TransferredToRange, TransferredFromRange,
        Received, Accepted, Queued, Execution, Complete, and Failed.
        There may be multiple ‘complete’ verifiers. ‘Complete’ verifiers
        are added to the Base MetaCommand ‘Complete’ verifier list.  All
        others will overide a verifier defined in a Base MetaCommand.
    :ivar parameter_to_set_list: Parameters that are set with a new
        value after the command has been sent.  Appended to the Base
        Command list
    :ivar parameters_to_suspend_alarms_on_set: Sometimes it is necessary
        to suspend alarms - particularly 'change' alarms for commands
        that will change the value of a Parameter
    :ivar abstract:
    """

    base_meta_command: Optional["MetaCommandType.BaseMetaCommand"] = field(
        default=None,
        metadata={
            "name": "BaseMetaCommand",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    system_name: Optional[str] = field(
        default=None,
        metadata={
            "name": "SystemName",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    argument_list: Optional["MetaCommandType.ArgumentList"] = field(
        default=None,
        metadata={
            "name": "ArgumentList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    command_container: Optional[CommandContainerType] = field(
        default=None,
        metadata={
            "name": "CommandContainer",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    transmission_constraint_list: Optional[
        "MetaCommandType.TransmissionConstraintList"
    ] = field(
        default=None,
        metadata={
            "name": "TransmissionConstraintList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    default_significance: Optional[SignificanceType] = field(
        default=None,
        metadata={
            "name": "DefaultSignificance",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    context_significance_list: Optional["MetaCommandType.ContextSignificanceList"] = (
        field(
            default=None,
            metadata={
                "name": "ContextSignificanceList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
    )
    interlock: Optional["MetaCommandType.Interlock"] = field(
        default=None,
        metadata={
            "name": "Interlock",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    verifier_set: Optional["MetaCommandType.VerifierSet"] = field(
        default=None,
        metadata={
            "name": "VerifierSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_to_set_list: Optional["MetaCommandType.ParameterToSetList"] = field(
        default=None,
        metadata={
            "name": "ParameterToSetList",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameters_to_suspend_alarms_on_set: Optional[
        "MetaCommandType.ParametersToSuspendAlarmsOnSet"
    ] = field(
        default=None,
        metadata={
            "name": "ParametersToSuspendAlarmsOnSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    abstract: bool = field(
        default=False,
        metadata={
            "type": "Attribute",
        },
    )

    @dataclass
    class BaseMetaCommand:
        argument_assignment_list: Optional[
            "MetaCommandType.BaseMetaCommand.ArgumentAssignmentList"
        ] = field(
            default=None,
            metadata={
                "name": "ArgumentAssignmentList",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        meta_command_ref: Optional[str] = field(
            default=None,
            metadata={
                "name": "metaCommandRef",
                "type": "Attribute",
                "required": True,
            },
        )

        @dataclass
        class ArgumentAssignmentList:
            argument_assignment: list[
                "MetaCommandType.BaseMetaCommand.ArgumentAssignmentList.ArgumentAssignment"
            ] = field(
                default_factory=list,
                metadata={
                    "name": "ArgumentAssignment",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )

            @dataclass
            class ArgumentAssignment:
                argument_name: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "argumentName",
                        "type": "Attribute",
                        "required": True,
                    },
                )
                argument_value: Optional[str] = field(
                    default=None,
                    metadata={
                        "name": "argumentValue",
                        "type": "Attribute",
                        "required": True,
                    },
                )

    @dataclass
    class ArgumentList:
        argument: list["MetaCommandType.ArgumentList.Argument"] = field(
            default_factory=list,
            metadata={
                "name": "Argument",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class Argument(NameDescriptionType):
            """
            :ivar argument_type_ref:
            :ivar initial_value: Used to set the initial calibrated
                values of Arguments.  Will overwrite an initial value
                defined for the ArgumentType.  For integer types base 10
                (decimal) form is assumed unless: if proceeded by a 0b
                or 0B, value is in base two (binary form, if proceeded
                by a 0o or 0O, values is in base 8 (octal) form, or if
                proceeded by a 0x or 0X, value is in base 16 (hex) form.
                Floating point types may be specified in normal (100.0)
                or scientific (1.0e2) form.  Time types are specified
                using the ISO 8601 formats described for XTCE time data
                types.  Initial values for string types, may include C
                language style (\\n, \\t, \\", \\\\, etc.) escape
                sequences.  Initial values for Array or Aggregate types
                may not be set.
            """

            argument_type_ref: Optional[str] = field(
                default=None,
                metadata={
                    "name": "argumentTypeRef",
                    "type": "Attribute",
                    "required": True,
                },
            )
            initial_value: Optional[str] = field(
                default=None,
                metadata={
                    "name": "initialValue",
                    "type": "Attribute",
                },
            )

    @dataclass
    class TransmissionConstraintList:
        """
        :ivar transmission_constraint: A CommandTransmission constraint
            is used to check that the command can be run in the current
            operating mode and may block the transmission of the command
            if the constraint condition is true.
        """

        transmission_constraint: list[
            "MetaCommandType.TransmissionConstraintList.TransmissionConstraint"
        ] = field(
            default_factory=list,
            metadata={
                "name": "TransmissionConstraint",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class TransmissionConstraint(MatchCriteriaType):
            """
            :ivar time_out: Pause during timeOut, fail when the timeout
                passes
            :ivar suspendable: Indicates whether the constraints for a
                Command may be suspended.
            """

            time_out: Optional[XmlDuration] = field(
                default=None,
                metadata={
                    "name": "timeOut",
                    "type": "Attribute",
                },
            )
            suspendable: bool = field(
                default=False,
                metadata={
                    "type": "Attribute",
                },
            )

    @dataclass
    class ContextSignificanceList:
        context_significance: list[
            "MetaCommandType.ContextSignificanceList.ContextSignificance"
        ] = field(
            default_factory=list,
            metadata={
                "name": "ContextSignificance",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class ContextSignificance:
            context_match: Optional[MatchCriteriaType] = field(
                default=None,
                metadata={
                    "name": "ContextMatch",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )
            significance: Optional[SignificanceType] = field(
                default=None,
                metadata={
                    "name": "Significance",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )

    @dataclass
    class Interlock:
        """
        :ivar scope_to_space_system: The name of a SpaceSystem this
            Interlock applies to.  By default, it only applies to the
            SpaceSystem that contains this MetaCommand.
        :ivar verification_to_wait_for:
        :ivar verification_progress_percentage: Only applies when the
            verificationToWaitFor attribute is 'queued' or 'executing'.
        :ivar suspendable: A flag that indicates that under special
            circumstances, this Interlock can be suspended.
        """

        scope_to_space_system: Optional[str] = field(
            default=None,
            metadata={
                "name": "scopeToSpaceSystem",
                "type": "Attribute",
            },
        )
        verification_to_wait_for: VerifierEnumerationType = field(
            default=VerifierEnumerationType.COMPLETE,
            metadata={
                "name": "verificationToWaitFor",
                "type": "Attribute",
            },
        )
        verification_progress_percentage: Optional[Decimal] = field(
            default=None,
            metadata={
                "name": "verificationProgressPercentage",
                "type": "Attribute",
            },
        )
        suspendable: bool = field(
            default=False,
            metadata={
                "type": "Attribute",
            },
        )

    @dataclass
    class VerifierSet:
        """
        :ivar transferred_to_range_verifier: Transferred to range means
            the command has been received to the network that connects
            the ground system to the spacecraft.  Obviously, this
            verifier must come from something other than the spacecraft.
        :ivar sent_from_range_verifier: Sent from range means the
            command has been transmitted to the spacecraft by the
            network that connects the ground system to the spacecraft.
            Obviously, this verifier must come from something other than
            the spacecraft.
        :ivar received_verifier: A verifier that simply means the
            SpaceSystem has received the command.
        :ivar accepted_verifier: A verifier that means the SpaceSystem
            has accepted the command
        :ivar queued_verifier: A verifer that means the command is
            scheduled for execution by the SpaceSystem.
        :ivar execution_verifier: A verifier that indicates that the
            command is being executed.  An optional Element indicates
            how far along the command has progressed either as a fixed
            value or an (possibly scaled) ParameterInstance value.
        :ivar complete_verifier: A possible set of verifiers that all
            must be true for the command be considered completed.
        :ivar failed_verifier: When true, indicates that the command
            failed.  timeToWait is how long to wait for the
            FailedVerifier to test true.
        """

        transferred_to_range_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "TransferredToRangeVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        sent_from_range_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "SentFromRangeVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        received_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "ReceivedVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        accepted_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "AcceptedVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        queued_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "QueuedVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        execution_verifier: Optional[
            "MetaCommandType.VerifierSet.ExecutionVerifier"
        ] = field(
            default=None,
            metadata={
                "name": "ExecutionVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        complete_verifier: list["MetaCommandType.VerifierSet.CompleteVerifier"] = field(
            default_factory=list,
            metadata={
                "name": "CompleteVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        failed_verifier: Optional[CommandVerifierType] = field(
            default=None,
            metadata={
                "name": "FailedVerifier",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class ExecutionVerifier(CommandVerifierType):
            percent_complete: Optional[DecimalValueType] = field(
                default=None,
                metadata={
                    "name": "PercentComplete",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )

        @dataclass
        class CompleteVerifier(CommandVerifierType):
            return_parm_ref: Optional[ParameterRefType] = field(
                default=None,
                metadata={
                    "name": "ReturnParmRef",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )

    @dataclass
    class ParameterToSetList:
        """
        :ivar parameter_to_set: Sets a Parameter to a new value (either
            from a derivation or explicitly) after the command has been
            verified (all verifications have passed)
        """

        parameter_to_set: list["MetaCommandType.ParameterToSetList.ParameterToSet"] = (
            field(
                default_factory=list,
                metadata={
                    "name": "ParameterToSet",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "min_occurs": 1,
                },
            )
        )

        @dataclass
        class ParameterToSet(ParameterRefType):
            """
            :ivar derivation: Result of the MathOperation will be the
                new Parameter value
            :ivar new_value:
            :ivar set_on_verification:
            """

            derivation: Optional[MathOperationType] = field(
                default=None,
                metadata={
                    "name": "Derivation",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )
            new_value: Optional[str] = field(
                default=None,
                metadata={
                    "name": "NewValue",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                },
            )
            set_on_verification: VerifierEnumerationType = field(
                default=VerifierEnumerationType.COMPLETE,
                metadata={
                    "name": "setOnVerification",
                    "type": "Attribute",
                },
            )

    @dataclass
    class ParametersToSuspendAlarmsOnSet:
        """
        :ivar parameter_to_suspend_alarms_on: Will suspend all Alarms
            associated with this Parameter for the given suspense time
            after the given verifier
        """

        parameter_to_suspend_alarms_on: list[
            "MetaCommandType.ParametersToSuspendAlarmsOnSet.ParameterToSuspendAlarmsOn"
        ] = field(
            default_factory=list,
            metadata={
                "name": "ParameterToSuspendAlarmsOn",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )

        @dataclass
        class ParameterToSuspendAlarmsOn(ParameterRefType):
            suspense_time: Optional[XmlDuration] = field(
                default=None,
                metadata={
                    "name": "suspenseTime",
                    "type": "Attribute",
                    "required": True,
                },
            )
            verifier_to_trigger_on: VerifierEnumerationType = field(
                default=VerifierEnumerationType.RELEASE,
                metadata={
                    "name": "verifierToTriggerOn",
                    "type": "Attribute",
                },
            )


@dataclass
class CommandMetaDataType:
    """
    Command Meta Data contains information about commands.

    :ivar parameter_type_set: A list of parameter types
    :ivar parameter_set: Parameters referenced by MetaCommands.  This
        Parameter Set is located here so that MetaCommand data can be
        built independently of TelemetryMetaData.
    :ivar argument_type_set:
    :ivar meta_command_set: A set of Command Definitions
    :ivar command_container_set: The Command Container defines the
        construction of a Command.
    :ivar stream_set:
    :ivar algorithm_set:
    """

    parameter_type_set: Optional[ParameterTypeSetType] = field(
        default=None,
        metadata={
            "name": "ParameterTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_set: Optional[ParameterSetType] = field(
        default=None,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    argument_type_set: Optional[ArgumentTypeSetType] = field(
        default=None,
        metadata={
            "name": "ArgumentTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    meta_command_set: Optional["CommandMetaDataType.MetaCommandSet"] = field(
        default=None,
        metadata={
            "name": "MetaCommandSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "required": True,
        },
    )
    command_container_set: Optional[CommandContainerSetType] = field(
        default=None,
        metadata={
            "name": "CommandContainerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    stream_set: Optional[StreamSetType] = field(
        default=None,
        metadata={
            "name": "StreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    algorithm_set: Optional[AlgorithmSetType] = field(
        default=None,
        metadata={
            "name": "AlgorithmSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class MetaCommandSet:
        """
        :ivar meta_command: All commands to be sent on this mission are
            listed here.  In addition this area has verification and
            validation information
        :ivar meta_command_ref: Used to include a MetaCommand defined in
            another sub-system in this sub-system.
        :ivar block_meta_command: BlockMetaCommands are simply a list of
            individual MetaCommands that can be packaged up in a single
            BlockMetaCommand.
        """

        meta_command: list[MetaCommandType] = field(
            default_factory=list,
            metadata={
                "name": "MetaCommand",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        meta_command_ref: list[str] = field(
            default_factory=list,
            metadata={
                "name": "MetaCommandRef",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )
        block_meta_command: list[
            "CommandMetaDataType.MetaCommandSet.BlockMetaCommand"
        ] = field(
            default_factory=list,
            metadata={
                "name": "BlockMetaCommand",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
            },
        )

        @dataclass
        class BlockMetaCommand(NameDescriptionType):
            meta_command_step_list: Optional[
                "CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList"
            ] = field(
                default=None,
                metadata={
                    "name": "MetaCommandStepList",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )

            @dataclass
            class MetaCommandStepList:
                meta_command_step: list[
                    "CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep"
                ] = field(
                    default_factory=list,
                    metadata={
                        "name": "MetaCommandStep",
                        "type": "Element",
                        "namespace": "http://www.omg.org/space/xtce",
                        "min_occurs": 1,
                    },
                )

                @dataclass
                class MetaCommandStep:
                    argument_list: Optional[
                        "CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep.ArgumentList"
                    ] = field(
                        default=None,
                        metadata={
                            "name": "ArgumentList",
                            "type": "Element",
                            "namespace": "http://www.omg.org/space/xtce",
                        },
                    )
                    meta_command_ref: Optional[str] = field(
                        default=None,
                        metadata={
                            "name": "metaCommandRef",
                            "type": "Attribute",
                            "required": True,
                        },
                    )

                    @dataclass
                    class ArgumentList:
                        argument: list[
                            "CommandMetaDataType.MetaCommandSet.BlockMetaCommand.MetaCommandStepList.MetaCommandStep.ArgumentList.Argument"
                        ] = field(
                            default_factory=list,
                            metadata={
                                "name": "Argument",
                                "type": "Element",
                                "namespace": "http://www.omg.org/space/xtce",
                                "min_occurs": 1,
                            },
                        )

                        @dataclass
                        class Argument:
                            name: Optional[str] = field(
                                default=None,
                                metadata={
                                    "type": "Attribute",
                                    "required": True,
                                },
                            )
                            value: Optional[str] = field(
                                default=None,
                                metadata={
                                    "type": "Attribute",
                                    "required": True,
                                },
                            )


@dataclass
class TelemetryMetaDataType:
    """
    All the data about telemetry is contained in TelemetryMetaData.

    :ivar parameter_type_set: A list of parameter types
    :ivar parameter_set: A list of Parameters for this Space System.
    :ivar container_set: Holds the list of all potential container
        definitions for telemetry. Containers may parts of packets or
        TDM, and then groups of the containers, and then an entire
        entity -- such as a packet.  In order to maximize re-used for
        duplication, the pieces may defined once here, and then
        assembled as needed into larger structures, also here.
    :ivar message_set: Messages are an alternative method of uniquely
        identifying containers within a Service.  A message provides a
        test in the form of MatchCriteria to match to a container.  A
        simple example might be: [When minorframeID=21, the message is
        the 21st minorframe container.  The collection of messages to
        search thru will be bound by a Service.
    :ivar stream_set:
    :ivar algorithm_set:
    """

    parameter_type_set: Optional[ParameterTypeSetType] = field(
        default=None,
        metadata={
            "name": "ParameterTypeSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    parameter_set: Optional[ParameterSetType] = field(
        default=None,
        metadata={
            "name": "ParameterSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    container_set: Optional[ContainerSetType] = field(
        default=None,
        metadata={
            "name": "ContainerSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    message_set: Optional["TelemetryMetaDataType.MessageSet"] = field(
        default=None,
        metadata={
            "name": "MessageSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    stream_set: Optional[StreamSetType] = field(
        default=None,
        metadata={
            "name": "StreamSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    algorithm_set: Optional[AlgorithmSetType] = field(
        default=None,
        metadata={
            "name": "AlgorithmSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )

    @dataclass
    class MessageSet:
        message: list["TelemetryMetaDataType.MessageSet.Message"] = field(
            default_factory=list,
            metadata={
                "name": "Message",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )
        name: Optional[str] = field(
            default=None,
            metadata={
                "type": "Attribute",
            },
        )

        @dataclass
        class Message(NameDescriptionType):
            """
            :ivar match_criteria:
            :ivar contain_ref: The ContainerRef should point to ROOT
                container that will describe an entire packet/minor
                frame or chunk of telemetry.
            """

            match_criteria: Optional[MatchCriteriaType] = field(
                default=None,
                metadata={
                    "name": "MatchCriteria",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )
            contain_ref: Optional[ContainerRefType] = field(
                default=None,
                metadata={
                    "name": "ContainRef",
                    "type": "Element",
                    "namespace": "http://www.omg.org/space/xtce",
                    "required": True,
                },
            )


@dataclass
class SpaceSystemType(NameDescriptionType):
    """SpaceSystem is a collection of SpaceSystem(s) including space assets,
    ground assets, multi-satellite systems and sub-systems.

    A SpaceSystem is the root element for the set of data necessary to monitor and command an arbitrary space device - this includes the binary decomposition the data streams going into and out of a device.

    :ivar header:
    :ivar telemetry_meta_data:
    :ivar command_meta_data:
    :ivar service_set: A service is a logical grouping of container
        and/or messages.
    :ivar space_system:
    :ivar operational_status:
    """

    header: Optional[HeaderType] = field(
        default=None,
        metadata={
            "name": "Header",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    telemetry_meta_data: Optional[TelemetryMetaDataType] = field(
        default=None,
        metadata={
            "name": "TelemetryMetaData",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    command_meta_data: Optional[CommandMetaDataType] = field(
        default=None,
        metadata={
            "name": "CommandMetaData",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    service_set: Optional["SpaceSystemType.ServiceSet"] = field(
        default=None,
        metadata={
            "name": "ServiceSet",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
        },
    )
    space_system: list["SpaceSystem"] = field(
        default_factory=list,
        metadata={
            "name": "SpaceSystem",
            "type": "Element",
            "namespace": "http://www.omg.org/space/xtce",
            "nillable": True,
        },
    )
    operational_status: Optional[str] = field(
        default=None,
        metadata={
            "name": "operationalStatus",
            "type": "Attribute",
        },
    )

    @dataclass
    class ServiceSet:
        service: list[ServiceType] = field(
            default_factory=list,
            metadata={
                "name": "Service",
                "type": "Element",
                "namespace": "http://www.omg.org/space/xtce",
                "min_occurs": 1,
            },
        )


@dataclass
class SpaceSystem(SpaceSystemType):
    """
    The ROOT Element.
    """

    class Meta:
        nillable = True
        namespace = "http://www.omg.org/space/xtce"
