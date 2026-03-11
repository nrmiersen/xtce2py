"""Base XTCE parser."""

from abc import ABC, abstractmethod

from xtce2py.xtce.context import (
    BaseEffectiveCommand,
    CommandViewModel,
    XtceMetadataContext,
)
from xtce2py.xtce.validator import XtceValidationError


class BaseXtceParser(ABC):
    """Abstract base XTCE parser."""

    @property
    @abstractmethod
    def xtce_version(self) -> str:
        """Return the XTCE version."""
        pass

    @property
    @abstractmethod
    def metadata(self) -> XtceMetadataContext:
        """Return the extracted metadata."""
        pass

    @property
    @abstractmethod
    def package_list(self) -> set[str]:
        """Return the set of all unique Python package names derived from the SpaceSystem hierarchy."""
        pass

    @property
    @abstractmethod
    def effective_commands(self) -> dict[str, BaseEffectiveCommand]:
        """Return the set of all effective commands."""
        pass

    @abstractmethod
    def __init__(self) -> None:
        """Initialize the base parser."""
        pass

    @abstractmethod
    def parse(self) -> None:
        """Parse the XTCE file."""
        pass

    @abstractmethod
    def validate(self) -> tuple[bool, list[XtceValidationError]]:
        """Run semantic validation checks on the parsed XTCE data.

        Returns:
            tuple[bool, list[XtceValidationError]]: A tuple containing a boolean indicating if the data is valid and a list of validation errors if not.

        """
        pass

    @abstractmethod
    def process(self) -> None:
        """Process the parsed XTCE data into effective commands and view models."""
        pass

    @abstractmethod
    def process_command(self, cmd: BaseEffectiveCommand) -> CommandViewModel:
        """Return the CommandViewModel for a given EffectiveCommand, which is used by the Jinja2 templates.

        Args:
            cmd (EffectiveCommand): The effective command to process.

        Returns:
            CommandViewModel: The view model containing all data needed to generate the command class.

        """
        pass
