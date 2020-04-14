from setuptools import find_namespace_packages, setup

__version__ = "1.1.1"

setup(
    name="aedificator",
    version=__version__,
    description="aedificator - Python project scaffolding tool",
    keywords="automation scaffolding",
    classifiers=[
        "Development Status :: 4 - Beta",
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
    package_dir={"": "src"},
    package_data={"": ["*.txt"]},
    packages=find_namespace_packages(where="src"),
    include_package_data=True,
    install_requires=["Jinja2", "click"],
    entry_points={"console_scripts": ["aedificate = aedificator.main:main"]},
)
