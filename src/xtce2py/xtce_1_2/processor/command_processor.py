"""Command processor."""

import re
from typing import Any

from xtce2py.xtce import (
    BaseProcessor,
    CodecRecipeItem,
    CommandViewModel,
    PydanticField,
    SystemContext,
    unwrap,
)
from xtce2py.xtce_1_2.bindings import models as xtce
from xtce2py.xtce_1_2.context import EffectiveCommand


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
                enc_info = self._extract_encoding(type_def)

                steps.append(
                    CodecRecipeItem(
                        name=arg_name,
                        value_src=f"self.{_sanitize(arg_name)}",
                        bits=enc_info["bits"],
                        encoding=enc_info["encoding"],
                        byte_order=enc_info["byte_order"],
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

    def _extract_encoding(self, type_def) -> dict[str, Any]:
        info = {
            "bits": 0,
            "encoding": "unsigned",
            "byte_order": "big",
            "reverse_bits": False,
        }

        if isinstance(type_def, xtce.StringArgumentType):
            if type_def.string_data_encoding:
                enc = type_def.string_data_encoding

                if enc.size_in_bits:
                    if enc.size_in_bits.fixed:
                        info["bits"] = enc.size_in_bits.fixed.fixed_value

                enc_val = (
                    enc.encoding.value
                    if hasattr(enc.encoding, "value")
                    else str(enc.encoding)
                )
                info["encoding"] = enc_val.lower().replace("_", "").replace("-", "")
                info["byte_order"] = self._map_endian(enc.byte_order)

        elif isinstance(type_def, xtce.IntegerArgumentType):
            if type_def.integer_data_encoding:
                enc = type_def.integer_data_encoding
                info["bits"] = enc.size_in_bits

                enc_val = (
                    enc.encoding.value
                    if hasattr(enc.encoding, "value")
                    else str(enc.encoding)
                )
                info["encoding"] = enc_val.lower()
                info["byte_order"] = self._map_endian(enc.byte_order)

            elif hasattr(type_def, "size_in_bits"):
                info["bits"] = type_def.size_in_bits

                is_signed = getattr(type_def, "signed", True)
                info["encoding"] = "signed" if is_signed else "unsigned"

                info["byte_order"] = "big"

        elif isinstance(type_def, xtce.EnumeratedArgumentType):
            if type_def.integer_data_encoding:
                enc = type_def.integer_data_encoding
                info["bits"] = enc.size_in_bits

                enc_val = (
                    enc.encoding.value
                    if hasattr(enc.encoding, "value")
                    else str(enc.encoding)
                )
                info["encoding"] = enc_val.lower()
                info["byte_order"] = self._map_endian(enc.byte_order)

        elif isinstance(type_def, xtce.FloatArgumentType):
            if type_def.float_data_encoding:
                enc = type_def.float_data_encoding
                info["bits"] = (
                    int(enc.size_in_bits.value)
                    if hasattr(enc.size_in_bits, "value")
                    else 32
                )
                info["encoding"] = "float"
                info["byte_order"] = self._map_endian(enc.byte_order)

            elif hasattr(type_def, "size_in_bits"):
                val = type_def.size_in_bits
                info["bits"] = int(val.value) if hasattr(val, "value") else 32
                info["encoding"] = "float"
                info["byte_order"] = "big"

        elif isinstance(type_def, xtce.BooleanArgumentType):
            info["bits"] = 1
            info["encoding"] = "unsigned"

        if info["bits"] == 0 and hasattr(type_def, "base_type") and type_def.base_type:
            try:
                _, parent = self.context.resolve(type_def.base_type, scope="")
                parent_info = self._extract_encoding(parent)
                if info["bits"] == 0:
                    info["bits"] = parent_info["bits"]
                if info["encoding"] == "unsigned":
                    info["encoding"] = parent_info["encoding"]
            except KeyError:
                pass

        return info

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

    def _map_endian(self, xtce_endian) -> str:
        s = str(xtce_endian).lower()
        if "least" in s:
            return "little"
        return "big"


def _sanitize(name: str) -> str:
    return name.replace(" ", "_").replace("-", "_").lower()


def _sanitize_class_name(name: str, is_abstract: bool = False) -> str:
    clean = name.replace(" ", "").replace("-", "_")
    base = clean[0].upper() + clean[1:]
    return f"_{base}" if is_abstract else base
