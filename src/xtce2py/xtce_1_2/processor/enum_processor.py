"""Enumeration processor."""

from typing import SupportsIndex, SupportsInt

from xtce2py.xtce import (
    BaseProcessor,
    EnumViewModel,
    SystemContext,
    sanitize_enum_label,
    unwrap,
)
from xtce2py.xtce_1_2 import bindings as xtce
from xtce2py.xtce_1_2.utils import get_description


class EnumProcessor(BaseProcessor):
    """Processes enumeration type objects to produce EnumViewModel instances for code generation."""

    def __init__(self, context: SystemContext) -> None:
        """Initialize the EnumProcessor.

        Args:
            context (SystemContext): The system context for resolving references.

        """
        self.context = context

    def process(
        self, xtce_obj: xtce.EnumeratedArgumentType | xtce.EnumeratedParameterType
    ) -> EnumViewModel:
        """Generate an EnumViewModel from an XTCE enumeration type object.

        Args:
            xtce_obj (xtce.EnumeratedArgumentType | xtce.EnumeratedParameterType): The XTCE enumeration type object to process.

        Returns:
            EnumViewModel: The generated EnumViewModel instance.

        """
        name = self.context.get_python_name(xtce_obj)
        desc = get_description(xtce_obj)

        # Extract values from the enum
        values = {}
        if xtce_obj.enumeration_list:
            for item in xtce_obj.enumeration_list.enumeration:
                clean_label = sanitize_enum_label(unwrap(item.label))

                # Sanity check fallback
                if clean_label is None:
                    raise ValueError(f"Invalid enumeration label: {item.label}")

                # Handle numeric conversion
                if isinstance(
                    item.value,
                    (SupportsInt, SupportsIndex, str, bytes, bytearray),
                ):
                    clean_value = int(unwrap(item.value))
                else:
                    # Fallback for things like hex values
                    clean_value = int(unwrap(item.value), 0)

                values[clean_label] = clean_value

        return EnumViewModel(name=name, description=desc, values=values)
