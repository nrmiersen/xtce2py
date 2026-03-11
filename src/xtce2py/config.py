"""Global configuration settings."""

import functools
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ValidationError, field_validator
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    TomlConfigSettingsSource,
)


class LoggingSettings(BaseModel):
    """Logging configuration settings."""

    level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] | None = None
    file: Path | None = None

    @field_validator("file", mode="before")
    @classmethod
    def expand_path(cls, v):
        """Expand user home directory and resolve path."""
        if v is None:
            return v
        if isinstance(v, str):
            return Path(v).expanduser()
        return v


class AuthorSettings(BaseModel):
    """Author information for output package."""

    name: str = "Anonymous"
    email: str = "user@example.com"


class PackageDefaults(BaseModel):
    """Default values for package generation."""

    name_override: str | None = None
    prefix: str = ""
    suffix: str = "toolkit"
    version: str = "1.0.0"
    license: str = "MIT"


class NamingSettings(BaseModel):
    """Naming conventions for generated package."""

    style: Literal["keep", "pascal", "snake", "camel"] = "keep"
    acronyms: list[str] = ["CCSDS"]


class Settings(BaseSettings):
    """Settings model."""

    author: AuthorSettings = AuthorSettings()
    package_defaults: PackageDefaults = PackageDefaults()
    naming_convention: NamingSettings = NamingSettings()
    logging: LoggingSettings = LoggingSettings()
    model_config = SettingsConfigDict(toml_file="xtce2py.toml")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the order of precedence for settings sources."""
        return (
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            TomlConfigSettingsSource(settings_cls),
        )


_runtime_settings: Settings | None = None


@functools.lru_cache(maxsize=1)
def _load_base_settings() -> Settings:
    """Load and validate settings from configured sources, then cache the result.

    Returns:
        Settings: The validated settings object.

    Raises:
        ValueError: If the settings fail validation.

    """
    try:
        return Settings()
    except ValidationError as e:
        # Format validation errors in a more readable way
        error_messages = []
        for error in e.errors():
            field_path = ".".join(str(loc) for loc in error["loc"])
            msg = error["msg"]
            input_val = error.get("input", "")

            # Create a user-friendly error message
            if error["type"] == "literal_error":
                # Extract expected values from the message or context
                ctx = error.get("ctx", {})
                expected = ctx.get("expected", "")
                error_messages.append(
                    f"  - {field_path}: '{input_val}' is not valid. Expected one of: {expected}"
                )
            else:
                error_messages.append(f"  - {field_path}: {msg} (got: '{input_val}')")

        formatted_errors = "\n".join(error_messages)
        raise ValueError(
            f"Configuration validation failed:\n{formatted_errors}\n\n"
            f"Please check your xtce2py.toml file."
        ) from e


def get_settings() -> Settings:
    """Get the active settings.

    Returns the runtime override if one is set, otherwise returns cached base settings.

    Returns:
        Settings: The active settings object.

    """
    return _runtime_settings or _load_base_settings()


def set_settings(settings: Settings) -> None:
    """Set runtime settings override.

    Args:
        settings: The settings object to use.

    """
    global _runtime_settings
    _runtime_settings = settings


def clear_runtime_settings() -> None:
    """Clear runtime settings override and reset cached base settings."""
    global _runtime_settings
    _runtime_settings = None
    _load_base_settings.cache_clear()
