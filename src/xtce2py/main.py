"""Provides the command-line interface for the xtce2py generator."""

import logging
import subprocess
import sys
from enum import IntEnum
from pathlib import Path
from typing import Optional

import typer
from pydantic import ValidationError
from rich.console import Console
from rich.logging import RichHandler

from xtce2py import config, xtce
from xtce2py.context import PackageContext
from xtce2py.generator import PackageGenerator
from xtce2py.xtce.context import XtceMetadataContext
from xtce2py.xtce.parser import BaseXtceParser

app = typer.Typer()
console = Console()


class ExitCode(IntEnum):
    """Defines exit codes for the CLI."""

    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    IO_ERROR = 3


def _validate_inputs(xtce_file: Path, output_dir: Path) -> None:
    """Ensure input parameters are valid.

    Args:
        xtce_file: Path to the input XTCE file.
        output_dir: Path to the output directory for generated code.

    Raises:
        FileNotFoundError: If the XTCE file or output directory parent does not exist.
        ValueError: If the XTCE path is not a file.
        NotADirectoryError: If the output path exists and is not a directory.

    """
    if not xtce_file.exists():
        raise FileNotFoundError(f"XTCE file not found: {xtce_file}")

    if not xtce_file.is_file():
        raise ValueError(f"XTCE path is not a file: {xtce_file}")

    if not output_dir.parent.exists():
        raise FileNotFoundError(
            f"Output directory parent does not exist: {output_dir.parent}"
        )

    if output_dir.exists() and not output_dir.is_dir():
        raise NotADirectoryError(
            f"Output path exists and is not a directory: {output_dir}"
        )


def _load_settings(
    package_version: Optional[str] = None,
    package_name_suffix: Optional[str] = None,
    log_file: Optional[Path] = None,
    log_level: Optional[str] = None,
) -> config.Settings:
    """Load configuration from TOML or defaults.

    Args:
        package_version: Optional version string override.
        package_name_suffix: Optional package suffix override.
        log_file: Optional log file path override.
        log_level: Optional log level override.

    Returns:
        config.Settings: An instance of config.Settings with the loaded configuration.

    """
    toml_path = Path("xtce2py.toml").resolve()
    if toml_path.exists():
        console.print(f"  - Using TOML File: [bold cyan]{toml_path}[/bold cyan]")

    settings = config.get_settings()
    settings_data = settings.model_dump()

    if package_version is not None:
        settings_data["package_defaults"]["version"] = package_version
    if package_name_suffix is not None:
        settings_data["package_defaults"]["suffix"] = package_name_suffix
    if log_file is not None:
        settings_data["logging"]["file"] = log_file
    if log_level is not None:
        settings_data["logging"]["level"] = log_level

    settings = config.Settings.model_validate(settings_data)
    config.set_settings(settings)

    return settings


