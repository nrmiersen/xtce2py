"""Semantic validation for XTCE objects."""

from xtce2py.xtce import BaseXtceValidator, SystemContext, XtceValidationError
from xtce2py.xtce_1_2 import bindings as xtce
from xtce2py.xtce_1_2.types import AnyArgumentType
from xtce2py.xtce_1_2.utils import iter_argument_types, iter_space_systems

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
        for space_system in iter_space_systems(self.space_system):
            self._validate_space_system(space_system)

        is_valid = len(self.errors) == 0
        return is_valid, self.errors

    def _validate_space_system(self, space_system: xtce.SpaceSystem):
        """Run all validations scoped to one SpaceSystem node."""
        self._validate_argument_types(space_system)

    def _validate_argument_types(self, space_system: xtce.SpaceSystem):
        """Validate that all argument types have valid encodings."""
        for argument_type in iter_argument_types(space_system):
            path = self.context.get_path(argument_type)
            self._validate_argument_encoding_types(argument_type, path)

    def _validate_argument_encoding_types(
        self, argument_type: AnyArgumentType, path: str
    ):
        """Ensure every concrete argument type contains exactly one data encoding."""
        # Arrays and aggregates don't have encodings, they just reference other types that do, so we skip them
        if isinstance(
            argument_type,
            (xtce.ArrayArgumentType, xtce.AggregateArgumentType),
        ):
            return

        # Time argument types have encoding definitions nested in an 'encoding' element
        elif isinstance(
            argument_type,
            (xtce.RelativeTimeArgumentType, xtce.AbsoluteTimeArgumentType),
        ):
            if argument_type.encoding:
                encodings = [
                    argument_type.encoding.binary_data_encoding,
                    argument_type.encoding.float_data_encoding,
                    argument_type.encoding.integer_data_encoding,
                    argument_type.encoding.string_data_encoding,
                ]
            else:
                # TODO try to resolve a base type and check its encodings instead
                encodings = []

        # All other argument types have encoding definitions directly on the type
        else:
            encodings = [
                argument_type.binary_data_encoding,
                argument_type.float_data_encoding,
                argument_type.integer_data_encoding,
                argument_type.string_data_encoding,
            ]

        active_encodings = [enc for enc in encodings if enc is not None]

        # An encoding element is required
        if len(active_encodings) == 0:
            self.errors.append(
                XtceValidationError(
                    location=path,
                    message="Type has no encoding defined. At least one encoding is required.",
                )
            )

        else:
            pass  # TODO need to check that the encoding type makes sense for the argument type
