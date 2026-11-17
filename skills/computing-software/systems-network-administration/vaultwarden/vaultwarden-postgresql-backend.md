---
id: computing-software.systems-network-administration.vaultwarden.vaultwarden-postgresql-backend
name: vaultwarden-postgresql-backend
category: computing-software
field: systems-network-administration
product: vaultwarden
tags: [vaultwarden, postgresql, database-url, libpq, pgloader, sqlite-migration, search-path]
level: advanced
status: docs-checked
description: "Run Vaultwarden on PostgreSQL: DATABASE_URL format, libpq options and custom schema, percent-encoding passwords, and the pgloader SQLite migration outline."
sources: ["https://github.com/dani-garcia/vaultwarden/wiki/Using-the-PostgreSQL-Backend"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Vaultwarden PostgreSQL backend

Use the official image (one image supports SQLite, MySQL and PostgreSQL) or a binary built with PostgreSQL support. Set `DATABASE_URL` for both container and binary:

```
-e 'DATABASE_URL=postgresql://user_name:user_password@db_host:5432/vaultwarden'
```
Format: `postgresql://[[user]:[password]@]host[:port][/database]`. The URL is parsed by libpq, so any libpq parameter works in the URL or through `PG*` environment variables; file paths must be valid inside the container. `?sslmode=require` enables TLS. A custom schema is selected with `application_name=vaultwarden&options=-c%20search_path%3Ddb_schema`. Passwords with special characters must be percent-encoded (`@` is `%40`, `:` is `%3A`, `/` is `%2F`, `=` is `%3D`).

Migrating from SQLite is called unsupported and not robustly tested; back up first. Outline: create a PostgreSQL user and an empty database owned by it; start Vaultwarden once against it so Diesel creates the schema, then stop it; disable WAL on the SQLite database; use pgloader with a load file that copies data only, renames the schema to `public`, and excludes the Diesel migrations table; run it and start Vaultwarden. From MySQL/MariaDB the approach is the same, but use pgloader 3.x latest, since distro versions can fail with newer PostgreSQL; errors usually mean an outdated pgloader. The data directory (attachments, keys) still needs separate backups.

## Checked

2026-11-03. Confirmed against the Vaultwarden wiki (https://github.com/dani-garcia/vaultwarden/wiki) by reading: Using-the-PostgreSQL-Backend.
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
