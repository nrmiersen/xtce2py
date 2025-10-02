"""XTCE version 1.1 parser module."""

from pathlib import Path
from typing import Any, Generator, Optional

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from xtce2py.context_models import (
    ModelContext,
    ModelsContext,
    ParserContext,
    XtceMetadataContext,
)
from xtce2py.utils import get_field_name, sanitize_description
from xtce2py.xtce_1_1 import *
from xtce2py.xtce_common.context_models import (
    ContainerDetailsContext,
    EncodingContext,
    ParameterContext,
    RestrictionContext,
)
from xtce2py.xtce_common.data_types import XTCE_ENCODING_MAP, XTCE_PARAMETER_TYPE_MAP


class XtceParser:
    """Parser for XTCE version 1.1 files."""

    def __init__(self, xml: Path):
        """Initialize the parser with default configuration."""
        self.root_containers = {}
        self.nodes = {}

        self.space_system = self._parse_xtce(xml)

        all_systems = list(self.get_all_space_systems(self.space_system))
        self.root_space_system = all_systems[0]
        self.sub_space_systems = all_systems[1:]

        self.map_parameters()
        self.build_container_tree()

    def _parse_xtce(self, xml: Path) -> SpaceSystem:
        """Parse the XTCE file and return a SpaceSystem object."""
        config = ParserConfig(fail_on_unknown_properties=False)
        parser = XmlParser(config=config)
        return parser.from_path(xml, SpaceSystem)

    def validate(self) -> list[str]:
        """Validate XTCE content for consistency and correctness.

        Returns:
            List of validation error messages. Empty list if no errors.

        """
        errors = []

        # TODO validate that parameters actually map to something

        # Validate parameter types
        if self.parameter_type_map:
            for type_name, param_type in self.parameter_type_map.items():
                # Validate integer parameter types
                if hasattr(param_type, "integer_data_encoding"):
                    encoding = param_type.integer_data_encoding
                    if encoding:
                        # Get sizes
                        param_size_bits = getattr(param_type, "size_in_bits", None)
                        encoding_size_bits = getattr(encoding, "size_in_bits", None)

                        # Validate byte order list
                        byte_order_list = getattr(encoding, "byte_order_list", None)
                        if byte_order_list:
                            byte_elements = getattr(byte_order_list, "byte", [])

                            if encoding_size_bits:
                                expected_bytes = (encoding_size_bits + 7) // 8
                                actual_bytes = len(byte_elements)

                                if actual_bytes > expected_bytes:
                                    errors.append(
                                        f"Parameter type '{type_name}': ByteOrderList has {actual_bytes} bytes "
                                        f"but encoding size ({encoding_size_bits} bits) only requires {expected_bytes} bytes"
                                    )

                                # Check byte significance values
                                for byte_elem in byte_elements:
                                    significance = getattr(
                                        byte_elem, "byte_significance", None
                                    )
                                    if significance is not None:
                                        if significance >= expected_bytes:
                                            errors.append(
                                                f"Parameter type '{type_name}': Byte significance {significance} "
                                                f"exceeds maximum allowed value {expected_bytes - 1}"
                                            )
                                        if significance < 0:
                                            errors.append(
                                                f"Parameter type '{type_name}': Byte significance {significance} cannot be negative"
                                            )

                        # Check parameter vs encoding size consistency
                        if (
                            param_size_bits
                            and encoding_size_bits
                            and encoding_size_bits > param_size_bits
                        ):
                            errors.append(
                                f"Parameter type '{type_name}': Encoding size ({encoding_size_bits} bits) "
                                f"exceeds parameter size ({param_size_bits} bits)"
                            )

        # TODO: Add more validation rules here as needed
        # - Container inheritance validation
        # - Parameter reference validation
        # - Restriction criteria validation

        return errors

    def get_space_system_hierarchy(self) -> dict[str, Any]:
        """Get space systems organized by their intended package structure."""
        hierarchy = {"root": self.root_space_system, "sub_systems": {}}

        for sub_system in self.sub_space_systems:
            if sub_system.name:
                module_name = (
                    sub_system.name.lower().replace(" ", "_").replace("-", "_")
                )
                hierarchy["sub_systems"][module_name] = sub_system

        return hierarchy

    def get_all_space_systems(
        self,
        system: SpaceSystem,
    ) -> Generator[SpaceSystem, None, None]:
        """Recursively traverse a SpaceSystem tree and yields each system."""
        yield system
        if system.space_system:
            for child_system in system.space_system:
                yield from self.get_all_space_systems(child_system)

    def map_parameters(self):
        """Create maps of parameters and parameter types."""
        if (
            self.space_system is None
            or self.space_system.telemetry_meta_data is None
            or self.space_system.telemetry_meta_data.parameter_set is None
            or self.space_system.telemetry_meta_data.parameter_type_set is None
        ):
            self.parameter_map = {}
            self.parameter_type_map = {}
            return

        self.parameter_map = {
            param.name: param
            for param in self.space_system.telemetry_meta_data.parameter_set.parameter
        }
        self.parameter_type_map = {}
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.string_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.enumerated_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.integer_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.binary_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.float_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.boolean_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.relative_time_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.absolute_time_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.array_parameter_type:
            self.parameter_type_map[p_type.name] = p_type
        for p_type in self.space_system.telemetry_meta_data.parameter_type_set.aggregate_parameter_type:
            self.parameter_type_map[p_type.name] = p_type

    def get_metadata(self) -> XtceMetadataContext:
        """Extract metadata from the SpaceSystem object."""
        name = self.space_system.name or "unknown"
        version = "1.0.0"
        if self.space_system.header:
            if self.space_system.header.version:
                version = self.space_system.header.version

        return XtceMetadataContext(
            name=name,
            version=version,
        )

    def get_sequence_containers(self) -> list[SequenceContainerType]:
        """Get all sequence containers from the SpaceSystem."""
        return (
            self.space_system.telemetry_meta_data.container_set.sequence_container
            if self.space_system
            and self.space_system.telemetry_meta_data
            and self.space_system.telemetry_meta_data.container_set
            else []
        )

    def get_encoding_context(
        self, param_type_obj: ParameterTypeSetType.IntegerParameterType
    ) -> EncodingContext:
        """Return an EncodingContext for the given parameter type."""

        def complete_byte_order_list(
            size_in_bits: int, byte_order_list: Optional[list[int]] = None
        ) -> list[int]:
            num_bytes = (size_in_bits + 7) // 8

            # Default to big-endian if no byte order is provided
            if not byte_order_list:
                return list(range(num_bytes - 1, -1, -1))

            if len(byte_order_list) == num_bytes:
                return byte_order_list

            # Fill in missing bytes with descending order of significance
            all_significances = set(range(num_bytes))
            used_significances = set(byte_order_list)
            missing_significances = list(all_significances - used_significances)
            completed_list = byte_order_list + missing_significances

            return completed_list

        if isinstance(param_type_obj, ParameterTypeSetType.IntegerParameterType):
            # Set defaults
            signed = param_type_obj.signed
            size_in_bits = param_type_obj.size_in_bits
            format_specifier = f"uint:{size_in_bits}"
            byte_order_list = complete_byte_order_list(size_in_bits)
            reverse_bits = False
            custom_byte_order = False
            custom_decoder = None

            # Override if encoding is specified
            encoding_obj = param_type_obj.integer_data_encoding
            if encoding_obj:
                size_in_bits = encoding_obj.size_in_bits
                format_specifier = f"uint:{size_in_bits}"
                byte_order_list = complete_byte_order_list(size_in_bits)
                reverse_bits = (
                    encoding_obj.bit_order
                    == DataEncodingTypeBitOrder.LEAST_SIGNIFICANT_BIT_FIRST
                )
                if encoding_obj.byte_order_list:
                    byte_order_list = [
                        byte.byte_significance
                        for byte in encoding_obj.byte_order_list.byte
                        if byte.byte_significance is not None
                    ]

                # Handle encoding types with custom decoders
                encoding_type = encoding_obj.encoding
                type_info = XTCE_ENCODING_MAP.get(encoding_type)
                custom_decoder = type_info.custom_decoder if type_info else None
            else:
                prefix = "int" if signed else "uint"
                format_specifier = f"{prefix}:{size_in_bits}"

        return EncodingContext(
            signed=signed,
            size_in_bits=size_in_bits,
            format_specifier=format_specifier,
            byte_order_list=byte_order_list,
            reverse_bits=reverse_bits,
            custom_byte_order=custom_byte_order,
            custom_decoder=custom_decoder,
        )

    def get_format_specifier(
        self,
        param_type_obj: ParameterTypeSetType.IntegerParameterType
        | ParameterTypeSetType.FloatParameterType,
    ) -> str:
        """Return the bitstring format string."""
        if isinstance(param_type_obj, ParameterTypeSetType.IntegerParameterType):
            signed = param_type_obj.signed
            encoding = param_type_obj.integer_data_encoding
            if encoding:
                prefix = (
                    "uint"
                    if encoding.encoding == IntegerDataEncodingTypeEncoding.UNSIGNED
                    else "int"
                )
                size_in_bits = encoding.size_in_bits
            else:
                prefix = "int" if signed else "uint"
                size_in_bits = param_type_obj.size_in_bits
            return f"{prefix}:{size_in_bits}"

        elif isinstance(param_type_obj, ParameterTypeSetType.FloatParameterType):
            encoding = param_type_obj.float_data_encoding
            return f"float:{encoding.size_in_bits}"

        return "not_implemented"

    def _get_restrictions_for_container(self, container) -> list[RestrictionContext]:
        """Safely extracts all restriction criteria for a given container."""
        restrictions = []
        criteria = getattr(
            getattr(container, "base_container", None), "restriction_criteria", None
        )
        if not criteria:
            return []

        if criteria.comparison:
            comp = criteria.comparison
            restrictions.append(
                RestrictionContext(
                    parameter_ref=comp.parameter_ref,
                    comparison_operator=comp.comparison_operator.value,
                    value=comp.value,
                )
            )

        if criteria.comparison_list:
            for comp in criteria.comparison_list.comparison:
                restrictions.append(
                    RestrictionContext(
                        parameter_ref=comp.parameter_ref,
                        comparison_operator=comp.comparison_operator.value,
                        value=comp.value,
                    )
                )

        return restrictions

    def _get_parameters_for_container(self, container) -> list[ParameterContext]:
        """Safely extracts and formats all parameters for a given container."""
        parameters = []
        entry_list = getattr(container, "entry_list", None)
        if not entry_list:
            return []

        param_ref_entries = getattr(entry_list, "parameter_ref_entry", [])

        for entry in param_ref_entries:
            param_ref = entry.parameter_ref

            param = self.parameter_map.get(param_ref)
            if not param:
                continue

            param_type_ref = param.parameter_type_ref
            param_type_obj = self.parameter_type_map.get(param_type_ref)
            if not param_type_obj:
                continue

            format_specifier = self.get_format_specifier(param_type_obj)

            encoding_context = self.get_encoding_context(param_type_obj)

            parameters.append(
                ParameterContext(
                    name=(param_ref),
                    python_type=XTCE_PARAMETER_TYPE_MAP.get(type(param_type_obj), Any),
                    format_specifier=format_specifier,
                )
            )
        return parameters

    def generate_parser_context(self) -> ParserContext:
        """Generate context data for the parser template.

        This is the high-level orchestrator.
        """
        sequence_containers = self.get_sequence_containers()
        parent_container_names = set(self.nodes.keys())

        container_details_map = {}
        for container in sequence_containers:
            container_name = container.name or "unknown"

            container_details_map[container_name] = ContainerDetailsContext(
                python_name=container_name,
                is_abstract=getattr(container, "abstract", False),
                has_children=(container_name in parent_container_names),
                restrictions=self._get_restrictions_for_container(container),
                parameters=self._get_parameters_for_container(container),
            )

        concrete_container_names = {
            name
            for name, details in container_details_map.items()
            if not details.is_abstract
        }

        return ParserContext(
            container_tree=self.root_containers.copy(),
            concrete_container_names=concrete_container_names,
            container_details_map=container_details_map,
        )

    def generate_model_context(self) -> Generator[ModelContext, None, None]:
        """Generate context for individual model containers."""
        sequence_containers: list[SequenceContainerType] = (
            self.get_sequence_containers()
        )

        for container in sequence_containers:
            # Handle potential None values for descriptions
            long_desc = container.long_description if container.long_description else ""
            short_desc = (
                container.short_description if container.short_description else ""
            )

            description = (
                sanitize_description(long_desc)
                or sanitize_description(short_desc)
                or ""
            )

            entries = []
            if container.entry_list and container.entry_list.parameter_ref_entry:
                for entry in container.entry_list.parameter_ref_entry:
                    parameter = self.parameter_map.get(entry.parameter_ref)
                    entries.append(
                        ParameterContext(
                            name=parameter.name,
                            format_specifier="",
                            python_type=XTCE_PARAMETER_TYPE_MAP.get(
                                type(
                                    self.parameter_type_map.get(
                                        parameter.parameter_type_ref
                                    )
                                ),
                                Any,
                            ),
                            description=sanitize_description(parameter.long_description)
                            or sanitize_description(parameter.short_description)
                            or "",
                        )
                    )

            yield ModelContext(
                name=container.name or "unknown",
                description=description,
                parent=(
                    container.base_container.container_ref
                    if container.base_container
                    and container.base_container.container_ref
                    else "PacketBase"
                ),
                entries=entries,
            )

    def build_container_tree(self):
        """Build a hierarchical tree of containers from a flat list."""
        all_container_objects = self.get_sequence_containers()

        inheritance_container_names = set()
        for c in all_container_objects:
            if c.base_container:
                inheritance_container_names.add(c.base_container.container_ref)
                inheritance_container_names.add(c.name)

        relevant_containers = [
            c for c in all_container_objects if c.name in inheritance_container_names
        ]

        # Create a node for every container
        self.nodes = {c.name: {} for c in relevant_containers}

        # Link children to their parents
        for container in relevant_containers:
            if container.base_container:
                parent_name = container.base_container.container_ref
                if parent_name in self.nodes:
                    self.nodes[parent_name][container.name] = self.nodes[container.name]
            else:
                self.root_containers[container.name] = self.nodes[container.name]
