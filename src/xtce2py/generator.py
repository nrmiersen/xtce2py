"""Package generator."""

import importlib.resources as pkg_resources
import logging
import shutil
from collections import defaultdict
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader

from xtce2py.context import PackageContext, PyprojectContext, ReadMeContext
from xtce2py.utils import path_to_package, sanitize_class_name
from xtce2py.xtce.parser import BaseXtceParser

log = logging.getLogger(__name__)


class PackageGenerator:
    """Package generator.

    Attributes:
        parser (XtceParser): The XTCE parser instance.
        output_dir (Path): Path to the output directory.

    """

    def __init__(
        self,
        package_info: PackageContext,
        parser: BaseXtceParser,
        output_dir: Path,
        clean_output: bool = False,
    ) -> None:
        """Initialize the package generator.

        Args:
            package_info (PackageContext): The package context.
            parser (BaseXtceParser): The XTCE parser instance.
            output_dir (Path): Path to the output directory.

        """
        self.package_info = package_info
        self.xtce_parser = parser
        self.output_dir = output_dir
        self.clean_output = clean_output

        self.exports = defaultdict(lambda: defaultdict(list))
        self.package_map: dict[str, str] = {}

        # Class variables
        self.env: Environment
        self.dist_name: str = ""
        self.package_name: str = ""
        self.package_dir: Path = Path()
        self.src_dir: Path = Path()
        self.class_registry: dict[str, tuple[str, str, str]] = {}
        self.modules = defaultdict(
            lambda: {
                "cmd": {"enums": [], "commands": [], "aggregates": []},
                "tlm": {"enums": [], "packets": [], "aggregates": []},
            }
        )

        self._generate_package_names()
        self._setup_jinja_environment()

    def generate(self) -> None:
        """Generate the installable Python package."""
        log.info("Starting package generation...")

        # Generate package information
        self._map_package_names()

        # Build the package structure
        self._build_registry()
        self._scaffold_package()

        # Generate package files
        self._generate_readme()
        self._generate_pyproject()
        self._generate_base_classes()

        # Generate all modules
        self._generate_modules()
        self._generate_init_files()

        log.info(f"Finished generating package at {self.output_dir.resolve()}")

    def _setup_jinja_environment(self) -> None:
        """Set up the Jinja environment.

        Args:
            template_dir (Path): Path to the template directory.

        """
        template_dir_ref = pkg_resources.files("xtce2py").joinpath("templates")

        with pkg_resources.as_file(template_dir_ref) as template_dir:
            loader = FileSystemLoader(template_dir)

        self.env = Environment(loader=loader)

    def _generate_package_names(self) -> None:
        """Generate package and distribution names."""
        base_name = self.package_info.package_name

        # Distribution name uses hyphens
        self.dist_name = base_name.replace(" ", "-").replace("_", "-")

        # Package name uses underscores
        self.package_name = base_name.replace(" ", "_").replace("-", "_")

    def _map_package_names(self) -> None:
        raw_packages = self.xtce_parser.package_list
        if not raw_packages:
            return

        xtce_root = min(raw_packages, key=len)

        target_root = self.package_name

        self.package_map.clear()

        for raw in raw_packages:
            if raw == xtce_root:
                self.package_map[raw] = target_root
            elif raw.startswith(xtce_root + "."):
                suffix = raw[len(xtce_root) :]
                self.package_map[raw] = target_root + suffix
            else:
                self.package_map[raw] = raw

    def _render_template(
        self, template_name: str, context: Any, output_filename: str
    ) -> None:
        """Render a template and write to file."""
        template = self.env.get_template(template_name)

        if isinstance(context, dict):
            generated_code = template.render(**context)
        else:
            generated_code = template.render(context=context)

        output_path = self.package_dir / output_filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated_code)

        log.info(f"Generated {output_path.name} at: {output_path}")

    def _scaffold_package(self) -> None:
        self.package_dir = self.output_dir / self.package_name
        self.src_dir = self.package_dir / "src"

        if self.clean_output and self.package_dir.exists():
            shutil.rmtree(self.package_dir)
            log.info(f"Cleaned output directory: {self.package_dir}")

        self.src_dir.mkdir(parents=True, exist_ok=True)

        for python_pkg in self.package_map.values():
            pkg_path = python_pkg.replace(".", "/")
            target_dir = self.src_dir / pkg_path

            target_dir.mkdir(parents=True, exist_ok=True)
            log.debug(f"Created directory: {target_dir}")

    def _ensure_init_chain(self, sub_path: str):
        """Generate __init__.py files along the given sub_path."""
        current_dir = self.src_dir

        parts = sub_path.split("/")

        for part in parts:
            current_dir = current_dir / part
            init_file = current_dir / "__init__.py"

            if not init_file.exists():
                with open(init_file, "w") as f:
                    f.write(f'"""Package: {part}"""\n')

                log.info(f"Created __init__.py at: {init_file}")

    def _build_registry(self) -> None:
        """Build the class registry mapping ClassNames to Python Packages."""
        self.class_registry.clear()
        self.modules.clear()

        for path, cmd in self.xtce_parser.effective_commands.items():
            xtce_pkg = path_to_package(path)
            if not xtce_pkg:
                continue

            python_pkg = self.package_map.get(xtce_pkg, xtce_pkg)
            class_name = sanitize_class_name(
                cmd.name, getattr(cmd, "is_abstract", False)
            )
            self.class_registry[class_name] = (python_pkg, "cmd", "commands")
            self.modules[python_pkg]["cmd"]["commands"].append(cmd)

        for xtce_pkg, enums in getattr(self.xtce_parser, "_cmd_enums", {}).items():
            if not xtce_pkg:
                continue

            python_pkg = self.package_map.get(xtce_pkg, xtce_pkg)
            self.modules[python_pkg]["cmd"]["enums"].extend(enums)
            for enum_vm in enums:
                self.class_registry[enum_vm.name] = (python_pkg, "cmd", "enums")

        for xtce_pkg, enums in getattr(self.xtce_parser, "_tlm_enums", {}).items():
            if not xtce_pkg:
                continue

            python_pkg = self.package_map.get(xtce_pkg, xtce_pkg)
            self.modules[python_pkg]["tlm"]["enums"].extend(enums)
            for enum_vm in enums:
                self.class_registry[enum_vm.name] = (python_pkg, "tlm", "enums")

    def _generate_modules(self) -> None:
        all_processed_vms = defaultdict(
            lambda: defaultdict(lambda: {"enums": [], "commands": [], "packets": []})
        )
        facade_exports_map = defaultdict(lambda: defaultdict(dict))

        for package_name, domains in self.modules.items():
            for domain, files in domains.items():
                if files["enums"]:
                    all_processed_vms[package_name][domain]["enums"] = files["enums"]
                    facade_exports_map[package_name][domain]["enums"] = [
                        enum.name for enum in files["enums"]
                    ]

                target_key = "commands" if domain == "cmd" else "packets"
                if files[target_key]:
                    view_models = []
                    facade_exports_map[package_name][domain][target_key] = []

                    for obj in files[target_key]:
                        vm = self.xtce_parser.process_command(obj)
                        view_models.append(vm)

                        facade_exports_map[package_name][domain][target_key].append(
                            vm.class_name
                        )
                        self.exports[package_name][domain].append(vm.class_name)

                        self.class_registry[vm.class_name] = (
                            package_name,
                            domain,
                            target_key,
                        )

                    all_processed_vms[package_name][domain][target_key] = view_models

        for package_name, domains in all_processed_vms.items():
            sub_path = package_name.replace(".", "/")
            base_pkg_dir = self.src_dir / sub_path

            for domain, data in domains.items():
                domain_dir = base_pkg_dir / domain
                target_key = "commands" if domain == "cmd" else "packets"

                if data["enums"]:
                    domain_dir.mkdir(parents=True, exist_ok=True)
                    self._render_template(
                        template_name="enums.py.j2",
                        context={"enums": data["enums"]},
                        output_filename=f"src/{sub_path}/{domain}/enums.py",
                    )

                if data[target_key]:
                    domain_dir.mkdir(parents=True, exist_ok=True)
                    imports_needed = set()

                    for vm in data[target_key]:
                        if vm.parent_class and vm.parent_class != "XtcePacket":
                            imp = self._resolve_import(
                                package_name, vm.parent_class, domain
                            )
                            if imp:
                                imports_needed.add(imp)

                        for field in getattr(vm, "fields", []):
                            if getattr(field, "required_import", None):
                                imports_needed.add(field.required_import)

                        if hasattr(vm, "required_enums") and vm.required_enums:
                            local_enums = set()
                            for enum_name in vm.required_enums:
                                imp = self._resolve_import(
                                    package_name, enum_name, domain
                                )
                                if imp:
                                    imports_needed.add(imp)
                                else:
                                    local_enums.add(enum_name)

                            if local_enums:
                                enum_names = ", ".join(sorted(local_enums))
                                imports_needed.add(f"from .enums import {enum_names}")

                    sorted_vms = self._sort_by_dependency(data[target_key])
                    self._render_template(
                        template_name=f"{domain}.py.j2",
                        context={
                            "commands": sorted_vms,
                            "extra_imports": sorted(list(imports_needed)),
                            "base_module": self._calculate_relative_base(
                                package_name, domain_depth=1
                            ),
                        },
                        output_filename=f"src/{sub_path}/{domain}/{target_key}.py",
                    )

                facade_exports = facade_exports_map[package_name][domain]
                if facade_exports:
                    self._write_facade(domain_dir, facade_exports)

    def _write_facade(self, domain_dir: Path, exports: dict[str, list[str]]) -> None:
        all_symbols = []
        class_exports = {}
        module_exports = []

        for module_name, symbols in exports.items():
            if module_name == "enums":
                # Export the module itself instead of the individual enum classes
                module_exports.append("enums")
                all_symbols.append("enums")
            elif symbols:
                # Export the individual command classes
                class_exports[module_name] = symbols
                all_symbols.extend(symbols)

        context = {
            "module_exports": module_exports,
            "class_exports": class_exports,
            "all_symbols": all_symbols,
        }

        rel_output_path = domain_dir.relative_to(self.package_dir) / "__init__.py"

        self._render_template(
            template_name="submodule_init.py.j2",
            context=context,
            output_filename=str(rel_output_path),
        )

    def _generate_readme(self) -> None:
        """Generate README.md."""
        readme_context = ReadMeContext(
            dist_name=self.dist_name,
            package_name=self.package_name,
            xtce_version=self.xtce_parser.xtce_version,
            metadata=self.xtce_parser.metadata,
        )
        self._render_template(
            template_name="README.md.j2",
            context=readme_context,
            output_filename="README.md",
        )

    def _generate_pyproject(self) -> None:
        """Generate pyproject.toml."""
        pyproject_context = PyprojectContext(
            dist_name=self.dist_name,
            package_name=self.package_name,
            version=self.package_info.package_version,
            metadata=self.xtce_parser.metadata,
        )
        self._render_template(
            template_name="pyproject.toml.j2",
            context=pyproject_context,
            output_filename="pyproject.toml",
        )

    def _generate_base_classes(self) -> None:
        if not self.modules:
            log.warning("No modules found. Skipping base class generation.")
            return

        root_pkg = min(self.modules.keys(), key=len)

        output_subpath = root_pkg.replace(".", "/")

        relative_path = f"src/{output_subpath}/base.py"

        self._render_template(
            template_name="base.py.j2",
            context={"metadata": self.xtce_parser.metadata},
            output_filename=relative_path,
        )

        log.debug(f"Generated base classes in {root_pkg}")

    def _generate_init_files(self) -> None:
        template = self.env.get_template("module_init.py.j2")

        all_packages = self.package_map.values()

        package_children = defaultdict(set)

        for pkg in all_packages:
            if "." in pkg:
                parent, child = pkg.rsplit(".", 1)
                package_children[parent].add(child)

        for package in all_packages:
            cmd_classes = self.exports[package].get("cmd", [])
            tlm_classes = self.exports[package].get("tlm", [])
            subpackages = sorted(list(package_children.get(package, [])))

            context = {
                "package_name": package,
                "commands": cmd_classes,
                "telemetry": tlm_classes,
                "subpackages": subpackages,
            }

            code = template.render(context)

            sub_path = package.replace(".", "/")
            output_path = self.src_dir / sub_path / "__init__.py"

            output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, "w", encoding="utf-8") as f:
                f.write(code)

            log.debug(f"Generated __init__.py for {package}")

    def _resolve_import(
        self, current_pkg: str, target_class: str, current_domain: str
    ) -> str | None:
        target_info = self.class_registry.get(target_class)
        if not target_info:
            return None

        target_pkg, target_domain, target_file = target_info

        if target_pkg == current_pkg and target_domain == current_domain:
            return None

        curr_parts = current_pkg.split(".")
        tgt_parts = target_pkg.split(".")

        common_len = 0
        for c, t in zip(curr_parts, tgt_parts):
            if c == t:
                common_len += 1
            else:
                break

        levels_up = (len(curr_parts) - common_len) + 1
        path_down = tgt_parts[common_len:]

        prefix = "." * (levels_up + 1)
        down_str = ".".join(path_down)

        if down_str:
            module_path = f"{prefix}{down_str}.{target_domain}.{target_file}"
        else:
            module_path = f"{prefix}{target_domain}.{target_file}"

        return f"from {module_path} import {target_class}"

    def _calculate_relative_base(self, package: str, domain_depth: int = 0) -> str:
        if not self.modules:
            return ".base"

        root_pkg = min(self.modules.keys(), key=len)
        rel_depth = len(package.split(".")) - len(root_pkg.split("."))

        dots = "." * (rel_depth + 1 + domain_depth)
        return f"{dots}base"

    def _sort_by_dependency(self, view_models: list) -> list:
        vm_map = {vm.class_name: vm for vm in view_models}
        visited = set()
        result = []

        def visit(name):
            if name in visited:
                return
            vm = vm_map.get(name)
            if not vm:
                return

            if vm.parent_class and vm.parent_class in vm_map:
                visit(vm.parent_class)

            visited.add(name)
            result.append(vm)

        for vm in view_models:
            visit(vm.class_name)

        return result
