---
id: computing-software.database-administration.sql.naming-conventions
name: naming-conventions
category: computing-software
field: database-administration
product: sql
tags: [sql, naming-conventions]
level: intro
status: docs-checked
description: "Adopt consistent, quoting-free SQL naming conventions."
sources: ["https://www.postgresql.org/docs/current/sql-syntax-lexical.html", "https://www.postgresql.org/docs/current/ddl-constraints.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Naming conventions for tables and columns

- PostgreSQL folds unquoted names to lower case; quoting makes a name case-sensitive, so `"Foo"` and `foo` differ and every later reference needs the quotes. Use lowercase snake_case so quoting is never needed. The manual advises always quoting a name or never quoting it, for portability.
- Avoid key words as names: a delimited `"select"` works, but an unquoted `select` where a name is expected is a parse error.
- Identifiers are limited to 63 bytes by default (NAMEDATALEN is 64); longer names are silently truncated.
- Name constraints explicitly with `CONSTRAINT name ...`; otherwise the system picks a name. Explicit names make error messages clearer and let you alter or drop the constraint later. Apply the same habit to indexes (`orders_cid_idx`).
- Team conventions (not from the manual): pick singular or plural table names and keep it; foreign keys as `customer_id`; booleans as `is_active`; timestamps `created_at`; no type prefixes such as `tbl_`.
- Self-check: a lint rule or information_schema query flags names that are not lowercase snake_case.

## Checked

Date: 2026-11-08

Method: Read the PostgreSQL manual pages sql-syntax-lexical.html and ddl-constraints.html; folding, quoting, key-word, 63-byte and constraint-naming claims match, and the team conventions are labelled as non-manual advice.
