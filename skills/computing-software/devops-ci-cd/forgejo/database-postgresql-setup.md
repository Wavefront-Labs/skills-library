---
id: computing-software.devops-ci-cd.forgejo.database-postgresql-setup
name: database-postgresql-setup
category: computing-software
field: devops-ci-cd
product: forgejo
tags: [postgresql-setup, pg-hba-conf, scram-sha-256, create-role]
level: practitioner
status: docs-checked
description: "Create a PostgreSQL role and UTF-8 database for Forgejo and allow it in pg_hba.conf with scram-sha-256."
sources:
  - https://forgejo.org/docs/latest/admin/installation/database-preparation/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On the database server, open a superuser console with `su -c "psql" - postgres`. Create a login role: `CREATE ROLE forgejo WITH LOGIN PASSWORD '<strong-password>';`. Then create a UTF-8 database owned by it, using template0 so the collation can be chosen:

`CREATE DATABASE forgejodb WITH OWNER forgejo TEMPLATE template0 ENCODING UTF8 LC_COLLATE 'en_US.UTF-8' LC_CTYPE 'en_US.UTF-8';`

Any libc collation may be given for LC_COLLATE and LC_CTYPE depending on expected content, and the names can be changed.

Next allow the role in `pg_hba.conf`. For a local database add a `local` line plus `host` lines for 127.0.0.1/32 and ::1/128, each with database `forgejodb`, user `forgejo` and method `scram-sha-256`. For a remote database add one `host` line with the Forgejo server address, for example 192.0.2.10/32.

Rules in pg_hba.conf are evaluated in order and the first match wins. If your distribution ships generic rules matching all users and databases, place the Forgejo rules above them. Restart PostgreSQL to apply the new authentication rules. The page also says to protect the root user with a secure password or disable the login.

## Checked

2026-11-04. Confirmed against the Forgejo Database Preparation page (PostgreSQL section): the psql console command, CREATE ROLE, CREATE DATABASE with template0 and libc collation, the pg_hba.conf lines for local and remote, first-match ordering and the restart. Reworded the last security sentence to match the page.

Method: documentation only; no commands were run.
