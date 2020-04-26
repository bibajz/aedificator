from setuptools import find_namespace_packages, setup

__version__ = "1.1.3"


def get_long_description() -> str:
    with open("README.md", encoding="utf8") as f:
        long_description = f.read()
    return long_description


setup(
    name="aedificator",
    version=__version__,
    description="aedificator - Python project scaffolding tool",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    keywords="automation scaffolding",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    url="https://github.com/bibajz/aedificator",
    author="Libor Martinek",
    author_email="libasmartinek@protonmail.com",
    package_dir={"": "src"},
    package_data={"": ["*.txt"]},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    install_requires=["Jinja2", "click"],
    entry_points={"console_scripts": ["aedificate = aedificator.main:main"]},
)
