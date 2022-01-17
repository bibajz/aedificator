import typing as t
from pathlib import Path


def extract_names_from_dir(dir: Path) -> t.Iterable[str]:
    for f in dir.iterdir():
        yield f.name


if __name__ == "__main__":
    import sys

    from aedificator.main import TEMPLATES

    template_dir = Path("./src/aedificator/templates").resolve()
    templates_in_script = sorted(t.name for t in TEMPLATES)
    templates_in_dir = sorted(extract_names_from_dir(template_dir))

    # We need to negate the equality, since `sys.exit(True)` results in exit code 1.
    sys.exit(not templates_in_dir == templates_in_script)
