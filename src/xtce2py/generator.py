"""Contains the core logic for generating parser package files.

It includes functions for creating directory layouts, rendering Jinja2
templates, and formatting the final output.
"""

from pathlib import Path

import jinja2


def create_project_names(space_system_name: str) -> str:
    """Create a package name based on the space system's name."""
    dist_name = (
        f"{space_system_name.lower().replace(' ', '-').replace('_', '-')}-toolkit"
    )
    package_name = (
        f"{space_system_name.lower().replace(' ', '_').replace('-', '_')}_toolkit"
    )
    return dist_name, package_name


def create_directory_structure(output_dir: Path):
    """Create the necessary directory structure for the generated package."""
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "src").mkdir(parents=True, exist_ok=True)


def generate_readme(
    output_dir: Path, dist_name: str, space_system_metadata: dict[str, any]
):
    """Generate a README.md file in the output directory."""
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates/"))

    template = environment.get_template("README.md.j2")

    context = {
        "dist_name": dist_name,
        "space_system_name": space_system_metadata["name"],
        "version": space_system_metadata.get("version", "1.0"),
    }

    generated_code = template.render(context)

    output_filename = output_dir / "README.md"
    with open(output_filename, "w") as f:
        f.write(generated_code)


def generate_pyproject_toml(
    output_dir: Path, dist_name: str, space_system_metadata: dict[str, any]
):
    """Generate a pyproject.toml file in the output directory."""
    environment = jinja2.Environment(loader=jinja2.FileSystemLoader("./templates/"))

    template = environment.get_template("pyproject.toml.j2")

    context = {
        "dist_name": dist_name,
        "space_system_name": space_system_metadata["name"],
        "version": space_system_metadata.get("version", "1.0"),
    }

    generated_code = template.render(context)

    output_filename = output_dir / "pyproject.toml"
    with open(output_filename, "w") as f:
        f.write(generated_code)
