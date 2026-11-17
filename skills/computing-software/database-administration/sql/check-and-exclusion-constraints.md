---
id: computing-software.database-administration.sql.check-and-exclusion-constraints
name: check-and-exclusion-constraints
category: computing-software
field: database-administration
product: sql
tags: [sql, check-and-exclusion-constraints]
level: practitioner
status: docs-checked
description: "Enforce domain rules with CHECK, NOT NULL and PostgreSQL EXCLUDE constraints."
sources: ["https://www.postgresql.org/docs/current/ddl-constraints.html", "https://www.postgresql.org/docs/current/btree-gist.html", "https://www.postgresql.org/docs/current/sql-altertable.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CHECK NOT NULL and exclusion constraints

- `CHECK (qty > 0 AND status IN ('new','done'))`; name constraints: `CONSTRAINT qty_pos CHECK (...)`.
- CHECK passes on NULL, so pair with NOT NULL.
- `EXCLUDE USING gist (room WITH =, during WITH &&)` prevents overlapping bookings (the `btree_gist` extension provides GiST operator classes with B-tree behaviour for scalar types, so they can be combined with `&&`).
- Adding a CHECK: `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT`.
- Self-check: insert one violating row and read the error message.

## Checked

2026-11-02. Confirmed: a CHECK passes when the expression is true or null; EXCLUDE USING gist syntax (constraints page); btree_gist operator classes (btree_gist page); NOT VALID and VALIDATE CONSTRAINT for CHECK constraints (ALTER TABLE page). Removed: the large-table and readable-error rationales.
Method: documentation only; no commands were run.
