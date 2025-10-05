"""XTCE encoding utilities."""

from dataclasses import dataclass
from typing import Any

from xtce2py import xtce_1_1


@dataclass
class TypeMappingInfo:
    """A structured container for Python type mapping information."""

    python_type: Any
    custom_decoder: str | None = None
    signed: bool = False


XTCE_ENCODING_MAP = {
    # Integer Types
    xtce_1_1.IntegerDataEncodingTypeEncoding.UNSIGNED: TypeMappingInfo(int),
    xtce_1_1.IntegerDataEncodingTypeEncoding.SIGN_MAGNITUDE: TypeMappingInfo(
        int,
        custom_decoder="_decode_sign_magnitude",
        signed=True,
    ),
    xtce_1_1.IntegerDataEncodingTypeEncoding.TWOS_COMPLIMENT: TypeMappingInfo(
        int,
        signed=True,
    ),
    xtce_1_1.IntegerDataEncodingTypeEncoding.ONES_COMPLIMENT: TypeMappingInfo(
        int,
        custom_decoder="_decode_ones_complement",
        signed=True,
    ),
    xtce_1_1.IntegerDataEncodingTypeEncoding.BCD: TypeMappingInfo(
        int,
        custom_decoder="_decode_unpacked_bcd",
    ),
    xtce_1_1.IntegerDataEncodingTypeEncoding.PACKED_BCD: TypeMappingInfo(
        int,
        custom_decoder="_decode_packed_bcd",
    ),
    # Float Types
    xtce_1_1.FloatDataEncodingTypeEncoding.IEEE754_1985: TypeMappingInfo(float),
    xtce_1_1.FloatDataEncodingTypeEncoding.MILSTD_1750_A: TypeMappingInfo(
        float, custom_decoder="_decode_milstd_1750a"
    ),
    # String Types
    xtce_1_1.StringDataEncodingTypeEncoding.UTF_8: TypeMappingInfo(str),
    xtce_1_1.StringDataEncodingTypeEncoding.UTF_16: TypeMappingInfo(str),
}

XTCE_PARAMETER_TYPE_MAP = {
    xtce_1_1.ParameterTypeSetType.IntegerParameterType: int,
    xtce_1_1.ParameterTypeSetType.FloatParameterType: float,
    xtce_1_1.ParameterTypeSetType.StringParameterType: str,
    xtce_1_1.ParameterTypeSetType.BooleanParameterType: bool,
    xtce_1_1.ParameterTypeSetType.BinaryParameterType: bytes,
}
