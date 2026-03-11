"""Context models for XTCE 1.2 objects."""

from xtce2py.xtce.context import BaseEffectiveCommand, BaseExecutionStep
from xtce2py.xtce_1_2.bindings import models as xtce

ExecutionStep = BaseExecutionStep[
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
]

EffectiveCommand = BaseEffectiveCommand[xtce.ArgumentType, ExecutionStep]
