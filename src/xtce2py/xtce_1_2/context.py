"""Context models for XTCE 1.2 objects."""

import xtce2py.xtce_1_2.bindings.models as xtce
from xtce2py.xtce.context import (
    BaseEffectiveArgument,
    BaseEffectiveCommand,
    BaseExecutionStep,
)
from xtce2py.xtce_1_2.types import AnyCommandContainerEntryType

EffectiveArgument = BaseEffectiveArgument[xtce.ArgumentType]

ExecutionStep = BaseExecutionStep[AnyCommandContainerEntryType]

EffectiveCommand = BaseEffectiveCommand[EffectiveArgument, ExecutionStep]
