"""Global runtime state for xtce2py."""

from dataclasses import dataclass


@dataclass
class AppState:
    """Global state for xtce2py."""

    package_name: str
    dist_name: str
    xtce_root_name: str


_STATE: AppState | None = None


def init_state(package_name: str, dist_name: str, xtce_root_name: str) -> None:
    """Initialize the global state."""
    global _STATE
    _STATE = AppState(
        package_name=package_name,
        dist_name=dist_name,
        xtce_root_name=xtce_root_name,
    )


def get_state() -> AppState:
    """Get the global state."""
    if _STATE is None:
        raise RuntimeError("State has not been initialized")
    return _STATE
