"""XTCE 1.2 types."""

from typing import TypeAlias

import xtce2py.xtce_1_2.bindings as xtce

AnyArgumentType: TypeAlias = (
    xtce.StringArgumentType
    | xtce.EnumeratedArgumentType
    | xtce.IntegerArgumentType
    | xtce.BinaryArgumentType
    | xtce.FloatArgumentType
    | xtce.BooleanArgumentType
    | xtce.RelativeTimeArgumentType
    | xtce.AbsoluteTimeArgumentType
    | xtce.ArrayArgumentType
    | xtce.AggregateArgumentType
)

AnyArgumentEntryType: TypeAlias = (
    xtce.ArgumentParameterRefEntryType
    | xtce.ArgumentParameterSegmentRefEntryType
    | xtce.ArgumentContainerRefEntryType
    | xtce.ArgumentContainerSegmentRefEntryType
    | xtce.ArgumentStreamSegmentEntryType
    | xtce.ArgumentIndirectParameterRefEntryType
    | xtce.ArgumentArrayParameterRefEntryType
    | xtce.ArgumentArgumentRefEntryType
    | xtce.ArgumentArrayArgumentRefEntryType
    | xtce.ArgumentFixedValueEntryType
)

AnyEncodingType: TypeAlias = (
    xtce.BinaryDataEncodingType
    | xtce.FloatDataEncodingType
    | xtce.IntegerDataEncodingType
    | xtce.StringDataEncodingType
)
