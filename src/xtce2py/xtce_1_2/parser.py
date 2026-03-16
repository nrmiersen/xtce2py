"""XTCE version 1.2 parser module."""

from collections import defaultdict
from pathlib import Path

from xsdata.formats.dataclass.parsers import XmlParser
from xsdata.formats.dataclass.parsers.config import ParserConfig

from xtce2py.utils import format_identifier, path_to_package
from xtce2py.xtce import (
    BaseXtceParser,
    CommandViewModel,
    EnumViewModel,
    SystemContext,
    XtceMetadataContext,
    XtceValidationError,
    unwrap,
)
from xtce2py.xtce_1_2 import bindings as xtce
from xtce2py.xtce_1_2.context import EffectiveArgument, EffectiveCommand, ExecutionStep
from xtce2py.xtce_1_2.processor import CommandProcessor, EnumProcessor
from xtce2py.xtce_1_2.utils import parse_match_criteria
from xtce2py.xtce_1_2.validator import SemanticValidator


class XtceParser(BaseXtceParser):
    """Parser for XTCE version 1.2 files."""

    def __init__(self, xml: Path) -> None:
        """Initialize the parser with default configuration.

        Args:
            xml (Path): Path to the XTCE XML file.

        """
        self.xml = xml

        self._xtce_version = "1.2"
        self._metadata: XtceMetadataContext = XtceMetadataContext()
        self._package_cache: set[str] = set()
        self._effective_commands: dict[str, EffectiveCommand] = {}
        self._space_system: xtce.SpaceSystem

        self._sys_context = SystemContext()
        self._cmd_processor = CommandProcessor(self._sys_context)
        self._enum_processor = EnumProcessor(self._sys_context)

        self._cmd_enums: dict[str, list[EnumViewModel]] = defaultdict(list)
        self._tlm_enums: dict[str, list[EnumViewModel]] = defaultdict(list)

    @property
    def xtce_version(self) -> str:
        """Return the XTCE version."""
        return self._xtce_version

    @property
    def metadata(self) -> XtceMetadataContext:
        """Return the extracted metadata."""
        return self._metadata

    @property
    def package_list(self) -> set[str]:
        """Return the set of all unique Python package names derived from the SpaceSystem hierarchy."""
        if not self._package_cache:
            for path in self._effective_commands.keys():
                pkg = path_to_package(path)
                if pkg:
                    self._package_cache.add(pkg)

        return self._package_cache

    @property
    def effective_commands(self) -> dict[str, EffectiveCommand]:
        """Return the set of all effective commands."""
        return self._effective_commands

    def process_command(self, cmd: EffectiveCommand) -> CommandViewModel:
        """Return the CommandViewModel for a given EffectiveCommand, which is used by the Jinja2 templates.

        Args:
            cmd (EffectiveCommand): The effective command to process.

        Returns:
            CommandViewModel: The view model containing all data needed to generate the command class.

        """
        return self._cmd_processor.process(cmd)

    def parse(self) -> None:
        """Parse the XTCE file.

        Args:
            xml (Path): Path to the XTCE XML file.

        """
        config = ParserConfig(fail_on_unknown_properties=False)
        parser = XmlParser(config=config)

        self._space_system: xtce.SpaceSystem = parser.from_path(
            self.xml, xtce.SpaceSystem
        )

        self._index_space_system(self._space_system)
        self._set_metadata()

    def validate(self) -> tuple[bool, list[XtceValidationError]]:
        """Run semantic validation checks on the parsed XTCE data.

        Returns:
            tuple[bool, list[XtceValidationError]]: A tuple containing a boolean indicating if the data is valid and a list of validation errors if not.

        """
        validator = SemanticValidator(self._space_system, self._sys_context)
        return validator.validate()

    def process(self) -> None:
        """Process the parsed XTCE data into effective commands and view models."""
        self._process_all_types()
        self._process_all_commands()

    def _index_space_system(
        self, space_system: xtce.SpaceSystem, parent_path: str = ""
    ) -> None:
        """Index the SpaceSystem into the SystemContext for easy lookup during processing. This is a recursive function that walks the entire SpaceSystem hierarchy.

        Args:
            space_system (xtce.SpaceSystem): The current SpaceSystem to index.
            parent_path (str): The path of the parent SpaceSystem.

        """
        # Set the base path
        current_path = f"{parent_path}/{space_system.name}"

        # Register command metadata
        if space_system.command_meta_data:
            cmd_metadata = space_system.command_meta_data

            # Register all argument types
            if cmd_metadata.argument_type_set:
                for arg_type in cmd_metadata.argument_type_set.entries:
                    full_name = f"{current_path}/{arg_type.name}"
                    self._sys_context.register(full_name, arg_type)
                    self._sys_context.register_python_name(
                        arg_type, format_identifier(unwrap(arg_type.name))
                    )

            # Register all meta commands
            if cmd_metadata.meta_command_set:
                for cmd in cmd_metadata.meta_command_set.meta_command:
                    full_name = f"{current_path}/{cmd.name}"
                    self._sys_context.register(full_name, cmd)
                    self._sys_context.register_python_name(
                        cmd, format_identifier(unwrap(cmd.name))
                    )

        # Register telemetry metadata
        if space_system.telemetry_meta_data:
            tlm_metadata = space_system.telemetry_meta_data

            # Register all parameter types
            if tlm_metadata.parameter_type_set:
                for param_type in getattr(
                    tlm_metadata.parameter_type_set, "entries", []
                ):
                    self._sys_context.register(
                        f"{current_path}/{param_type.name}", param_type
                    )
                    self._sys_context.register_python_name(
                        param_type, format_identifier(unwrap(param_type.name))
                    )

            # Register all sequence containers
            if tlm_metadata.container_set:
                for container in tlm_metadata.container_set.sequence_container:
                    self._sys_context.register(
                        f"{current_path}/{container.name}", container
                    )
                    self._sys_context.register_python_name(
                        container, format_identifier(unwrap(container.name))
                    )

        # Recurse into child SpaceSystems
        for child in space_system.space_system:
            self._index_space_system(child, current_path)

    def _process_all_types(self) -> None:
        """Process all registered types into ViewModels."""
        for path, obj in self._sys_context.definitions.items():
            xtce_pkg = path_to_package(path)

            if isinstance(obj, xtce.EnumeratedArgumentType):
                vm = self._enum_processor.process(obj)
                self._cmd_enums[xtce_pkg].append(vm)

            elif isinstance(obj, xtce.EnumeratedParameterType):
                vm = self._enum_processor.process(obj)
                self._tlm_enums[xtce_pkg].append(vm)

            # TODO handle aggregates

    def _process_all_commands(self):
        """Process all registered commands into EffectiveCommands."""
        for path, obj in list(self._sys_context.definitions.items()):
            if isinstance(obj, xtce.MetaCommandType):
                self._process_command(path, obj)

    def _process_command(
        self, path: str, meta_command_obj: xtce.MetaCommandType
    ) -> None:
        """Process a single MetaCommandType into an EffectiveCommand, resolving inheritance and flattening execution steps.

        Args:
            path (str): The full path of the MetaCommand in the SpaceSystem hierarchy.
            meta_command_obj (xtce.MetaCommandType): The MetaCommandType object to process.

        """
        # Resolve command chain
        chain_tuples = self._get_command_chain(meta_command_obj, path)

        # Initialize the EffectiveCommand with required info
        effective_cmd = EffectiveCommand(
            name=unwrap(meta_command_obj.name),
            path=path,
            is_abstract=meta_command_obj.abstract,
        )

        # Determine the parent if one exists
        if len(chain_tuples) > 1:
            parent_path, _ = chain_tuples[-2]
            effective_cmd.parent_path = parent_path

        assignments = {}
        for anc_path, ancestor in chain_tuples:
            # Get all arguments from ancestors
            if ancestor.argument_list:
                effective_cmd.all_arguments.extend(
                    [EffectiveArgument(arg) for arg in ancestor.argument_list.argument]
                )

            # Get all own arguments from the current command
            if anc_path == path and ancestor.argument_list:
                effective_cmd.own_arguments.extend(
                    [EffectiveArgument(arg) for arg in ancestor.argument_list.argument]
                )

            # Get argument assignments
            if ancestor.base_meta_command:
                if ancestor.base_meta_command.argument_assignment_list:
                    for assignment in ancestor.base_meta_command.argument_assignment_list.argument_assignment:
                        assignments[assignment.argument_name] = (
                            assignment.argument_value
                        )

            # Flatten entries from command containers into execution steps
            if ancestor.command_container and ancestor.command_container.entry_list:
                ordered_entries = ancestor.command_container.entry_list.entries
                for entry in ordered_entries:
                    condition_str = None
                    if entry.include_condition:
                        condition_str = parse_match_criteria(
                            entry.include_condition, self._sys_context
                        )

                    step = ExecutionStep(item=entry, python_condition=condition_str)
                    effective_cmd.execution_steps.append(step)

        effective_cmd.argument_assignments = assignments

        self._effective_commands[path] = effective_cmd

    def _set_metadata(self) -> None:
        """Extract metadata from the SpaceSystem object."""
        # Set defaults
        name = self._space_system.name or "unknown"
        description = self._space_system.long_description or ""
        version = date = classification = None
        authors, notes, history = [], [], []

        # Overwrite values if header exists
        header = self._space_system.header
        if header:
            version = header.version
            date = header.date
            classification = header.classification

            authors = header.author_set.author if header.author_set else []
            notes = header.note_set.note if header.note_set else []
            history = header.history_set.history if header.history_set else []

        self._metadata = XtceMetadataContext(
            name=name,
            description=description,
            version=version,
            date=date,
            classification=classification,
            authors=authors,
            notes=notes,
            history=history,
        )

    def _get_command_chain(
        self, cmd_obj: xtce.MetaCommandType, current_path: str
    ) -> list[tuple[str, xtce.MetaCommandType]]:
        """Get the chain of MetaCommands from the root ancestor down to the given command.

        Args:
            cmd_obj (xtce.MetaCommandType): The command to get the chain for.
            current_path (str): The path of the command in the SpaceSystem hierarchy, used for resolving references.

        Returns:
            list[tuple[str, xtce.MetaCommandType]]: A list of tuples containing the path and MetaCommandType object for each command in the chain, ordered from root ancestor to the given command.

        """
        chain = [(current_path, cmd_obj)]
        cursor = cmd_obj

        while True:
            if cursor.base_meta_command and cursor.base_meta_command.meta_command_ref:
                ref_str = cursor.base_meta_command.meta_command_ref

                # Get the path and object of the parent command
                parent_path, parent_obj = self._sys_context.resolve(
                    ref_str, scope=current_path
                )
                chain.insert(0, (parent_path, parent_obj))

                # Move up the tree
                cursor = parent_obj
                current_path = parent_path
            else:
                break

        return chain