def _parse_and_validate_xtce(xtce_file: Path, verbose: bool = False) -> BaseXtceParser:
    """Parse and validate the XTCE file.

    Args:
        xtce_file: Path to the input XTCE file.
        verbose: If True, prints detailed validation errors.

    Returns:
        BaseXtceParser: An instance of the appropriate XTCE parser.

    """
    console.print(f"Parsing XTCE [bold cyan]{xtce_file}[/bold cyan]...")

    # Find the XTCE version
    try:
        xtce_version = xtce.get_xtce_version(xtce_file)
        log.info(f"Detected XTCE version: {xtce_version}")
        console.print(f"  - XTCE Version: [bold cyan]{xtce_version}[/bold cyan]")
    except ValueError as e:
        log.error(f"Invalid XTCE version: {e}")
        console.print(f"  [bold red]ERROR: {e}[/bold red]")
        raise ValueError(f"Invalid XTCE version: {e}")

    # Validate the XTCE file against the XSD schema
    xsd_bytes = xtce_version.get_xsd_bytes()
    is_valid, errors = xtce.validate_xtce_file(xtce_file, xsd_bytes)

    if not is_valid:
        log.error("XTCE file failed XML validation.")
        log.error(f"Validation errors: {errors}")
        console.print("[bold red]ERROR: XTCE file failed XML validation.[/bold red]")
        if verbose:
            console.print("\n[bold]Validation Errors:[/bold]")
            console.print(errors)
        else:
            console.print("  (Hint: Use --verbose to see details)")
        raise ValueError("XTCE file failed XML schema validation.")

    log.info("XTCE file passed XML schema validation.")
    console.print("  - XML Schema Validation: [green]PASS[/green]")

    # Parse the XTCE file into a parser object
    parser = xtce.get_xtce_parser(xtce_file)
    if not parser:
        raise ValueError("Failed to parse XTCE.")

    log.info("Parsing XTCE into SpaceSystem object...")
    console.print("  - Parsing XTCE into SpaceSystem object...")
    try:
        parser.parse()
    except Exception as e:
        log.error(f"ERROR during parsing: {e}")
        console.print(f"  [bold red]ERROR during parsing: {e}[/bold red]")
        if verbose:
            console.print_exception()
        raise ValueError(f"Failed to parse XTCE: {e}")

    # Validate the XTCE file for semantic correctness and parse it into a parser object
    log.info("Performing XTCE semantic validation...")
    console.print("Performing XTCE semantic validation...")
    is_valid, errors = parser.validate()
    if not is_valid:
        log.error("XTCE file has semantic errors.")
        console.print("[bold red]ERROR: XTCE file has semantic errors:[/bold red]")
        for error in errors:
            log.error(f"  - in {error.location}: {error.message}")
            console.print(
                f"  - [dim]in[/dim] [bold cyan]{error.location}[/bold cyan]: {error.message}"
            )
        raise ValueError("XTCE file has semantic errors.")

    log.info("XTCE file passed semantic validation.")
    console.print("  - Semantic Validation: [green]PASS[/green]")

    # Process the SpaceSystem
    log.info("Processing SpaceSystem...")
    console.print("Processing SpaceSystem...")
    try:
        parser.process()
    except Exception as e:
        log.error(f"ERROR during processing: {e}")
        console.print(f"  [bold red]ERROR during processing: {e}[/bold red]")
        if verbose:
            console.print_exception()
        raise ValueError(f"Failed to process XTCE: {e}")

    return parser


def _set_package_context(
    xtce_metadata: XtceMetadataContext,
    settings: config.Settings,
    package_version: str | None,
    package_name_override: str | None,
    package_name_prefix: str | None,
    package_name_suffix: str | None,
) -> PackageContext:
    """Set the package context based on the parser and settings.

    Args:
        xtce_metadata: The XTCE metadata context.
        settings: The loaded configuration settings.
        package_version: Optional version string override.
        package_name_override: Optional package name override.
        package_name_prefix: Optional package name prefix.
        package_name_suffix: Optional package name suffix.

    Returns:
        PackageContext: The configured package context.

    """
    # Set the package version
    final_version = (
        package_version
        or settings.package_defaults.version
        or xtce_metadata.version
        or "0.1.0"
    )

    # Set the package name
    if package_name_override:
        package_name = package_name_override
    elif settings.package_defaults.name_override:
        package_name = settings.package_defaults.name_override
    else:
        prefix = package_name_prefix or settings.package_defaults.prefix
        suffix = package_name_suffix or settings.package_defaults.suffix
        package_name = f"{prefix}{'_' if prefix else ''}{xtce_metadata.name}{'_' if suffix else ''}{suffix}".lower()

    return PackageContext(
        package_version=final_version,
        package_name=package_name,
    )


