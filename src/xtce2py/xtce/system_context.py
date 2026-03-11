"""System context class."""

import logging
from typing import Any

log = logging.getLogger(__name__)


class SystemContext:
    """Maintain a mapping of all XTCE definitions by their full absolute path."""

    def __init__(self):
        """Maintain a mapping of all XTCE definitions by their full absolute path."""
        self.definitions: dict[str, Any] = {}
        self._python_names: dict[int, str] = {}

    def register(self, path: str, obj: Any) -> None:
        """Register an object with its full absolute path.

        Args:
            path (str): The full absolute path of the object.
            obj (Any): The object to register.

        """
        if path in self.definitions:
            log.warning(f"Overwriting definition for {path}")

        self.definitions[path] = obj
        log.debug(
            f"Registered path {path} -> {type(obj).__name__}{'(' + getattr(obj, 'name', '') + ')' if hasattr(obj, 'name') else ''}"
        )

    def register_python_name(self, xtce_obj: object, name: str) -> None:
        """Register a Python name for an XTCE object.

        Args:
            xtce_obj (object): The XTCE object to register.
            name (str): The Python name to associate with the object.

        """
        self._python_names[id(xtce_obj)] = name
        log.debug(
            f"Registered Python name for {type(xtce_obj).__name__}{'(' + getattr(xtce_obj, 'name', '') + ')' if hasattr(xtce_obj, 'name') else ''}: {name}"
        )

    def resolve(self, ref: str, scope: str = "") -> tuple[str, Any]:
        """Resolve a reference string relative to the current scope.

        Args:
            ref (str): The reference string to resolve (can be absolute or relative).
            scope (str): The current scope for resolving relative references.

        Returns:
            tuple[str, Any]: A tuple containing the (absolute_path, resolved_object).

        Raises:
            KeyError: If the reference cannot be resolved.

        """
        # Check if absolute reference
        if ref.startswith("/"):
            if ref in self.definitions:
                return ref, self.definitions[ref]
            raise KeyError(f"Absolute reference '{ref}' not found.")

        # Check if relative reference
        parts = scope.strip("/").split("/")

        # Normalize the reference
        ref_parts = ref.split("/")
        while ref_parts and ref_parts[0] == "..":
            ref_parts.pop(0)
            if parts:
                parts.pop()
        clean_ref = "/".join(ref_parts)

        # Iteratively check path
        while True:
            prefix = "/" + "/".join(parts) if parts else ""
            candidate = f"/{clean_ref}" if prefix == "/" else f"{prefix}/{clean_ref}"

            if candidate in self.definitions:
                return candidate, self.definitions[candidate]

            if not parts:
                break
            parts.pop()

        raise KeyError(f"Could not resolve '{ref}' from scope '{scope}'")

    def get_python_name(self, xtce_obj: object) -> str:
        """Get the registered Python name for an XTCE object, if available.

        Args:
            xtce_obj (object): The XTCE object to look up.

        Returns:
            str: The registered Python name.

        Raises:
            KeyError: If no Python name is registered for the object.

        """
        name = self._python_names.get(id(xtce_obj))
        if name is None:
            raise KeyError(
                f"No Python name registered for object of type {type(xtce_obj).__name__}"
            )

        return name

    def _lookup(self, path: str) -> Any:
        """Lookup an object by its absolute path.

        Args:
            path (str): The absolute path of the object.

        Returns:
            Any: The object at the specified path.

        Raises:
            KeyError: If the path is not found.

        """
        if path not in self.definitions:
            raise KeyError(f"Absolute path not found: {path}")

        return self.definitions[path]
