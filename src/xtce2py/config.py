"""Global configuration settings."""

import functools
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, field_validator
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
            # Expand ~ to user home directory
            return Path(v).expanduser()
        return v


class AuthorSettings(BaseModel):
    """Author information for output package."""

    name: str = "Anonymous"
    email: str = "user@example.com"


class PackageDefaults(BaseModel):
    """Default values for package generation."""

    suffix: str = "toolkit"
    version: str = "1.0.0"
    license: str = "MIT"


class NamingSettings(BaseModel):
    """Naming conventions for generated package."""

    use_existing_names: bool = True
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


@functools.lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Load and validate the settings, then cache the result."""
    return Settings()
