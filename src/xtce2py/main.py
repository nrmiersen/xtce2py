"""Provides the command-line interface for the xtce2py generator.

It uses Typer to create a user-friendly CLI and orchestrates the parsing
and generation process.
"""

import subprocess
from pathlib import Path

import typer
from rich.console import Console

from . import generator, xtce_parser

app = typer.Typer()
console = Console()


@app.command()
def generate(
    xtce_file: Path = typer.Argument(..., help="The path to the input XTCE file."),
    output_dir: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="The destination directory for the generated package.",
    ),
):
    """Generate a Python parser package from an XTCE file."""
    console.print(f"Starting generator...")
    console.print(f"  - Input XTCE: [bold cyan]{xtce_file}[/bold cyan]")
    console.print(f"  - Output Dir: [bold cyan]{output_dir}[/bold cyan]")

    console.print(f"Parsing '{xtce_file}'...")
    parser = xtce_parser.get_xtce_parser(xtce_file)
    space_system_metadata = parser.get_metadata()
    console.print("✅ Parsed XTCE file.")

    dist_name, package_name = generator.create_project_names(
        space_system_metadata["name"]
    )
    package_dir = output_dir / package_name
    generator.create_directory_structure(package_dir)
    generator.generate_readme(package_dir, dist_name, space_system_metadata)
    generator.generate_pyproject_toml(package_dir, dist_name, space_system_metadata)
    console.print("✅ Rendered templates and saved to output directory.")

    # # 1. PARSE XTCE FILE
    # # ------------------
    # # Here you would call your xsdata logic to parse the xtce_file
    # # and get back the `space_system` object.
    # # space_system = parse_xtce(xtce_file)
    # console.print("✅ Parsed XTCE file.")

    # # 2. TRANSFORM DATA FOR TEMPLATES
    # # -----------------------------
    # # Here you would transform the space_system object into the
    # # simple 'db_context' dictionary that your templates expect.
    # # context = transform_data(space_system)
    # console.print("✅ Transformed data for templates.")

    # # 3. RENDER & WRITE FILES
    # # -----------------------
    # # Here you would use Jinja2 to render your templates (*.py.j2)
    # # with the 'context' and save them to the output_dir.
    # # render_templates(context, output_dir)
    # console.print("✅ Generated source files.")

    # # 4. FORMAT THE OUTPUT
    # # --------------------
    # # Here you run Black on the generated code for clean formatting.
    # try:
    #     subprocess.run(["black", str(output_dir)], check=True)
    #     console.print("✅ Formatted output with Black.")
    # except Exception:
    #     console.print("⚠️ Could not format with Black. Is it installed?")

    # console.print(
    #     f"\n[bold green]✨ Success![/bold green] Parser package generated at {output_dir}"
    # )


if __name__ == "__main__":
    app()
