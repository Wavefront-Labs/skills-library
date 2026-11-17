---
id: computing-software.database-administration.sql.identity-columns-vs-serial
name: identity-columns-vs-serial
category: computing-software
field: database-administration
product: sql
tags: [sql, identity-columns-vs-serial]
level: practitioner
status: docs-checked
description: "Prefer GENERATED AS IDENTITY over SERIAL and manage sequences safely."
sources: ["https://www.postgresql.org/docs/current/sql-createtable.html", "https://www.postgresql.org/docs/current/sql-insert.html", "https://www.postgresql.org/docs/current/datatype-numeric.html", "https://www.postgresql.org/docs/current/functions-sequence.html", "https://www.postgresql.org/docs/current/functions-info.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Identity columns versus SERIAL

- `id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY`; SERIAL creates a sequence and a default, and marks the sequence as owned by the column.
- `ALWAYS` rejects explicit values unless `OVERRIDING SYSTEM VALUE`; `BY DEFAULT` allows them.
- After bulk loading explicit ids: `SELECT setval(pg_get_serial_sequence('t','id'), max(id)) FROM t;`.
- Sequence changes made by `setval` are not undone if the transaction rolls back, so do not expect gap-free values.
- Self-check: insert after a COPY load and confirm no duplicate-key error.

## Checked

2026-11-02. Confirmed: GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY, OVERRIDING SYSTEM VALUE behaviour (CREATE TABLE and INSERT pages); serial creates an owned sequence (numeric types page); setval and pg_get_serial_sequence (sequence and system information function pages). Removed: version attributions, the 'legacy' label, the 'standard SQL' remark, and the general gap claim beyond setval.
Method: documentation only; no commands were run.
