"""Context models for XTCE 1.2 objects."""

from xtce2py.xtce.context import BaseEffectiveCommand, BaseExecutionStep
from xtce2py.xtce_1_2.bindings import models as xtce
from xtce2py.xtce_1_2.types import AnyArgumentEntryType

ExecutionStep = BaseExecutionStep[AnyArgumentEntryType]

EffectiveCommand = BaseEffectiveCommand[xtce.ArgumentType, ExecutionStep]
