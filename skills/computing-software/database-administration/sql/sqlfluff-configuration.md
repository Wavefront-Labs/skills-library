---
id: computing-software.database-administration.sql.sqlfluff-configuration
name: sqlfluff-configuration
category: computing-software
field: database-administration
product: sql
tags: [sql, sqlfluff-configuration]
level: practitioner
status: docs-checked
description: "Lint and autoformat SQL with SQLFluff and a project config."
sources: ["https://docs.sqlfluff.com/en/stable/configuration/index.html", "https://docs.sqlfluff.com/en/stable/reference/cli.html", "https://docs.sqlfluff.com/en/stable/gettingstarted.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SQLFluff lint and fix configuration

- Install with `pip install sqlfluff`. Try it with `sqlfluff lint test.sql --dialect ansi`; each violation shows line, position, a rule code (such as LT01) and a description.
- Config files read: `setup.cfg`, `tox.ini`, `pep8.ini`, `.sqlfluff` and `pyproject.toml`; later files override earlier ones. The cfg-style files use a `[sqlfluff]` section with colon-separated subsections (`[sqlfluff:templater:jinja]`); `pyproject.toml` uses `[tool.sqlfluff...]`. Config files in subdirectories cannot set `templater`.
- Keys: `dialect` (for example `postgres`; choose the one that matches your engine, and see `sqlfluff dialects` for the list), `max_line_length` (default 80; zero or negative disables the check), `exclude_rules` (comma-separated rule codes or names), `sql_file_exts`, `processes`.
- `templater` is one of `raw`, `jinja`, `python` or `placeholder`; dbt projects use the dbt templater with `[sqlfluff:templater:dbt] project_dir`. Use a templater only when the SQL is templated.
- Commands: `sqlfluff lint` (report), `sqlfluff fix` (apply fixes to a file, directory or stdin), `sqlfluff format` (autoformat; forces `fix` with a known subset of fairly stable rules, still respecting rule exclusions), plus `parse`, `render`, `rules`, `dialects` and `version`.
- Run lint in CI and pre-commit: the SQLFluff docs have separate Pre-commit and CI/CD Integration guides.
- Self-check: lint a messy file, run fix, and confirm lint passes.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed against the SQLFluff configuration, CLI and getting-started pages. Removed: the specific `LT05` exclusion and `max_line_length = 100` example (the rules page did not show that rule code; the default is 80) and the dbt/jinja pairing as an unqualified rule.
