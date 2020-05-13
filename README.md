# aedificator
Python project scaffolding tool.

## Installation

```bash
$ pip install aedificator
```

## Usage
In the directory where you want the scaffolding to happen, type
```bash
$ aedificate your_project_name
```
This will create a following structure:
```
current_working_directory
├── dev-requirements.txt
├── .dockerignore
├── .gitignore
├── Makefile
├── requirements.txt
├── setup.cfg
├── setup.py
├── src
│   └── your_project_name
│       ├── __init__.py
│       └── __version__.py
├── tests
│   └── __init__.py
└── tox.ini

```

You can now start putting your code in the `src/your_project_name` directory. 

---------------------------------------------------------------------------------------
To start developing, first, tweak `setup.py` file and type (preferably in some
dedicated virtual environment)
```bash
$ python setup.py develop
```
---------------------------------------------------------------------------------------
Aedificator comes with preconfigured formatting, linting, type checking and testing
options, leveraging the power of `tox`. If you do not have `tox` installed, type
```bash
$ pip install tox
```

Now, use
```bash
$ tox -e linters
```
for formatting, linting, and type checking (or `tox -e format|flake8|mypy` for just one
of them) and
```bash
$ tox -e py37|py38
```
for your test suites. 

Use
```
$ tox
``` 
if you want it all. ;)

---------------------------------------------------------------------------------------
A small note: `tox` will fail as long as you have no tests in your `tests` directory.
If you like to see green colour, while you still have no tests, limit yourself to
`tox -e linters` (and hurry to add some tests)