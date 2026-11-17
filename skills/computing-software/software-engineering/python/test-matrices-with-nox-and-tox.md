---
id: computing-software.software-engineering.python.test-matrices-with-nox-and-tox
name: test-matrices-with-nox-and-tox
category: computing-software
field: software-engineering
product: python
tags: [python, python-testing, nox, tox, test-matrix, multi-version, ci, uv]
level: practitioner
status: verified
description: "Run tests, linters and builds across Python versions and dependency sets with nox or tox, locally and in CI, with fast uv-backed environments."
sources:
  - https://nox.thea.codes/en/stable/
  - https://tox.wiki/en/latest/
  - https://docs.github.com/en/actions/use-cases-and-examples/building-and-testing/building-and-testing-python
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Multi-version test matrices with nox and tox

**Goal:** one command reproduces the CI matrix locally: each Python version, minimum and latest dependencies, lint and docs.

## 1. nox (Python file, flexible)
```python
# noxfile.py
import nox
nox.options.default_venv_backend = "uv|virtualenv"
nox.options.sessions = ["lint", "tests"]
PYTHONS = ["3.10", "3.11", "3.12", "3.13"]

@nox.session(python=PYTHONS)
def tests(session):
    session.install("-e", ".[test]")
    session.run("pytest", "--cov=mypkg", *session.posargs)

@nox.session(python="3.10")
def tests_min_deps(session):
    session.install("-e", ".[test]", "--resolution=lowest-direct") if session.venv_backend == "uv" else \
        session.install("-c", "constraints-min.txt", "-e", ".[test]")
    session.run("pytest")

@nox.session
def lint(session):
    session.install("ruff", "mypy")
    session.run("ruff", "check", ".")
    session.run("mypy", "src")

@nox.session
@nox.parametrize("django", ["4.2", "5.1"])
def django_compat(session, django):
    session.install(f"django~={django}.0", "-e", ".[test]")
    session.run("pytest", "tests/django")
```
```bash
nox -l                       # list sessions
nox -s tests-3.12 -- -k api  # one session, pass args to pytest
nox -R                       # reuse venvs, skip installs
```

## 2. tox (declarative)
```toml
# tox.toml (tox 4.21+) or [tool.tox] in pyproject
env_list = ["3.13", "3.12", "3.11", "lint"]
[env_run_base]
extras = ["test"]
commands = [["pytest", { replace = "posargs", default = ["tests"], extend = true }]]   # extend = true is required, else tox fails with "['tests'] is not of type 'str'"
[env.lint]
skip_install = true
deps = ["ruff"]
commands = [["ruff", "check", "."]]
```
`tox -e 3.12`, `tox p` (parallel), `tox -r` (recreate). `nox -R` reuses venvs and skips reinstall. Pass pytest args after `--`. `tox-uv` plugin makes env creation fast.

## 3. CI
Let CI provide interpreters and call the same sessions:
```yaml
strategy:
  matrix: { python: ["3.10", "3.11", "3.12", "3.13"] }
steps:
  - uses: actions/setup-python@v5   # v5 still works; latest major was v7 when reviewed
    with: { python-version: "${{ matrix.python }}" }
  - run: pipx run nox -s tests-${{ matrix.python }}
```

## Gotchas
- Missing interpreters: nox errors (or skips with `--no-error-on-missing-interpreters`); use `uv python install 3.10 3.11` locally.
- Testing against an editable install hides packaging bugs; add one session that builds the wheel and installs it (`session.install(dist_wheel)`).
- Minimum-version testing is what catches `>=` lower bounds that no longer work.
- Keep tool versions pinned in sessions or the lint session breaks on new rule releases.

## Verify
- `nox` (or `tox`) on a clean machine runs every default session green, and CI job names map one-to-one to sessions.
