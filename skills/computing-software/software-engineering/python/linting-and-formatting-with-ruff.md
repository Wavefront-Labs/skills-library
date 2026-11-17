---
id: computing-software.software-engineering.python.linting-and-formatting-with-ruff
name: linting-and-formatting-with-ruff
category: computing-software
field: software-engineering
product: python
tags: [python, python-quality, ruff, python-linting, formatter, pep8, isort, pre-commit]
level: practitioner
status: verified
description: "Adopt ruff as linter and formatter: rule selection, per-file ignores, autofix safety, migrating from flake8/black/isort, and enforcing it in editors, hooks and CI."
sources:
  - https://docs.astral.sh/ruff/
  - https://docs.astral.sh/ruff/rules/
  - https://docs.astral.sh/ruff/formatter/
  - https://peps.python.org/pep-0008/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Linting and formatting with ruff

**Goal:** one fast tool replacing flake8, isort, pyupgrade and black, configured once and enforced everywhere.

## 1. Configuration
```toml
# pyproject.toml
[tool.ruff]
target-version = "py311"
line-length = 100
extend-exclude = ["migrations", "vendor"]

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "UP", "SIM", "C4", "PIE", "RUF", "S", "PT", "N", "DTZ", "PTH"]
ignore = ["E501"]                 # optional: the formatter wraps what it can, E501 still flags what it cannot (long strings); ruff docs say it can be used with the formatter
fixable = ["ALL"]
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]             # assert is fine in tests (add PLR2004 here only if you select PLR)
"__init__.py" = ["F401"]
[tool.ruff.lint.isort]
known-first-party = ["mypkg"]

[tool.ruff.format]
quote-style = "double"
docstring-code-format = true
```
Families: `F` pyflakes (real bugs), `B` bugbear (likely bugs), `UP` pyupgrade, `I` imports, `S` bandit security, `DTZ` naive datetimes, `PTH` prefer pathlib. Start with `F,E,W,I,B,UP`, add more per sprint.

## 2. Commands
```bash
ruff check .                  # lint
ruff check --fix .            # apply safe fixes
ruff check --fix --unsafe-fixes --diff .   # review unsafe ones first
ruff format .                 # format (black-compatible style)
ruff format --check .         # CI
ruff rule B008                # explain a rule
ruff check --statistics .     # counts per rule, for adoption planning
```

## 3. Adopting on a legacy codebase
1. `ruff format .` in one commit; add its sha to `.git-blame-ignore-revs`.
2. `ruff check --add-noqa .` to insert `# noqa: XXX` for current violations, so new code is clean immediately; burn down noqas over time.
3. Remove flake8/isort/black configs and their pre-commit hooks to avoid fights.

## 4. Enforce
- Editor: Ruff VS Code extension / `ruff server` LSP, format on save.
- pre-commit: `astral-sh/ruff-pre-commit` hooks `ruff-check` (with `args: [--fix]`) then `ruff-format` (`ruff` is a legacy alias of `ruff-check`).
- CI: `ruff check --output-format=github .` (inline annotations) and `ruff format --check .`.

## Gotchas
- Pin the ruff version; new releases add rules to existing selectors like `RUF` and can fail CI.
- Some lint rules conflict with the formatter (`COM812`, `ISC001`); `ruff format` prints a warning when `COM812` is selected (tested on 0.17.1); disable them. `E501` can be used alongside the formatter.
- `# noqa` without a code silences everything on the line; `RUF100` flags unused noqa.
- Safe fixes preserve behaviour; unsafe fixes may change semantics (e.g. removing unused variables with side effects).

## Verify
- `ruff check . && ruff format --check .` passes locally and in CI; introduce an unused import and confirm both the hook and CI fail.
