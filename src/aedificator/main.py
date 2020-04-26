from pathlib import Path

import click

from jinja2 import Environment, PackageLoader

TEMPLATE_MAPPING = {
    "dev-requirements_tmpl.txt": "dev-requirements.txt",
    "dockerignore_tmpl.txt": ".dockerignore",
    "gitignore_tmpl.txt": ".gitignore",
    "tox_tmpl.txt": "tox.ini",
    "setup_cfg_tmpl.txt": "setup.cfg",
}


TEMPLATE_TO_RENDER_MAPPING = {
    "setup_py_tmpl.txt": "setup.py",
}


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

    with cwd_path_joiner("requirements.txt").open("w"):
        pass

    jinja_env = Environment(loader=PackageLoader("aedificator", "templates"))

    for template_name, actual in TEMPLATE_MAPPING.items():
        with cwd_path_joiner(actual).open("w") as f_name:
            template = jinja_env.get_template(template_name).render()
            f_name.write(template)

    for template_name, actual in TEMPLATE_TO_RENDER_MAPPING.items():
        with cwd_path_joiner(actual).open("w") as f_name:
            template = jinja_env.get_template(template_name).render(
                project_name=project_name
            )
            f_name.write(template)
