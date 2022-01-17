from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any, Callable, NamedTuple, Sequence

import click
from jinja2 import Environment, PackageLoader

from ._util import extract_keys, transform_str


class TemplateData(NamedTuple):
    name: str
    context_keys: list[str]


DOT_PREFIX = "dot_"
TEMPLATE_SUFFIX = ".template"
JINJA_SUFFIX = ".jinja"

TRANSFORM_MAP = {
    DOT_PREFIX: ".",
    TEMPLATE_SUFFIX: "",
    JINJA_SUFFIX: "",
}


TEMPLATES = [
    # Copy-pasta files have `template` suffix.
    # XXX: I encountered some problems with prefixing the files with `.`, therefore
    #   resort to this `dot_` prefix.
    TemplateData(DOT_PREFIX + "dockerignore" + TEMPLATE_SUFFIX, []),
    TemplateData(DOT_PREFIX + "gitignore" + TEMPLATE_SUFFIX, []),
    TemplateData("Makefile" + TEMPLATE_SUFFIX, []),
    TemplateData("dev-requirements.txt" + TEMPLATE_SUFFIX, []),
    TemplateData("requirements.txt" + TEMPLATE_SUFFIX, []),
    TemplateData("tox.ini" + TEMPLATE_SUFFIX, []),
    # Files which are context dependent have `jinja` suffix
    TemplateData("setup.py" + JINJA_SUFFIX, ["project_name"]),
    TemplateData("setup.cfg" + JINJA_SUFFIX, ["project_name"]),
    TemplateData("README.md" + JINJA_SUFFIX, ["project_name"]),
]


def package_structure(project_name: str) -> list[tuple[str, ...]]:
    return [("src", project_name), ("tests",)]


def convert_dir_to_python_package(dir_path: Path) -> None:
    with dir_path.joinpath("__init__.py").open("w", encoding="utf-8"):
        pass


def create_python_package(
    path_joiner: Callable[..., Path],
    dirs: Sequence[str],
) -> None:
    dir_path = path_joiner(*dirs)
    dir_path.mkdir(parents=True, exist_ok=True)
    convert_dir_to_python_package(dir_path)


def create_version_file(
    path_joiner: Callable[..., Path],
    project_name: str,
) -> None:
    with path_joiner("src", project_name, "__version__.py").open("w", encoding="utf-8") as f:
        f.write('__version__ = "0.0.1"\n')


def render_with_ctx(
    jinja_env: Environment,
    template_data: TemplateData,
    context: dict[str, Any],
) -> str:
    return jinja_env.get_template(template_data.name).render(
        **extract_keys(context, template_data.context_keys)
    )


def create_from_template(
    path_joiner: Callable[..., Path],
    name_transformer: Callable[[str], str],
    jinja_env: Environment,
    template_data: TemplateData,
    context: dict[str, Any],
) -> None:
    actual = name_transformer(template_data.name)
    with path_joiner(actual).open("w", encoding="utf-8") as f_name:
        f_name.write(render_with_ctx(jinja_env, template_data, context))
        f_name.write("\n")


TARGET_DIR_HELP_MSG = "Desired destination of the scaffolding."


@click.command()
@click.option(
    "--target-dir",
    "-t",
    default=".",
    type=str,
    show_default=True,
    help=TARGET_DIR_HELP_MSG,
)
@click.argument("project_name", type=str)
def main(target_dir: str, project_name: str) -> None:
    """
    Type the project name and let the aedificator do the (boring) scaffolding.

    """

    path_joiner = Path(target_dir).resolve().joinpath

    # Create package structure.
    for subpackage_path in package_structure(project_name):
        create_python_package(path_joiner, subpackage_path)

    # Create a version file in `src/{project_name}/__version__.py`
    create_version_file(path_joiner, project_name)

    # Render and save the templates.
    for template in TEMPLATES:
        create_from_template(
            path_joiner,
            partial(transform_str, transforms=list(TRANSFORM_MAP.items())),
            Environment(loader=PackageLoader("aedificator", "templates")),
            template,
            {"project_name": project_name},
        )
