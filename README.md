# Poetry Template

Django app template, using `poetry-python` as dependency manager.

This project is a template that can be cloned and re-used for
redistributable apps.

It includes the following:

* `poetry` for dependency management
* `isort`, `black`, `pyupgrade` and `flake8` linting
* `pre-commit` to run linting
* `mypy` for type checking
* `tox` and Github Actions for builds and CI

There are default config files for the linting and mypy.

## Principles

The motivation for this project is to provide a consistent set of
standards across all YunoJuno public Python/Django projects. The
principles we want to encourage are:

* Simple for developers to get up-and-running
* Consistent style (`black`, `isort`, `flake8`)
* Future-proof (`pyupgrade`)
* Full type hinting (`mypy`)

## Versioning

We currently support Python 3.7+, and Django 3.2+. We will aggressively
upgrade Django versions, and we won't introduce hacks to support
breaking changes - if Django 4 introduces something that 2.2 doesn't
support we'll drop it.

## Tests

#### Tests package

The package tests themselves are _outside_ of the main library code, in
a package that is itself a Django app (it contains `models`, `settings`,
and any other artifacts required to run the tests (e.g. `urls`).) Where
appropriate, this test app may be runnable as a Django project - so that
developers can spin up the test app and see what admin screens look
like, test migrations, etc.

#### Running tests

The tests themselves use `pytest` as the test runner. If you have
installed the `poetry` evironment, you can run them thus:

```
$ poetry run pytest
```

or

```
$ poetry shell
(my_app) $ pytest
```

The full suite is controlled by `tox`, which contains a set of
environments that will format, lint, and test against all
support Python + Django version combinations.

```
$ tox
...
______________________ summary __________________________
  fmt: commands succeeded
  lint: commands succeeded
  mypy: commands succeeded
  py37-django22: commands succeeded
  py37-django32: commands succeeded
  py37-djangomain: commands succeeded
  py38-django22: commands succeeded
  py38-django32: commands succeeded
  py38-djangomain: commands succeeded
  py39-django22: commands succeeded
  py39-django32: commands succeeded
  py39-djangomain: commands succeeded
```

#### CI

There is a `.github/workflows/tox.yml` file that can be used as a
baseline to run all of the tests on Github. This file runs the oldest
(2.2), newest (3.2), and head of the main Django branch.
