"""Semantic validation for XTCE objects."""

from xtce2py.xtce import BaseXtceValidator, SystemContext, XtceValidationError
from xtce2py.xtce_1_2 import bindings as xtce

"""
TODO:

need to check that all references actually exist
need to check recursion in command hierarchy (e.g., A inherits from B, B inherits from A)
need to validate that encoding types are actually valid (BCD has valid number of bits, etc.)
need to check that arguments don't collide (raise warning)
need to check that string arguments actually have enough defined to encode them
"""


class SemanticValidator(BaseXtceValidator):
    """Validates the logical integrity of an XTCE SpaceSystem."""

    def __init__(self, space_system: xtce.SpaceSystem, context: SystemContext):
        """Initialize the validator with the system context.

        Args:
            space_system (xtce.SpaceSystem): The XTCE space system to validate.
            context (SystemContext): The system context containing the XTCE paths and objects.

        """
        self.space_system = space_system
        self.context = context
        self.errors: list[XtceValidationError] = []

    def validate(self) -> tuple[bool, list[XtceValidationError]]:
        """Run all semantic validation.

        Returns:
            tuple[bool, list[XtceValidationError]]: A tuple containing a boolean indicating if the data is valid and a list of validation errors if not.

        """
        is_valid = len(self.errors) == 0
        return is_valid, self.errors
