import re
from pathlib import Path
from typing import Any, Dict, List, Tuple

import click

from jinja2 import Environment, PackageLoader

# Copy-pasta files have `template` suffix
TEMPLATES = [
    "dockerignore.template",
    "gitignore.template",
    "Makefile.template",
    "dev-requirements.txt.template",
    "setup.cfg.template",
    "requirements.txt.template",
    "tox.ini.template",
]

# Files which are context dependent have `jinja` suffix
TEMPLATES_TO_RENDER: List[Tuple[str, List[str]]] = [
    ("setup.py.jinja", ["project_name",])
]


def get_template_context(keys: List[str], context: Dict[str, Any]) -> Dict[str, Any]:
    """Extract keys from the provided context."""
    return {k: context[k] for k in iter(keys)}


@click.command()
@click.argument("project_name", type=str)
def main(project_name: str) -> None:
    """Type the project name and let the aedificator do the (boring) scaffolding."""

    cwd = Path.cwd()
    cwd_path_joiner = cwd.joinpath

    # Create package structure.
    for d_name in ["tests", f"src/{project_name}"]:
        dir_path = cwd_path_joiner(d_name)
        dir_path.mkdir(parents=True, exist_ok=True)

        with dir_path.joinpath("__init__.py").open("w"):
            pass

    # Create a version file in `src/{project_name}/__version__.py`
    with cwd_path_joiner("src", project_name, "__version__.py").open("w") as v_file:
        v_file.write('__version__ = "0.0.1"\n')

    jinja_env = Environment(loader=PackageLoader("aedificator", "templates"))

    for template_name in TEMPLATES:
        actual = re.sub(r"\.template$", "", template_name)

        # Templates with "." prefix are not included in the package - do this hack
        if actual.startswith("gitignore") or actual.startswith("dockerignore"):
            actual = "." + actual

        with cwd_path_joiner(actual).open("w") as f_name:
            template = jinja_env.get_template(template_name).render()
            f_name.write(template)

    project_context = {"project_name": project_name}
    for template_name, ctx_keys in TEMPLATES_TO_RENDER:
        actual = re.sub(r"\.jinja$", "", template_name)
        with cwd_path_joiner(actual).open("w") as f_name:
            template = jinja_env.get_template(template_name).render(
                **get_template_context(ctx_keys, project_context)
            )
            f_name.write(template)