def _run_formatter(package_dir: Path, verbose: bool = False) -> None:
    """Format the generated package using Ruff.

    Args:
        package_dir: The directory of the generated package to format.
        verbose: If True, prints detailed error information if formatting fails.

    """
    if not package_dir.exists():
        log.error(f"Cannot format non-existent directory: {package_dir}")
        console.print(
            f"[bold red]Error: Cannot format non-existent directory: {package_dir}[/bold red]"
        )
        return

    log.info("Formatting generated code...")
    console.print("Formatting generated code...")

    # Ruff should be installed in the same environment as xtce2py
    ruff_cmd = [sys.executable, "-m", "ruff"]

    try:
        # Format the code first
        subprocess.run(
            ruff_cmd + ["format", "."],
            check=True,
            capture_output=True,
            cwd=package_dir,
        )

        # Check the code and attempt to fix any remaining issues
        subprocess.run(
            ruff_cmd + ["check", "--fix", "."],
            check=True,
            capture_output=True,
            cwd=package_dir,
        )

        log.info("Formatted code with Ruff.")
        console.print("[green]Formatted code with Ruff.[/green]")

    except subprocess.CalledProcessError as e:
        log.error("Error during formatting!")
        if e.stderr:
            log.error(f"Stderr: {e.stderr.decode()}")
        if e.stdout:
            log.error(f"Stdout: {e.stdout.decode()}")

        console.print("[bold red]Error during formatting![/bold red]")
        if verbose:
            console.print(f"Command: {' '.join(e.cmd)}")
            if e.stderr:
                console.print(f"Stderr: {e.stderr.decode()}")
            if e.stdout:
                console.print(f"Stdout: {e.stdout.decode()}")

    except FileNotFoundError:
        log.warning("Formatting skipped (subprocess failed).")
        console.print(
            "[bold yellow]Warning: Formatting skipped (subprocess failed).[/bold yellow]"
        )


def _setup_logging(log_level: str | None = None, log_file: Path | None = None) -> None:
    """Configure the logging system.

    Args:
        log_level: The logging level as a string (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). If None, logging is disabled.
        log_file: Optional path to a log file. If provided, logs will be written to this file with rotation. If None, logs will be output to the console.

    """
    if log_level is None:
        # Disable all logging by setting level higher than CRITICAL
        logging.disable(logging.CRITICAL)
        return

    handlers = []

    if log_file:
        log_path = Path(log_file) if not isinstance(log_file, Path) else log_file

        # Rotate existing logs
        if log_path.exists():
            # Delete the oldest log if it exists
            # TODO make the number of retained logs configurable
            Path(f"{log_path}5").unlink(missing_ok=True)

            # Shift numbered logs backwards
            for i in range(4, 0, -1):
                src_path = Path(f"{log_path}{i}")
                dst_path = Path(f"{log_path}{i + 1}")
                if src_path.exists():
                    src_path.replace(dst_path)

            # Rename current log to log1
            log_path.replace(Path(f"{log_path}1"))

        # Log output to a file
        file_handler = logging.FileHandler(log_path)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    else:
        # Only log to console if no file is set
        console_handler = RichHandler(
            console=console,
            show_time=False,
            show_path=False,
            rich_tracebacks=True,
        )
        handlers.append(console_handler)

    logging.basicConfig(
        level=log_level.upper(),
        format="%(message)s",
        handlers=handlers,
    )

    global log
    log = logging.getLogger(__name__)


