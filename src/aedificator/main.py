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
    target: str = "."


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
    TemplateData("tox.ini" + TEMPLATE_SUFFIX, []),
    TemplateData("mypy.ini" + TEMPLATE_SUFFIX, []),
    # Files which are context dependent have `jinja` suffix
    TemplateData("README.md" + JINJA_SUFFIX, ["project_name"]),
    TemplateData(DOT_PREFIX + "flake8" + JINJA_SUFFIX, ["line_length"]),
    TemplateData("pyproject.toml" + JINJA_SUFFIX, ["project_name", "line_length"]),
    TemplateData("__init__.py" + JINJA_SUFFIX, ["project_name"], target="./src/{project_name}/"),
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
    target_dir = template_data.target.format(**context)
    with path_joiner(target_dir, actual).open("w", encoding="utf-8") as f:
        f.write(render_with_ctx(jinja_env, template_data, context))
        f.write("\n")


@click.command()
@click.option(
    "--target-dir",
    "-t",
    default=".",
    type=str,
    show_default=True,
    help="Desired destination of the scaffolding.",
)
@click.option(
    "--line-length",
    "-l",
    default=100,
    type=click.IntRange(min=80),
    show_default=True,
    help="Maximum line length enforced by Black and flake8.",
)
@click.argument("project_name", type=str)
def main(target_dir: str, line_length: int, project_name: str) -> None:
    """
    Type the project name and let the aedificator do the (boring) scaffolding.

    """

    path_joiner = Path(target_dir).resolve().joinpath

    # Create package structure.
    for subpackage_path in package_structure(project_name):
        create_python_package(path_joiner, subpackage_path)

    # Render and save the templates.
    for template in TEMPLATES:
        create_from_template(
            path_joiner,
            partial(transform_str, transforms=list(TRANSFORM_MAP.items())),
            Environment(loader=PackageLoader("aedificator", "templates")),
            template,
            {
                "project_name": project_name,
                "line_length": line_length,
            },
        )
