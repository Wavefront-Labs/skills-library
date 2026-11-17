---
id: computing-software.database-administration.sql.sql-style-and-readability
name: sql-style-and-readability
category: computing-software
field: database-administration
product: sql
tags: [sql, sql-style-guide, sql-formatting, sqlfluff, naming-conventions]
level: intro
status: draft
description: "Format and name SQL consistently using a style guide and enforce it with a linter such as SQLFluff."
sources: ["https://www.postgresql.org/docs/current/", "https://www.sqlite.org/docs.html", "https://www.iso.org/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SQL style

- Conventions (Simon Holywell's sqlstyle.guide, GitLab and dbt style guides): keywords upper or lower case but consistent, one clause per line, one select-list column per line, trailing or leading commas per team choice, explicit `AS` for aliases, meaningful aliases rather than `a, b, c`, explicit `JOIN` types, comments for intent not mechanics (`--` and `/* */`).
- Naming: lower `snake_case`, avoid reserved words and quoted mixed-case identifiers (PostgreSQL folds unquoted names to lower, so `"UserId"` forces quoting forever).
- Enforce: `sqlfluff lint` and `sqlfluff fix` with `--dialect postgres` (set the dialect, otherwise parse errors); keep a `.sqlfluff` config in the repo and run in CI and pre-commit.
- Qualify every column with its table alias in multi-table queries.
- Do not format by hand in reviews; automate.
