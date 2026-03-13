"""Command processor."""

import keyword
import logging
import re
from functools import singledispatchmethod
from typing import Any

from xtce2py.xtce import (
    BaseProcessor,
    CodecRecipeItem,
    CommandViewModel,
    EncodingInfo,
    PydanticField,
    SystemContext,
    unwrap,
)
from xtce2py.xtce_1_2.bindings import models as xtce
from xtce2py.xtce_1_2.context import EffectiveCommand
from xtce2py.xtce_1_2.utils import map_bit_order, map_byte_order

log = logging.getLogger(__name__)


class CommandProcessor(BaseProcessor):
    """Processes EffectiveCommand objects to produce CommandViewModel instances for code generation."""

    def __init__(self, context: SystemContext) -> None:
        """Initialize the processor with a system context.

        Args:
            context (SystemContext): The system context for resolving references.

        """
        self.context = context

    def process(self, cmd: EffectiveCommand) -> CommandViewModel:
        """Generate a CommandViewModel from an EffectiveCommand.

        Args:
            cmd (EffectiveCommand): The command to process.

        Returns:
            CommandViewModel: The generated view model for the command.

        """
        # Map argument names to types
        arg_map = {}
        all_args_map = {}

        for arg in cmd.all_arguments:
            all_args_map[arg.name] = arg
            if arg.argument_type_ref:
                try:
                    _, resolved_type = self.context.resolve(
                        arg.argument_type_ref, scope=cmd.path
                    )
                    arg_map[arg.name] = resolved_type
                except KeyError:
                    arg_map[arg.name] = arg

        fields: list[PydanticField] = []
        steps: list[CodecRecipeItem] = []
        own_arg_names = {arg.name for arg in cmd.own_arguments}

        # Create fields for own arguments
        fields = []
        required_enums = set()
        for arg in cmd.own_arguments:
            type_def = arg_map.get(arg.name)
            pydantic_field = self._create_field(arg.name, type_def)

            if arg.name in cmd.argument_assignments:
                raw_val = cmd.argument_assignments[arg.name]
                val_str, enum_name = self._coerce_default(
                    raw_val, type_def, pydantic_field
                )
                pydantic_field.default = val_str
                if enum_name:
                    required_enums.add(enum_name)

            fields.append(pydantic_field)

        # Get inherited defaults
        inherited_defaults = {}
        for arg_name, raw_val in cmd.argument_assignments.items():
            if arg_name not in own_arg_names and arg_name in all_args_map:
                parent_arg = all_args_map[arg_name]
                type_def = arg_map.get(arg_name)
                temp_field = self._create_field(parent_arg.name, type_def)
                sanitized_name = _sanitize(arg_name)
                val_str, enum_name = self._coerce_default(raw_val, type_def, temp_field)
                inherited_defaults[sanitized_name] = {
                    "value": val_str,
                    "type_hint": temp_field.type_hint,
                }
                if enum_name:
                    required_enums.add(enum_name)

        fields.sort(key=lambda f: f.default is not None and f.default != "")

        # Create recipe from all steps
        for step in cmd.execution_steps:
            item = step.item
            condition = step.python_condition

            if isinstance(item, xtce.ArgumentArgumentRefEntryType):
                arg_name = unwrap(item.argument_ref)
                type_def = arg_map.get(arg_name)
                encoding_info: EncodingInfo = self._extract_encoding(type_def)

                steps.append(
                    CodecRecipeItem(
                        name=arg_name,
                        value_src=f"self.{_sanitize(arg_name)}",
                        encoding=encoding_info,
                        condition=condition,
                    )
                )

            else:
                raise NotImplementedError(
                    f"Unsupported codec recipe item type: {type(item)}"
                )

        class_obj: xtce.MetaCommandType = self.context._lookup(cmd.path)
        class_name = self.context.get_python_name(class_obj)

        # Determine parent class name
        parent_class = "XtcePacket"
        if cmd.parent_path:
            # Get the parent object
            parent_obj: xtce.MetaCommandType = self.context._lookup(cmd.parent_path)
            parent_class = self.context.get_python_name(parent_obj)

        return CommandViewModel(
            class_name=class_name,
            parent_class=parent_class,
            docstring=f"XTCE Path: {cmd.path}.",
            fields=fields,
            encode_steps=steps,
            inherited_defaults=inherited_defaults,
            required_enums=required_enums,
        )

    def _coerce_default(
        self, raw_val: str, type_def: Any, pydantic_field: "PydanticField"
    ) -> tuple[str, str | None]:
        if isinstance(type_def, xtce.BooleanArgumentType):
            one_str = getattr(type_def, "one_string_value", "True")
            if str(raw_val) == str(one_str):
                return "1", None
            else:
                return "0", None

        val_lower = str(raw_val).lower()
        if val_lower == "true":
            return "1", None
        if val_lower == "false":
            return "0", None

        try:
            float(raw_val)
            return raw_val, None
        except ValueError:
            pass

        enum_class = None
        match = re.search(r"Union\[(\w+),\s*int,\s*str\]", pydantic_field.type_hint)
        if match:
            enum_class = match.group(1)
        elif type_def and "Enumerated" in type_def.__class__.__name__:
            enum_class = _sanitize_class_name(type_def.name, False)

        if enum_class:
            clean_label = raw_val.upper()
            return f"{enum_class}.{clean_label}", enum_class

        return f'"{raw_val}"', None

    @singledispatchmethod
    def _extract_encoding(
        self,
        type_def: xtce.StringArgumentType
        | xtce.EnumeratedArgumentType
        | xtce.IntegerArgumentType
        | xtce.BinaryArgumentType
        | xtce.FloatArgumentType
        | xtce.BooleanArgumentType
        | xtce.RelativeTimeArgumentType
        | xtce.AbsoluteTimeArgumentType
        | xtce.ArrayArgumentType
        | xtce.AggregateArgumentType,
    ) -> EncodingInfo:
        """Dispatch method to extract encoding information based on argument type."""
        raise TypeError(
            f"Unsupported argument type for encoding extraction: {type(type_def)}"
        )

    @_extract_encoding.register
    def _(self, string_argument_type: xtce.StringArgumentType) -> EncodingInfo:
        """Extract encoding information from a StringArgumentType definition."""
        # Set temporary defaults
        bits = 0

        if string_argument_type.string_data_encoding:
            if string_argument_type.string_data_encoding.size_in_bits:
                if string_argument_type.string_data_encoding.size_in_bits.fixed:
                    bits = unwrap(
                        string_argument_type.string_data_encoding.size_in_bits.fixed.fixed_value
                    )
            encoding = string_argument_type.string_data_encoding.encoding.value.lower()
            byte_order = map_byte_order(
                string_argument_type.string_data_encoding.byte_order
            )
            reverse_bits = map_bit_order(
                string_argument_type.string_data_encoding.bit_order
            )

        else:
            raise NotImplementedError(
                "String arguments without explicit encoding are not supported."
            )

        return EncodingInfo(
            bits=bits,
            encoding=encoding,
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, enumerated_argument_type: xtce.EnumeratedArgumentType) -> EncodingInfo:
        """Extract encoding information from a EnumeratedArgumentType definition."""
        # Set temporary defaults
        bits = 0

        if enumerated_argument_type.integer_data_encoding:
            # Override with fields defined in integer data encoding if present
            bits = enumerated_argument_type.integer_data_encoding.size_in_bits
            encoding = (
                enumerated_argument_type.integer_data_encoding.encoding.value.lower()
            )
            byte_order = map_byte_order(
                enumerated_argument_type.integer_data_encoding.byte_order
            )
            reverse_bits = map_bit_order(
                enumerated_argument_type.integer_data_encoding.bit_order
            )

        else:
            raise NotImplementedError(
                "Enumerated arguments without explicit encoding are not supported."
            )

        return EncodingInfo(
            bits=bits,
            encoding=encoding,
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, integer_argument_type: xtce.IntegerArgumentType) -> EncodingInfo:
        """Extract encoding information from a IntegerArgumentType definition."""
        # Extract encoding info from the base type definition
        bits = integer_argument_type.size_in_bits
        signed = integer_argument_type.signed
        encoding = "unsigned"
        byte_order = "big"

        if integer_argument_type.integer_data_encoding:
            # Override with fields defined in integer data encoding if present
            bits = integer_argument_type.integer_data_encoding.size_in_bits
            encoding = (
                integer_argument_type.integer_data_encoding.encoding.value.lower()
            )
            byte_order = map_byte_order(
                integer_argument_type.integer_data_encoding.byte_order
            )
            reverse_bits = map_bit_order(
                integer_argument_type.integer_data_encoding.bit_order
            )

        elif signed:
            # Default to two's complement if signed but no encoding specified
            arg_name = self.context.get_python_name(integer_argument_type)
            log.warning(
                f"Integer argument '{arg_name}' is marked as signed but has no explicit encoding. Defaulting to two's complement."
            )
            encoding = "twosComplement"

        return EncodingInfo(
            bits=bits,
            encoding=encoding,
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, type_def: xtce.BinaryArgumentType) -> EncodingInfo:
        """Extract encoding information from a BinaryArgumentType definition."""
        return EncodingInfo(
            bits=0, encoding="unsigned", byte_order="big", reverse_bits=False
        )  # TODO

    @_extract_encoding.register
    def _(self, float_argument_type: xtce.FloatArgumentType) -> EncodingInfo:
        """Extract encoding information from a FloatArgumentType definition."""
        # Extract encoding info from the base type definition
        bits = float_argument_type.size_in_bits

        if float_argument_type.float_data_encoding:
            # Override with fields defined in float data encoding if present
            bits = float_argument_type.float_data_encoding.size_in_bits.value
            encoding = float_argument_type.float_data_encoding.encoding.value.lower()
            byte_order = map_byte_order(
                float_argument_type.float_data_encoding.byte_order
            )
            reverse_bits = map_bit_order(
                float_argument_type.float_data_encoding.bit_order
            )

        else:
            raise NotImplementedError(
                "Enumerated arguments without explicit encoding are not supported."
            )

        return EncodingInfo(
            bits=bits,
            encoding=encoding,
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, type_def: xtce.BooleanArgumentType) -> EncodingInfo:
        """Extract encoding information from a BooleanArgumentType definition."""
        return EncodingInfo(
            bits=1, encoding="unsigned", byte_order="big", reverse_bits=False
        )

    @_extract_encoding.register
    def _(self, type_def: xtce.RelativeTimeArgumentType) -> EncodingInfo:
        """Extract encoding information from a RelativeTimeArgumentType definition."""
        return EncodingInfo(
            bits=0, encoding="unsigned", byte_order="big", reverse_bits=False
        )  # TODO

    @_extract_encoding.register
    def _(self, type_def: xtce.AbsoluteTimeArgumentType) -> EncodingInfo:
        """Extract encoding information from a AbsoluteTimeArgumentType definition."""
        return EncodingInfo(
            bits=0, encoding="unsigned", byte_order="big", reverse_bits=False
        )  # TODO

    @_extract_encoding.register
    def _(self, type_def: xtce.ArrayArgumentType) -> EncodingInfo:
        """Extract encoding information from a ArrayArgumentType definition."""
        return EncodingInfo(
            bits=0, encoding="unsigned", byte_order="big", reverse_bits=False
        )  # TODO

    @_extract_encoding.register
    def _(self, type_def: xtce.AggregateArgumentType) -> EncodingInfo:
        """Extract encoding information from a AggregateArgumentType definition."""
        return EncodingInfo(
            bits=0, encoding="unsigned", byte_order="big", reverse_bits=False
        )  # TODO

    def _create_field(self, name, type_def) -> PydanticField:
        clean_name = _sanitize(name)
        desc = getattr(type_def, "short_description", "") or ""

        py_type = "int"
        req_import = None

        if isinstance(type_def, xtce.FloatArgumentType):
            py_type = "float"
        elif isinstance(type_def, xtce.StringArgumentType):
            py_type = "str"
        elif isinstance(type_def, xtce.EnumeratedArgumentType):
            enum_name = _sanitize_class_name(unwrap(type_def.name))
            py_type = f"Annotated[Union[{enum_name}, int, str], BeforeValidator(fuzzy_validator({enum_name}))]"
            req_import = f"from .enums import {enum_name}"

        return PydanticField(
            name=clean_name,
            type_hint=f"Annotated[{py_type}, Field(description='{desc}')]",
            default=None,
            is_fixed=False,
            required_import=req_import,
        )


def _sanitize(name: str) -> str:
    clean = name.replace(" ", "_").replace("-", "_").lower()

    # If the resulting name is a reserved Python keyword, append an underscore
    if keyword.iskeyword(clean):
        return f"{clean}_"

    return clean


def _sanitize_class_name(name: str, is_abstract: bool = False) -> str:
    clean = name.replace(" ", "").replace("-", "_")
    base = clean[0].upper() + clean[1:]
    return f"_{base}" if is_abstract else base