def generate(
    xtce_file: Path,
    output_dir: Path,
    clean: bool = False,
    package_version: Optional[str] = None,
    package_name_override: Optional[str] = None,
    package_name_prefix: Optional[str] = None,
    package_name_suffix: Optional[str] = None,
    verbose: bool = False,
    log_file: Optional[Path] = None,
    log_level: Optional[str] = None,
) -> None:
    """Generate a Python toolkit package from an XTCE file.

    Args:
        xtce_file: Path to the input XTCE file.
        output_dir: Path to the output directory for the generate package.
        clean: If True, deletes the output directory before generating.
        package_version: Optional version string to use for the generated package.
        package_name_override: Optional name to override the generated package name.
        package_name_prefix: Optional prefix to prepend to the generated package name.
        package_name_suffix: Optional suffix to append to the generated package name.
        verbose: If True, enables verbose output during generation.
        log_file: Optional path to a log file. If provided, logs will be written to this file with rotation. If None, logs will be output to the console.
        log_level: Optional logging level as a string (e.g., "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"). If None, logging is disabled.

    """
    # Initial setup
    _validate_inputs(xtce_file, output_dir)
    settings = _load_settings(
        package_version=package_version,
        package_name_suffix=package_name_suffix,
        log_file=log_file,
        log_level=log_level,
    )
    _setup_logging(settings.logging.level, settings.logging.file)

    if verbose:
        log.info(f"Loaded settings: {settings.model_dump()}")
        console.print(f"  - Current Settings: {settings.model_dump()}")

    # Parse the XTCE
    log.info("Starting xtce2py...")
    log.info(f"Input XTCE: '{xtce_file}'")
    log.info(f"Output Dir: '{output_dir}'")
    console.print("Starting xtce2py...")
    console.print(f"  - Input XTCE: [bold cyan]{xtce_file}[/bold cyan]")
    console.print(f"  - Output Dir: [bold cyan]{output_dir}[/bold cyan]")
    parser = _parse_and_validate_xtce(xtce_file, verbose)

    # Set package configuration
    package_context = _set_package_context(
        parser.metadata,
        settings,
        package_version,
        package_name_override,
        package_name_prefix,
        package_name_suffix,
    )

    # Initialize the generator
    log.info("Starting generator...")
    console.print("Starting generator...")
    generator = PackageGenerator(
        package_info=package_context,
        parser=parser,
        output_dir=output_dir,
        clean_output=clean,
    )
    log.info(f"Distribution name: {generator.dist_name}")
    log.info(f"Package name: {generator.package_name}")
    if verbose:
        console.print(f"  - Distribution name: '{generator.dist_name}'")
        console.print(f"  - Package name: '{generator.package_name}'")

    # Generate the package
    try:
        generator.generate()
    except Exception as e:
        log.error(f"ERROR during generation: {e}")
        console.print(f"  [bold red]ERROR during generation: {e}[/bold red]")
        if verbose:
            console.print_exception()
        raise ValueError(f"Failed to generate package: {e}")
    log.info(
        f"Successfully generated package '{generator.dist_name}' at '{output_dir / generator.package_name}'"
    )
    console.print(
        f"\n[bold green]Success![/bold green] Generated '{generator.dist_name}'"
    )

    # Format the generated package
    generated_path = output_dir / generator.package_name
    _run_formatter(generated_path, verbose)


@app.command(name="generate")
def cli_generate(
    xtce_file: Path = typer.Argument(
        ...,
        help="Path to input XTCE file.",
    ),
    output_dir: Path = typer.Argument(
        ...,
        help="Destination directory.",
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        "-c",
        is_flag=True,
        help="Delete the output directory before generating.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        is_flag=True,
        help="Enable verbose output.",
    ),
    package_version: str = typer.Option(
        None,
        "--package-version",
        help="Version string to use for the generated package (e.g., '1.0.0').",
    ),
    package_name_override: str = typer.Option(
        None,
        "--package-name-override",
        help="Override the generated package name.",
    ),
    package_name_prefix: str = typer.Option(
        None,
        "--package-name-prefix",
        help="Prefix to prepend to the generated package name.",
    ),
    package_name_suffix: str = typer.Option(
        None,
        "--package-name-suffix",
        help="Suffix to append to the generated package name.",
    ),
    log_level: str = typer.Option(
        None,
        "--log-level",
        help="Logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'). If not set, logging is disabled.",
    ),
    log_file: Path = typer.Option(
        None,
        "--log-file",
        help="Path to a log file. If provided, logs will be written to this file with rotation. If not set, logs will be output to the console.",
    ),
):
    """Generate a Python toolkit package from an XTCE file."""
    try:
        generate(
            xtce_file=xtce_file,
            output_dir=output_dir,
            clean=clean,
            package_version=package_version,
            package_name_override=package_name_override,
            package_name_prefix=package_name_prefix,
            package_name_suffix=package_name_suffix,
            verbose=verbose,
            log_file=log_file,
            log_level=log_level,
        )

    except (FileNotFoundError, NotADirectoryError) as e:
        log.error(f"IO ERROR: {e}")
        console.print(f"[bold red]IO ERROR: {e}[/bold red]")

        raise typer.Exit(code=ExitCode.IO_ERROR)

    except (ValueError, ValidationError) as e:
        if isinstance(e, ValidationError):
            log.error(f"Configuration validation error: {e}")
            console.print(f"[bold red]Configuration Validation Error:[/bold red] {e}")

        raise typer.Exit(code=ExitCode.USAGE_ERROR)

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        console.print(f"[bold red]Unexpected Error: {e}[/bold red]")
        if verbose:
            console.print_exception()
        raise typer.Exit(code=ExitCode.GENERAL_ERROR)

    raise typer.Exit(code=ExitCode.SUCCESS)


if __name__ == "__main__":
    app()
