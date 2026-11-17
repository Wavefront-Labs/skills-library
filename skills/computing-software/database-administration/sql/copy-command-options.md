---
id: computing-software.database-administration.sql.copy-command-options
name: copy-command-options
category: computing-software
field: database-administration
product: sql
tags: [sql, copy-command-options]
level: practitioner
status: docs-checked
description: "Load and export data with PostgreSQL COPY and psql client copy."
sources: ["https://www.postgresql.org/docs/current/sql-copy.html", "https://www.postgresql.org/docs/current/app-psql.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# COPY and psql copy options

- Server-side: `COPY t (a,b) FROM '/path/file.csv' WITH (FORMAT csv, HEADER true, NULL '');` the file is read or written directly by the server, so it must be accessible to the server.
- Client-side: `\copy t FROM 'file.csv' CSV HEADER` performs a frontend (client) copy.
- Export: `COPY (SELECT ...) TO STDOUT WITH CSV HEADER`.
- By default COPY fails on an error; the `ON_ERROR` option (for example `ON_ERROR ignore`) selects other behaviour. Alternatively load into a staging table then `INSERT ... SELECT` with cleaning.
- Self-check: compare row counts and a checksum column afterwards.

## Checked

2026-11-02. Confirmed: server-side file access, `\copy` as a client-side copy, COPY ... TO STDOUT, default failure on error and the ON_ERROR option with ignore (COPY and psql pages). Removed: the PostgreSQL 17 version attribution.
Method: documentation only; no commands were run.
