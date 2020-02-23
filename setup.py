from setuptools import setup, find_packages


setup(
    name="aedificator",
    version="1",
    description="aedificator - Python project scaffolding tool.",
    url="https://github.com/bibajz/aedificator",
    author="Libor Martinek",
    packages=find_packages(),
    install_requires=["Jinja2", "click"],
    entry_points={"console_scripts": ["aedificate = aedificator.main:main"]},
)
