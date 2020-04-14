import os
from functools import partial

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

    cwd = os.getcwd()
    cwd_path_joiner = partial(os.path.join, cwd)

    # Create package structure.
    for d_name in ["tests", f"src/{project_name}"]:
        dir_path = cwd_path_joiner(d_name)
        try:
            os.makedirs(dir_path)
        except OSError:
            # Directories already exist. Fine by me.
            pass

        with open(os.path.join(dir_path, "__init__.py"), "w"):
            pass

    with open(cwd_path_joiner("requirements.txt"), "w"):
        pass

    jinja_env = Environment(loader=PackageLoader("aedificator", "templates"))

    for template_name, actual in TEMPLATE_MAPPING.items():
        with open(cwd_path_joiner(actual), "w") as f_name:
            template = jinja_env.get_template(template_name).render()
            f_name.write(template)

    for template_name, actual in TEMPLATE_TO_RENDER_MAPPING.items():
        with open(cwd_path_joiner(actual), "w") as f_name:
            template = jinja_env.get_template(template_name).render(
                project_name=project_name
            )
            f_name.write(template)
