"""XTCE version 1.1 parser module."""

import logging
from pathlib import Path
from typing import Any, Generator, Optional

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from xtce2py._validation import (
    ValidationResult,
    ValidationSeverity,
    XtceSemanticValidationError,
)
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

log = logging.getLogger(__name__)


class XtceParser:
    """Parser for XTCE version 1.1 files."""

    def __init__(self, xml: Path):
        """Initialize the parser with default configuration."""
        self.parameter_map = {}
        self.parameter_type_map = {}
        self.root_containers = {}
        self.nodes = {}

        # Parse the XTCE file
        self.space_system = self._parse_xtce(xml)
        self.metadata = self._get_metadata()

        # Build system hierarchy and maps
        self.all_systems = list(self._get_all_space_systems(self.space_system))
        self.root_space_system = self.all_systems[0]
        self.sub_space_systems = self.all_systems[1:]
        self._map_parameters()
        self._build_container_tree()

        # Perform semantic validation
        self.errors, self.warnings = self._validate()
        if self.errors:
            raise XtceSemanticValidationError(self.errors)

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

    def generate_parser_context(self) -> ParserContext:
        """Generate context data for the parser template."""
        sequence_containers = self._get_sequence_containers()
        parent_container_names = set(self.nodes.keys())

        container_details_map = {}
        for container in sequence_containers:
            container_name = container.name or "unknown"

            container_details_map[container_name] = ContainerDetailsContext(
                python_name=container_name,
                is_abstract=getattr(container, "abstract", False),
                has_children=(container_name in parent_container_names),
                restrictions=self._get_container_restrictions(container),
                parameters=self._get_container_parameters(container),
            )

        concrete_container_names: set[str] = {
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
            self._get_sequence_containers()
        )

        for container in sequence_containers:
            description = self._get_description(container)

            entries = []
            if container.entry_list and container.entry_list.parameter_ref_entry:
                for entry in container.entry_list.parameter_ref_entry:
                    parameter = self.parameter_map.get(entry.parameter_ref)
                    entries.append(
                        self._get_parameter_context(parameter) if parameter else {}
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

    def _parse_xtce(self, xml: Path) -> SpaceSystem:
        """Parse the XTCE file into a SpaceSystem object."""
        config = ParserConfig(fail_on_unknown_properties=False)
        parser = XmlParser(config=config)
        return parser.from_path(xml, SpaceSystem)

    def _get_metadata(self) -> XtceMetadataContext:
        """Extract metadata from the SpaceSystem object."""
        name = self.space_system.name or "unknown"
        description = self._get_description(self.space_system)

        version = date = classification = None
        authors, notes, history = [], [], []

        header = getattr(self.space_system, "header", None)
        if header:
            version = getattr(header, "version", None)
            date = getattr(header, "date", None)
            classification = getattr(header, "classification", None)

            author_set = getattr(header, "author_set", None)
            if author_set:
                authors = getattr(author_set, "author", [])
            notes_container = getattr(header, "note_set", None)
            if notes_container:
                notes = getattr(notes_container, "note", [])
            history_container = getattr(header, "history_set", None)
            if history_container:
                history = getattr(history_container, "history", [])

        return XtceMetadataContext(
            name=name,
            description=description,
            version=version,
            date=date,
            classification=classification,
            authors=authors,
            notes=notes,
            history=history,
        )

    def _get_all_space_systems(
        self,
        system: SpaceSystem,
    ) -> Generator[SpaceSystem, None, None]:
        """Recursively traverse a SpaceSystem tree and yields each system."""
        yield system
        if system.space_system:
            for child_system in system.space_system:
                yield from self._get_all_space_systems(child_system)

    def _map_parameters(self):
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

    def _build_container_tree(self):
        """Build a hierarchical tree of containers from a flat list."""
        all_container_objects = self._get_sequence_containers()

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

    def _validate(self) -> tuple[list[ValidationResult], list[ValidationResult]]:
        """Orchestrates all semantic validation checks."""
        errors, warnings = [], []
        for result in self._run_all_validators():
            if result.severity == ValidationSeverity.ERROR:
                errors.append(result)
            else:
                warnings.append(result)
        return errors, warnings

    def _run_all_validators(self) -> Generator[ValidationResult, None, None]:
        """Run all validator methods and yield results."""
        yield from self._validate_reference_integrity()
        yield from self._validate_completeness()
        yield from self._validate_data_encodings()
        yield from self._validate_uniqueness()

    def _validate_reference_integrity(self) -> Generator[ValidationResult, None, None]:
        """Check that all parameter and container references are valid."""
        log.debug("Starting reference integrity validation...")
        for param_name, param_obj in self.parameter_map.items():
            type_ref = getattr(param_obj, "parameter_type_ref", None)
            if type_ref not in self.parameter_type_map:
                log.debug(
                    f"- FAILED: Parameter '{param_name}' has broken reference to '{type_ref}'."
                )
                yield ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"Parameter '{param_name}' references an unknown ParameterType '{type_ref}'.",
                    location="ParameterSet",
                )

        all_containers = self._get_sequence_containers()
        all_container_names = {c.name for c in all_containers if c.name}

        for container in all_containers:
            # Check Container -> BaseContainer references
            if (
                container.base_container
                and container.base_container.container_ref not in all_container_names
            ):
                yield ValidationResult(
                    severity=ValidationSeverity.ERROR,
                    message=f"BaseContainer reference to '{container.base_container.container_ref}' not found.",
                    location=f"Container '{container.name}'",
                )

            # Check Container -> Parameter references in its EntryList
            entry_list: EntryListType | None = getattr(container, "entry_list", None)
            if entry_list:
                param_refs: list[ParameterRefEntryType] = getattr(
                    entry_list, "parameter_ref_entry", []
                )
                for entry in param_refs:
                    if entry.parameter_ref not in self.parameter_map:
                        yield ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            message=f"Contains a reference to an unknown Parameter '{entry.parameter_ref}'.",
                            location=f"Container '{container.name}'",
                        )
        log.debug("Finished reference integrity validation.")

    def _validate_completeness(self) -> Generator[ValidationResult, None, None]:
        """Check for unused parameters or types (generates warnings)."""
        log.debug("Starting completeness validation...")
        # Find all referenced parameters
        referenced_params = set()
        for container in self._get_sequence_containers():
            entry_list: EntryListType | None = getattr(container, "entry_list", None)
            if entry_list:
                for entry in getattr(entry_list, "parameter_ref_entry", []):
                    referenced_params.add(entry.parameter_ref)

        # Compare defined parameters vs. referenced parameters
        defined_params = set(self.parameter_map.keys())
        unused_params = defined_params - referenced_params
        for param_name in unused_params:
            yield ValidationResult(
                severity=ValidationSeverity.WARNING,
                message=f"Parameter '{param_name}' is defined but not used in any container.",
                location="ParameterSet",
            )
        log.debug("Finished completeness validation.")

    def _validate_data_encodings(self) -> Generator[ValidationResult, None, None]:
        """Validate the consistency of DataEncoding definitions for all ParameterTypes."""
        log.debug("Starting data encoding validation...")
        if not self.parameter_type_map:
            return

        for type_name, param_type in self.parameter_type_map.items():
            if isinstance(param_type, ParameterTypeSetType.StringParameterType):
                pass
            if isinstance(param_type, ParameterTypeSetType.EnumeratedParameterType):
                pass
            elif isinstance(param_type, ParameterTypeSetType.IntegerParameterType):
                encoding = getattr(param_type, "integer_data_encoding", None)
                if not encoding:
                    continue

                param_size_bits = getattr(param_type, "size_in_bits", None)
                encoding_size_bits = getattr(encoding, "size_in_bits", None)

                effective_size_bits = encoding_size_bits or param_size_bits
                if not effective_size_bits:
                    continue

                # Check if encoding size exceeds parameter size
                if (
                    param_size_bits
                    and encoding_size_bits
                    and encoding_size_bits > param_size_bits
                ):
                    yield ValidationResult(
                        severity=ValidationSeverity.ERROR,
                        message=f"Encoding size ({encoding_size_bits} bits) exceeds parameter size ({param_size_bits} bits).",
                        location=f"ParameterType '{type_name}'",
                    )

                # Check ByteOrderList if it exists
                byte_order_list = getattr(encoding, "byte_order_list", None)
                if byte_order_list:
                    byte_elements = getattr(byte_order_list, "byte", [])
                    expected_bytes = (effective_size_bits + 7) // 8
                    actual_bytes = len(byte_elements)

                    if actual_bytes > expected_bytes:
                        yield ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            message=f"ByteOrderList has {actual_bytes} bytes, but encoding size ({effective_size_bits} bits) only requires {expected_bytes}.",
                            location=f"ParameterType '{type_name}'",
                        )

                    # Check significance values for each byte in the list
                    for i, byte_elem in enumerate(byte_elements):
                        significance = getattr(byte_elem, "byte_significance", None)
                        if significance is not None:
                            if significance >= expected_bytes:
                                yield ValidationResult(
                                    severity=ValidationSeverity.ERROR,
                                    message=f"Byte at index {i} has significance {significance}, which exceeds the maximum allowed value of {expected_bytes - 1}.",
                                    location=f"ParameterType '{type_name}'",
                                )
                            if significance < 0:
                                yield ValidationResult(
                                    severity=ValidationSeverity.ERROR,
                                    message=f"Byte at index {i} has an invalid negative significance of {significance}.",
                                    location=f"ParameterType '{type_name}'",
                                )
            elif isinstance(param_type, ParameterTypeSetType.BinaryParameterType):
                pass
            elif isinstance(param_type, ParameterTypeSetType.FloatParameterType):
                pass
            elif isinstance(param_type, ParameterTypeSetType.BooleanParameterType):
                pass
            elif isinstance(param_type, ParameterTypeSetType.RelativeTimeParameterType):
                pass
            elif isinstance(param_type, AbsoluteTimeDataType):
                pass
            elif isinstance(param_type, ArrayDataTypeType):
                pass
            elif isinstance(param_type, AggregateDataType):
                pass
        log.debug("Finished data encoding validation.")

    def _validate_uniqueness(self) -> Generator[ValidationResult, None, None]:
        """Check for duplicate names of Parameters, ParameterTypes, and Containers within each SpaceSystem."""
        log.debug("Starting uniqueness validation...")
        for system in self.all_systems:
            location = f"SpaceSystem '{system.name}'"

            # Check for duplicate Parameters
            if system.telemetry_meta_data and system.telemetry_meta_data.parameter_set:
                seen_params = set()
                for param in system.telemetry_meta_data.parameter_set.parameter:
                    if param.name in seen_params:
                        yield ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            message=f"Duplicate Parameter found: '{param.name}'",
                            location=location,
                        )
                    seen_params.add(param.name)

            # Check for duplicate ParameterTypes
            if (
                system.telemetry_meta_data
                and system.telemetry_meta_data.parameter_type_set
            ):
                seen_types = set()
                type_set = system.telemetry_meta_data.parameter_type_set
                all_types = (
                    type_set.string_parameter_type
                    + type_set.enumerated_parameter_type
                    + type_set.integer_parameter_type
                    + type_set.float_parameter_type
                    + type_set.boolean_parameter_type
                    + type_set.relative_time_parameter_type
                    + type_set.absolute_time_parameter_type
                    + type_set.array_parameter_type
                    + type_set.aggregate_parameter_type
                )
                for p_type in all_types:
                    if p_type.name in seen_types:
                        yield ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            message=f"Duplicate ParameterType found: '{p_type.name}'",
                            location=location,
                        )
                    seen_types.add(p_type.name)

            # Check for duplicate Containers
            if system.telemetry_meta_data and system.telemetry_meta_data.container_set:
                seen_containers = set()
                for (
                    container
                ) in system.telemetry_meta_data.container_set.sequence_container:
                    if container.name in seen_containers:
                        yield ValidationResult(
                            severity=ValidationSeverity.ERROR,
                            message=f"Duplicate SequenceContainer found: '{container.name}'",
                            location=location,
                        )
                    seen_containers.add(container.name)
        log.debug("Finished uniqueness validation.")

    def _get_sequence_containers(self) -> list[SequenceContainerType]:
        """Get all sequence containers from the SpaceSystem."""
        return (
            self.space_system.telemetry_meta_data.container_set.sequence_container
            if self.space_system
            and self.space_system.telemetry_meta_data
            and self.space_system.telemetry_meta_data.container_set
            else []
        )

    @staticmethod
    def _get_description(obj: Any) -> Optional[str]:
        """Extract a sanitized description from an object."""
        long_desc = getattr(obj, "long_description", None)
        short_desc = getattr(obj, "short_description", None)

        description = (
            sanitize_description(long_desc) or sanitize_description(short_desc) or None
        )
        return description

    def _get_parameter_context(
        self, parameter: ParameterSetType.Parameter
    ) -> Optional[ParameterContext]:
        """Return a ParameterContext for the given parameter name."""
        param_type_ref = parameter.parameter_type_ref
        param_type_obj = self.parameter_type_map.get(param_type_ref)
        if not param_type_obj:
            return None

        return ParameterContext(
            name=parameter.name or "unknown",
            description=self._get_description(parameter),
            python_type=XTCE_PARAMETER_TYPE_MAP.get(type(param_type_obj), Any),
            encoding=self._get_encoding_context(param_type_obj),
        )

    def _get_encoding_context(
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

    def _get_container_restrictions(self, container) -> list[RestrictionContext]:
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

    def _get_container_parameters(self, container) -> list[ParameterContext]:
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

            parameters.append(
                ParameterContext(
                    name=(param_ref),
                    python_type=XTCE_PARAMETER_TYPE_MAP.get(type(param_type_obj), Any),
                    encoding=self._get_encoding_context(param_type_obj),
                )
            )
        return parameters
