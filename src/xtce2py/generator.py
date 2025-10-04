"""Contains the core logic for generating parser package files.

It includes functions for creating directory layouts, rendering Jinja2
templates, and formatting the final output.
"""

import importlib.resources as pkg_resources
import logging
import shutil
from pathlib import Path
from typing import Any

import jinja2

from xtce2py import config, xtce_1_1, xtce_1_2, xtce_1_3
from xtce2py.context_models import (
    InitContext,
    ModelContext,
    ModelsContext,
    PyprojectContext,
    ReadMeContext,
)

log = logging.getLogger(__name__)


def setup_jinja_environment() -> jinja2.Environment:
    """Set up the Jinja2 environment for template rendering."""
    template_dir_ref = pkg_resources.files("xtce2py").joinpath("templates")

    with pkg_resources.as_file(template_dir_ref) as template_dir:
        loader = jinja2.FileSystemLoader(template_dir)

    return jinja2.Environment(loader=loader)


TEMPLATE_ENV = setup_jinja_environment()
STATIC_FILE_MAP = [
    ("setup.py", "setup.py"),
    ("_decoding.py", "src/{package_name}/_decoding.py"),
]


def create_project_names(
    space_system_name: str, package_name_suffix: str
) -> tuple[str, str]:
    """Create a package name based on the space system's name."""
    dist_name = f"{space_system_name.lower().replace(' ', '-').replace('_', '-')}-{package_name_suffix}"
    package_name = f"{space_system_name.lower().replace(' ', '_').replace('-', '_')}_{package_name_suffix}"
    return dist_name, package_name


def create_directory_structure(
    package_dir: Path,
    package_name: str,
    parser: xtce_1_1.XtceParser,  # | xtce_1_2.XtceParser | xtce_1_3.XtceParser,
) -> None:
    """Create the necessary directory structure for the generated package."""
    # Delete existing output directory if it exists
    if package_dir.exists():
        for item in package_dir.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    package_dir.mkdir(parents=True, exist_ok=True)
    (package_dir / "src").mkdir(parents=True, exist_ok=True)

    # Create main package directory
    main_package_dir = package_dir / "src" / package_name
    main_package_dir.mkdir(parents=True, exist_ok=True)

    # Create sub-directories for each sub-space system
    hierarchy = parser.get_space_system_hierarchy()
    for module_name in hierarchy["sub_systems"].keys():
        sub_module_dir = main_package_dir / module_name
        sub_module_dir.mkdir(parents=True, exist_ok=True)

    log.info(f"Generated directory structure at {package_dir}")


def copy_static_files(package_dir: Path):
    """Copy static files to the generated package."""
    for src_filename, dest_template_path in STATIC_FILE_MAP:
        dest_path = package_dir / dest_template_path.format(
            package_name=package_dir.name
        )

        with pkg_resources.as_file(
            pkg_resources.files("xtce2py").joinpath(f"static/{src_filename}")
        ) as src_path:
            shutil.copy2(src_path, dest_path)

    log.info(f"Copied static files to {package_dir}")


def generate_readme(package_dir: Path, readme_context: ReadMeContext):
    """Generate a README.md file in the output package directory."""
    template = TEMPLATE_ENV.get_template("README.md.j2")

    generated_code = template.render(context=readme_context)

    output_filename = package_dir / "README.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    log.info(f"Generated {output_filename.name} at {output_filename}")


def generate_pyproject_toml(
    package_dir: Path,
    pyproject_context: PyprojectContext,
):
    """Generate a pyproject.toml file in the output package directory."""
    template = TEMPLATE_ENV.get_template("pyproject.toml.j2")

    generated_code = template.render(context=pyproject_context)

    output_filename = package_dir / "pyproject.toml"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    log.info(f"Generated {output_filename.name} at {output_filename}")


def generate_init(
    package_src_dir: Path,
    init_context: InitContext,
    parser: xtce_1_1.XtceParser,  # | xtce_1_2.XtceParser | xtce_1_3.XtceParser,
):
    """Generate a __init__.py file in the output src directory."""
    template = TEMPLATE_ENV.get_template("__init__.py.j2")

    model_class_names = [
        container.name for container in parser.generate_model_context()
    ]
    public_api_names = ["parse_packet", "parse_packets", "PacketBase"]
    all_public_names = sorted(model_class_names + public_api_names)

    generated_code = template.render(
        context=init_context,
        model_class_names=model_class_names,
        all_public_names=all_public_names,
    )

    output_filename = package_src_dir / "__init__.py"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    log.info(f"Generated {output_filename.name} at {output_filename}")


def generate_models(
    package_src_dir: Path,
    parser: xtce_1_1.XtceParser,  # | xtce_1_2.XtceParser | xtce_1_3.XtceParser,
):
    """Generate models.py files for the main package and sub-systems."""
    template = TEMPLATE_ENV.get_template("models.py.j2")

    hierarchy = parser.get_space_system_hierarchy()

    # Generate models for the root space system
    root_system = hierarchy["root"]
    models_context = ModelsContext(
        imports={
            "typing": ["Literal"],
            "pydantic": ["BaseModel", "Field", "field_validator"],
        },
        containers=list(parser.generate_model_context()),
    )
    generated_code = template.render(context=models_context)

    output_filename = package_src_dir / "models.py"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    log.info(f"Generated {output_filename.name} at {output_filename}")

    # Generate models for each sub-system in separate modules
    for module_name, sub_system in hierarchy["sub_systems"].items():
        print(f"Generating models for sub-system: {sub_system.name} -> {module_name}")
        sub_module_dir = package_src_dir / module_name
        # TODO: Generate models.py in sub_module_dir


def generate_parser(
    package_src_dir: Path,
    parser: xtce_1_1.XtceParser,  # | xtce_1_2.XtceParser | xtce_1_3.XtceParser,
):
    """Generate a parser.py file in the output src directory."""
    template = TEMPLATE_ENV.get_template("parser.py.j2")

    parser_context = parser.generate_parser_context()

    generated_code = template.render(context=parser_context)

    output_filename = package_src_dir / "parser.py"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(generated_code)

    log.info(f"Generated {output_filename.name} at {output_filename}")
