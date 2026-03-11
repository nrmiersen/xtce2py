"""Base processor."""

from abc import ABC, abstractmethod
from typing import Any


class BaseProcessor(ABC):
    """Abstract base processor."""

    @abstractmethod
    def __init__(self):
        """Initialize the base processor."""
        pass

    @abstractmethod
    def process(self) -> Any:
        """Process the input data and produce the output view model."""
        pass
