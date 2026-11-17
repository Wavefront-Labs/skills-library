---
id: computing-software.email-administration.mail-server-administration.sql-lookup-tables
name: sql-lookup-tables
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sql-lookup-tables, mysql-table, pgsql-table, sql-lookup]
level: advanced
status: docs-checked
description: "Back Postfix virtual maps with MySQL/PostgreSQL lookup tables, including query files and connection settings."
sources:
  - https://www.postfix.org/pgsql_table.5.html
  - https://www.postfix.org/DATABASE_README.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sql lookup tables

**Goal:** manage domains and mailboxes in a database.
## Steps
1. `virtual_mailbox_maps = pgsql:/etc/postfix/pgsql-mailboxes.cf`
2. Query file: `hosts = 127.0.0.1`, `user = mailro`, `password = ...`, `dbname = mail`, `query = SELECT 1 FROM mailbox WHERE email='%s'`.
3. Keep the file out of world-readable main.cf: pgsql_table(5) notes main.cf is normally world-readable, so put credentials in the separate query file and restrict its permissions.
4. Test: `postmap -q alice@example.com pgsql:/etc/postfix/pgsql-mailboxes.cf`.
## Failure modes
- DB unreachable: lookups fail; monitor the connection.
- Chrooted processes cannot reach a unix socket (`hosts = unix:/file/name`) outside the jail.
## Verify
- `postmap -q` returns a row for an existing mailbox and nothing for an unknown address.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): pgsql_table(5), DATABASE_README.
Confirmed: `hosts`, `user`, `password`, `dbname`, `query` with `%s`, `postmap -q` against a `pgsql:` table, world-readable main.cf note.
Corrected or removed: the `chmod 640` figure and the defer-not-reject claim (not in the pages read).
Method: documentation only; no commands were run.
