"""Provides the command-line interface for the xtce2py generator."""

import enum
import logging
import shutil
import subprocess
from pathlib import Path

import jinja2
import typer
from pydantic import ValidationError
from rich.console import Console
from rich.logging import RichHandler

from xtce2py import config, generator, xtce
from xtce2py._validation import (
    ValidationResult,
    ValidationSeverity,
    XtceSemanticValidationError,
)
from xtce2py.context_models import InitContext, PyprojectContext, ReadMeContext

app = typer.Typer()
console = Console()


class ExitCode(enum.IntEnum):
    """Exit codes for the application."""

    SUCCESS = 0
    GENERAL_ERROR = 1
    USAGE_ERROR = 2
    IO_ERROR = 3


def setup_logging(log_level: str | None, log_file: Path | None):
    """Configure the logging system for the application."""
    if log_level is None:
        # Disable all logging by setting level higher than CRITICAL
        logging.disable(logging.CRITICAL)
        return

    handlers = []

    console_handler = RichHandler(
        console=console,
        show_time=False,
        show_path=False,
        rich_tracebacks=True,
    )
    handlers.append(console_handler)

    if log_file:
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    logging.basicConfig(
        level=log_level.upper(),
        format="%(message)s",
        handlers=handlers,
    )


@app.command()
def generate(
    xtce_file: Path = typer.Argument(..., help="The path to the input XTCE file."),
    output_dir: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="The destination directory for the generated package.",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed errors.",
        is_flag=True,
    ),
    package_version: str = typer.Option(
        "",
        "--package-version",
        help="The version to assign to the generated package. If not provided, defaults to the XTCE header version.",
    ),
    package_name_suffix: str = typer.Option(
        "",
        "--package-name-suffix",
        help="A suffix to append to the generated package name.",
    ),
    log_file: Path = typer.Option(
        None,
        "--log-file",
        help="Path to save detailed logs. If not provided, logs go to console only.",
    ),
    log_level: str | None = typer.Option(
        None,
        "--log-level",
        help="Set the logging verbosity (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    ),
):
    """Generate a Python parser package from an XTCE file."""
    # Check inputs
    if not xtce_file.exists():
        console.print(f"[bold red]ERROR: XTCE file not found: {xtce_file}[/bold red]")
        raise typer.Exit(code=ExitCode.IO_ERROR)
    if not xtce_file.is_file():
        console.print(
            f"[bold red]ERROR: XTCE path is not a file: {xtce_file}[/bold red]"
        )
        raise typer.Exit(code=ExitCode.IO_ERROR)
    if not output_dir.parent.exists():
        console.print(
            f"[bold red]ERROR: Output directory parent does not exist: {output_dir.parent}[/bold red]"
        )
        raise typer.Exit(code=ExitCode.IO_ERROR)
    if output_dir.exists() and not output_dir.is_dir():
        console.print(
            f"[bold red]ERROR: Output path exists and is not a directory: {output_dir}[/bold red]"
        )
        raise typer.Exit(code=ExitCode.IO_ERROR)

    console.print("Starting generator...")
    console.print(f"  - Input XTCE: [bold cyan]{xtce_file}[/bold cyan]")
    console.print(f"  - Output Dir: [bold cyan]{output_dir}[/bold cyan]")

    # Try to load configuration settings
    toml_path = Path("xtce2py.toml")
    if toml_path.exists():
        console.print(f"  - Using TOML File: [bold cyan]{toml_path}[/bold cyan]")
    try:
        settings = config.get_settings()
        console.print(
            f"  - Current Settings: {settings.model_dump()}"
        ) if verbose else None
    except ValidationError as e:
        console.print(
            f"[bold red]ERROR: Invalid configuration in '{toml_path}'.[/bold red]"
        )
        console.print("\n[bold]Validation Details:[/bold]")
        console.print(e)
        raise typer.Exit(code=ExitCode.USAGE_ERROR)

    log_level = log_level or settings.logging.level
    if log_level:
        log_level = log_level.upper()
    log_file = log_file or (
        Path(settings.logging.file) if settings.logging.file else None
    )
    setup_logging(log_level, log_file)

    console.print(
        f"  - Log level: [bold cyan]{log_level}[/bold cyan]"
    ) if verbose and log_level else None
    console.print(
        f"  - Log file: [bold cyan]{log_file}[/bold cyan]"
    ) if verbose and log_file else None

    # Use settings
    package_version = package_version or settings.package_defaults.version
    package_name_suffix = package_name_suffix or settings.package_defaults.suffix

    # Parse the XTCE file
    console.print(f"Parsing XTCE '{xtce_file}'...")
    try:
        xtce_version = xtce.get_xtce_version(xtce_file)
    except ValueError as e:
        console.print(f"  [bold red]ERROR: {e}[/bold red]")
        raise typer.Exit(code=ExitCode.USAGE_ERROR)
    console.print(f"  - XTCE version: {xtce_version}")

    # Validate the XTCE file
    is_valid, errors = xtce.validate_xtce_file(xtce_file, xtce_version.xsd)
    if is_valid:
        console.print(
            f"  - XTCE validated against XML schema: '{xtce_version.xsd.name}'"
        )
    else:
        console.print("[bold red]ERROR: XTCE file failed validation.[/bold red]")
        if verbose:
            console.print("\n[bold]Validation Errors:[/bold]")
            console.print(errors)
        else:
            console.print("  (Hint: Use the --verbose flag to see detailed errors)")
        raise typer.Exit(code=ExitCode.USAGE_ERROR)

    # Get the appropriate parser for the XTCE version and perform semantic validation
    console.print("Performing XTCE semantic validation...")
    try:
        xtce_parser = xtce.get_xtce_parser(xtce_file)
        if not xtce_parser:
            console.print(
                f"[bold red]ERROR: Failed to create XTCE parser for XTCE version {xtce_version}.[/bold red]"
            )
            raise typer.Exit(code=ExitCode.GENERAL_ERROR)
        if not xtce_parser.space_system:
            console.print(
                f"[bold red]ERROR: No SpaceSystem found in XTCE file '{xtce_file}'.[/bold red]"
            )
            raise typer.Exit(code=ExitCode.USAGE_ERROR)
    except XtceSemanticValidationError as e:
        console.print("[bold red]ERROR: XTCE file has semantic errors:[/bold red]")
        for error in e.errors:
            console.print(
                f"  - [dim]in[/dim] [bold cyan]{error.location}[/bold cyan]: {error.message}"
            )
        raise typer.Exit(code=ExitCode.USAGE_ERROR)
    if xtce_parser.warnings:
        console.print("  [bold yellow]Warnings:[/bold yellow]")
        for warning in xtce_parser.warnings:
            console.print(
                f"  - [dim]in[/dim] [bold yellow]{warning.location}[/bold yellow]: {warning.message}"
            )
    console.print("[green]XTCE semantic validation complete.[/green]")

    # Get the XTCE metadata
    space_system_metadata = xtce_parser.metadata
    console.print(f"  - SpaceSystem name: '{space_system_metadata.name}'")
    console.print(f"  - SpaceSystem version: {space_system_metadata.version}")
    console.print("[green]Parsed XTCE file.[/green]")

    # Set package versions
    package_version = (
        package_version
        or space_system_metadata.version
        or settings.package_defaults.version
    )

    # Set package and distribution names
    dist_name, package_name = generator.create_project_names(
        space_system_metadata.name,
        package_name_suffix=package_name_suffix,
    )
    console.print("Generating package...")
    console.print(f"  - Package Name: [bold cyan]{package_name}[/bold cyan]")
    console.print(f"  - Distribution Name: [bold cyan]{dist_name}[/bold cyan]")
    console.print(f"  - Package Version: [bold cyan]{package_version}[/bold cyan]")

    # Set directories
    package_dir = output_dir / package_name
    package_src_dir = package_dir / "src" / package_name
    console.print(f"  - Package Dir: [bold cyan]{package_dir}[/bold cyan]")

    # Generate files
    try:
        generator.create_directory_structure(
            package_dir=package_dir, package_name=package_name, parser=xtce_parser
        )

        generator.copy_static_files(package_dir)

        readme_context = ReadMeContext(
            dist_name=dist_name,
            package_name=package_name,
            xtce_version=str(xtce_version),
            metadata=space_system_metadata,
        )
        generator.generate_readme(package_dir, readme_context)

        pyproject_context = PyprojectContext(
            dist_name=dist_name,
            package_name=package_name,
            version=package_version,
            metadata=space_system_metadata,
        )
        generator.generate_pyproject_toml(package_dir, pyproject_context)

        init_context = InitContext(metadata=space_system_metadata)
        generator.generate_init(package_src_dir, init_context, xtce_parser)

        generator.generate_models(package_src_dir, xtce_parser)

        generator.generate_parser(package_src_dir, xtce_parser)

        console.print("[green]Generated package.[/green]")

    except jinja2.TemplateError as e:
        console.print(f"[bold red]ERROR: Template rendering error: {e}[/bold red]")
        raise typer.Exit(code=ExitCode.GENERAL_ERROR)

    except FileNotFoundError as e:
        console.print(f"[bold red]ERROR: Failed to generate file: {e}[/bold red]")
        raise typer.Exit(code=ExitCode.GENERAL_ERROR)

    # Format the output
    console.print("Formatting generated code...")
    try:
        # Run Ruff to format code, sort imports, and apply all auto-fixes.
        ruff_format_cmd = ["ruff", "format", str(package_dir)]
        subprocess.run(
            ruff_format_cmd,
            check=True,
            capture_output=True,
            cwd=package_dir,
        )

        ruff_check_cmd = ["ruff", "check", "--fix", str(package_dir)]
        subprocess.run(
            ruff_check_cmd,
            check=True,
            capture_output=True,
            cwd=package_dir,
        )

        console.print("[green]Formatted code with Ruff.[/green]")

    except subprocess.CalledProcessError as e:
        console.print("[bold red]Error during formatting![/bold red]")
        cmd_str = " ".join(e.cmd)
        console.print(f"  - Command failed: `{cmd_str}`")
        console.print(f"  - Exit Code: {e.returncode}")
        if e.stdout:
            console.print(f"  - Stdout: {e.stdout.decode()}")
        if e.stderr:
            console.print(f"  - Stderr: {e.stderr.decode()}")

    except FileNotFoundError as e:
        console.print(
            f"[bold yellow]Could not format. Command not found: '{e.filename}'[/bold yellow]"
        )

    console.print(
        f"\n[bold green]Success![/bold green] '{dist_name}' package generated at {package_dir}\n"
    )


if __name__ == "__main__":
    app()
