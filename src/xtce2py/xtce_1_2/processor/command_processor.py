"""Command processor.

This module defines the CommandProcessor class, which processes EffectiveCommand objects to produce CommandViewModel instances for code generation. The processor maps argument definitions to Python types, extracts encoding information, and constructs a view model that captures the structure and encoding of the command for use in generating Python code.
"""

import logging
from functools import singledispatchmethod

from xtce2py.utils import sanitize_class_name
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
from xtce2py.xtce_1_2.context import EffectiveArgument, EffectiveCommand
from xtce2py.xtce_1_2.types import AnyArgumentType
from xtce2py.xtce_1_2.utils import get_description, map_bit_order, map_byte_order

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
        """Generate a CommandViewModel from an EffectiveCommand."""
        required_enums = set()

        # Resolve argument types
        type_map = self._resolve_types(cmd)
        all_args_map = {arg.name: arg for arg in cmd.all_arguments}
        own_arg_names = {arg.name for arg in cmd.own_arguments}

        # Extract data from the arguments
        fields = self._process_own_arguments(cmd, type_map, required_enums)
        encode_steps = self._process_execution_steps(
            cmd, type_map, all_args_map, own_arg_names
        )
        inherited_defaults = self._process_inherited_arguments(
            cmd, type_map, all_args_map, own_arg_names, required_enums
        )

        # Resolve class hierarchy
        class_name, parent_class = self._resolve_class_hierarchy(cmd)

        return CommandViewModel(
            class_name=class_name,
            parent_class=parent_class,
            docstring=f"XTCE Path: {cmd.path}.",
            fields=fields,
            encode_steps=encode_steps,
            inherited_defaults=inherited_defaults,
            required_enums=required_enums,
        )

    def _resolve_types(self, cmd: EffectiveCommand) -> dict[str, AnyArgumentType]:
        """Resolve argument type references."""
        type_map: dict[str, AnyArgumentType] = {}
        for arg in cmd.all_arguments:
            type_ref = unwrap(arg.raw_arg.argument_type_ref)
            _, type_def = self.context.resolve(type_ref, scope=cmd.path)

            type_map[arg.name] = type_def

        return type_map

    def _process_own_arguments(
        self,
        cmd: EffectiveCommand,
        type_map: dict[str, AnyArgumentType],
        required_enums: set[str],
    ) -> list[PydanticField]:
        """Process the command's own arguments."""
        fields: list[PydanticField] = []
        for arg in cmd.own_arguments:
            type_def = type_map[arg.name]

            # Generate the Pydantic field
            pydantic_field = self._create_field(arg, type_def)

            # Get the initial/default value if present
            raw_initial = arg.initial_value
            raw_assign = cmd.argument_assignments.get(arg.name)
            raw_val = raw_assign if raw_assign is not None else raw_initial

            if raw_val is not None:
                val_str, enum_name = self._coerce_default(raw_val, type_def)
                pydantic_field.default = val_str
                if enum_name:
                    required_enums.add(enum_name)

            fields.append(pydantic_field)

        # Sort so fixed fields are last
        fields.sort(key=lambda f: f.default is not None and f.default != "")

        return fields

    def _process_inherited_arguments(
        self,
        cmd: EffectiveCommand,
        type_map: dict[str, AnyArgumentType],
        all_args_map: dict[str, EffectiveArgument],
        own_arg_names: set[str],
        required_enums: set[str],
    ) -> dict[str, dict[str, str]]:
        """Process inherited arguments."""
        inherited_defaults: dict[str, dict[str, str]] = {}
        for raw_name, raw_val in cmd.argument_assignments.items():
            if raw_name not in own_arg_names and raw_name in all_args_map:
                parent_arg = all_args_map[raw_name]
                type_def = type_map[raw_name]

                # Create the inherited field and set the default
                temp_field = self._create_field(parent_arg, type_def)
                val_str, enum_name = self._coerce_default(raw_val, type_def)

                inherited_defaults[parent_arg.clean_name] = {
                    "value": val_str,
                    "type_hint": temp_field.type_hint,
                }

                if enum_name:
                    required_enums.add(enum_name)

        return inherited_defaults

    def _process_execution_steps(
        self,
        cmd: EffectiveCommand,
        type_map: dict[str, AnyArgumentType],
        all_args_map: dict[str, EffectiveArgument],
        own_arg_names: set[str],
    ) -> list[CodecRecipeItem]:
        """Process the command's execution steps."""
        steps: list[CodecRecipeItem] = []
        for step in cmd.execution_steps:
            item = step.item
            if isinstance(item, xtce.ArgumentArgumentRefEntryType):
                raw_name = unwrap(item.argument_ref)

                if raw_name not in own_arg_names:
                    continue

                arg = all_args_map[raw_name]
                type_def = type_map.get(raw_name, arg.raw_arg)
                encoding_info = self._extract_encoding(type_def)

                steps.append(
                    CodecRecipeItem(
                        name=raw_name,
                        value_src=f"self.{arg.clean_name}",
                        encoding=encoding_info,
                        condition=step.python_condition,
                    )
                )

            else:
                raise NotImplementedError(
                    f"Unsupported CommandContainerEntryListType entry type: {type(item).__name__}"
                )

        return steps

    def _resolve_class_hierarchy(self, cmd: EffectiveCommand) -> tuple[str, str]:
        """Determine the Python class name and its parent class name."""
        class_obj: xtce.MetaCommandType = self.context.lookup(cmd.path)
        class_name = self.context.get_python_name(class_obj)

        parent_class = "XtcePacket"
        if cmd.parent_path:
            parent_obj: xtce.MetaCommandType = self.context.lookup(cmd.parent_path)
            parent_class = self.context.get_python_name(parent_obj)

        return class_name, parent_class

    def _create_field(
        self, arg: EffectiveArgument, type_def: AnyArgumentType
    ) -> PydanticField:
        """Create a Pydantic field."""
        builder = FieldBuilder(arg, type_def)
        return builder.build()

    def _coerce_default(
        self, raw_val: str, type_def: AnyArgumentType | xtce.ArgumentType
    ) -> tuple[str, str | None]:
        """Convert an XTCE raw value into a safe Python literal string."""
        if isinstance(type_def, xtce.EnumeratedArgumentType):
            enum_class = sanitize_class_name(unwrap(type_def.name))
            clean_label = str(raw_val).upper().replace(" ", "_")
            return f"{enum_class}.{clean_label}", enum_class

        if isinstance(type_def, xtce.BooleanArgumentType):
            return "1" if str(raw_val) == str(type_def.one_string_value) else "0", None

        if isinstance(type_def, (xtce.IntegerArgumentType, xtce.FloatArgumentType)):
            return str(raw_val), None

        if isinstance(type_def, (xtce.StringArgumentType, xtce.BinaryArgumentType)):
            return f'"{raw_val}"', None

        return f'"{raw_val}"', None

    @singledispatchmethod
    def _extract_encoding(self, type_def: AnyArgumentType) -> EncodingInfo:
        """Dispatch method to extract encoding information based on argument type."""
        # TODO add support for units (maybe not here?)
        # TODO add support for base type resolution
        raise TypeError(
            f"Unsupported argument type for encoding extraction: {type(type_def)}"
        )

    @_extract_encoding.register
    def _(self, string_argument_type: xtce.StringArgumentType) -> EncodingInfo:
        """Extract encoding information from a StringArgumentType definition."""
        # Parse string encoding
        if enc := string_argument_type.string_data_encoding:
            # TODO add support for variable length encodings and encodings with size defined by another parameter
            bits = (
                unwrap(enc.size_in_bits.fixed.fixed_value)
                if enc.size_in_bits and enc.size_in_bits.fixed
                else 0
            )
            encoding = enc.encoding.value.lower()
            byte_order = map_byte_order(enc.byte_order)
            reverse_bits = map_bit_order(enc.bit_order)

        else:
            raise NotImplementedError(
                f"Unsupported string argument encoding at {self.context.get_path(string_argument_type)}: expected StringDataEncodingType. Other encoding elements for StringArgumentType are not implemented yet."
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
        # Parse integer encoding
        if enc := enumerated_argument_type.integer_data_encoding:
            bits = enc.size_in_bits
            encoding = enc.encoding.value.lower()
            byte_order = map_byte_order(enc.byte_order)
            reverse_bits = map_bit_order(enc.bit_order)

        else:
            raise NotImplementedError(
                f"Unsupported enumerated argument encoding at {self.context.get_path(enumerated_argument_type)}: expected IntegerDataEncodingType. Other encoding elements for EnumeratedArgumentType are not implemented yet."
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
        # Parse integer encoding
        if enc := integer_argument_type.integer_data_encoding:
            bits = enc.size_in_bits
            encoding = enc.encoding.value.lower()
            byte_order = map_byte_order(enc.byte_order)
            reverse_bits = map_bit_order(enc.bit_order)

        else:
            raise NotImplementedError(
                f"Unsupported integer argument encoding at {self.context.get_path(integer_argument_type)}: expected IntegerDataEncodingType. Other encoding elements for IntegerArgumentType are not implemented yet."
            )

        return EncodingInfo(
            bits=bits,
            encoding=encoding,
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, binary_argument_type: xtce.BinaryArgumentType) -> EncodingInfo:
        """Extract encoding information from a BinaryArgumentType definition."""
        # Parse binary encoding
        if enc := binary_argument_type.binary_data_encoding:
            # TODO add support for variable length encoding
            bits = (
                enc.size_in_bits.fixed_value
                if enc.size_in_bits and enc.size_in_bits.fixed_value
                else 0
            )
            byte_order = map_byte_order(enc.byte_order)
            reverse_bits = map_bit_order(enc.bit_order)

        else:
            raise NotImplementedError(
                f"Unsupported binary argument encoding at {self.context.get_path(binary_argument_type)}: expected BinaryDataEncodingType. Other encoding elements for BinaryArgumentType are not implemented yet."
            )

        return EncodingInfo(
            bits=bits,
            encoding="binary",
            byte_order=byte_order,
            reverse_bits=reverse_bits,
        )

    @_extract_encoding.register
    def _(self, float_argument_type: xtce.FloatArgumentType) -> EncodingInfo:
        """Extract encoding information from a FloatArgumentType definition."""
        # Parse float encoding
        if enc := float_argument_type.float_data_encoding:
            bits = enc.size_in_bits.value
            encoding = enc.encoding.value.lower()
            byte_order = map_byte_order(enc.byte_order)
            reverse_bits = map_bit_order(enc.bit_order)

        else:
            raise NotImplementedError(
                f"Unsupported float argument encoding at {self.context.get_path(float_argument_type)}: expected FloatDataEncodingType. Other encoding elements for FloatArgumentType are not implemented yet."
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
        # TODO add support for one_string_value and zero_string_value
        # TODO add support for bit length > 1
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


class FieldBuilder:
    """Pydantic Field constructor."""

    # TODO potentially add a singledispatchmethod that handles all field arguments for each specific type

    def __init__(self, arg: EffectiveArgument, type_def: AnyArgumentType):
        """Initialize the FieldBuilder."""
        self.arg = arg
        self.type_def = type_def
        self.raw_name = unwrap(type_def.name)

        self.py_type = "int"
        self.req_import: str | None = None
        self.field_kwargs: dict[str, str] = {}

    def _resolve_python_type(self) -> None:
        """Determine the base Python type and any required imports."""
        if isinstance(self.type_def, xtce.FloatArgumentType):
            self.py_type = "float"

        elif isinstance(self.type_def, xtce.StringArgumentType):
            self.py_type = "str"

        elif isinstance(self.type_def, xtce.BinaryArgumentType):
            self.py_type = "bytes"

        elif isinstance(self.type_def, xtce.EnumeratedArgumentType):
            enum_name = sanitize_class_name(unwrap(self.type_def.name))
            self.py_type = f"Annotated[Union[{enum_name}, int, str], BeforeValidator(enum_validator({enum_name}))]"
            self.req_import = f"from .enums import {enum_name}"

        # TODO support remaining types

    def _resolve_metadata(self) -> None:
        """Extract metadata from the XTCE type definition."""
        # Description
        desc = get_description(self.type_def)
        if desc:
            self.field_kwargs["description"] = f'"{desc}"'

        # Alias
        if self.raw_name != self.arg.clean_name:
            self.field_kwargs["alias"] = f'"{self.arg.name}"'

        # Range
        # TODO figure out a better way to do this
        if (
            isinstance(self.type_def, xtce.IntegerArgumentType)
            and self.type_def.valid_range_set
        ):
            if len(self.type_def.valid_range_set.valid_range) > 1:
                raise NotImplementedError(
                    f"Multiple valid ranges are not yet supported at {self.type_def.name}."
                )
            if (
                min_val := self.type_def.valid_range_set.valid_range[0].min_inclusive
            ) is not None:
                self.field_kwargs["ge"] = str(min_val)
            if (
                max_val := self.type_def.valid_range_set.valid_range[0].max_inclusive
            ) is not None:
                self.field_kwargs["le"] = str(max_val)

        elif (
            isinstance(self.type_def, xtce.FloatArgumentType)
            and self.type_def.valid_range_set
        ):
            if len(self.type_def.valid_range_set.valid_range) > 1:
                raise NotImplementedError(
                    f"Multiple valid ranges are not yet supported at {self.type_def.name}."
                )

            # Checking for all four types is valid because semantic validation will only allow inclusive or exclusive, not both
            if (
                min_val := self.type_def.valid_range_set.valid_range[0].min_inclusive
            ) is not None:
                self.field_kwargs["ge"] = str(min_val)
            if (
                max_val := self.type_def.valid_range_set.valid_range[0].max_inclusive
            ) is not None:
                self.field_kwargs["le"] = str(max_val)
            if (
                min_val := self.type_def.valid_range_set.valid_range[0].min_exclusive
            ) is not None:
                self.field_kwargs["gt"] = str(min_val)
            if (
                max_val := self.type_def.valid_range_set.valid_range[0].max_exclusive
            ) is not None:
                self.field_kwargs["lt"] = str(max_val)

    def build(self) -> PydanticField:
        """Compile the resolved data into a final PydanticField."""
        self._resolve_python_type()
        self._resolve_metadata()

        # Wrap in Annotated and Field if there is metadata
        if self.field_kwargs:
            kwargs_str = ", ".join(f"{k}={v}" for k, v in self.field_kwargs.items())

            if self.py_type.startswith("Annotated["):
                type_hint = self.py_type[:-1] + f", Field({kwargs_str})]"
            else:
                type_hint = f"Annotated[{self.py_type}, Field({kwargs_str})]"

        # Just the base type if no metadata
        else:
            type_hint = self.py_type

        return PydanticField(
            name=self.arg.clean_name,
            type_hint=type_hint,
            default=None,
            is_fixed=False,
            required_import=self.req_import,
        )
