---
id: computing-software.systems-network-administration.paperless-ngx.mariadb-collation-mix
name: mariadb-collation-mix
category: computing-software
field: systems-network-administration
product: paperless-ngx
tags: [paperless-ngx, mariadb, illegal-mix-of-collations, collation, paperless-db-options, convert-mariadb-uuid]
level: advanced
status: docs-checked
description: "Fix MariaDB or MySQL 'Illegal mix of collations' errors and the transaction_id 'Data too long' error left over from older Paperless versions."
sources:
  - "https://docs.paperless-ngx.com/troubleshooting/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MariaDB collation and UUID errors

## Illegal mix of collations
```
(1267, "Illegal mix of collations (utf8mb4_general_ci,IMPLICIT) and (utf8mb4_unicode_ci,IMPLICIT) for operation '='")
```
Tables in the database use different collations. This is common on databases that predate a MariaDB or MySQL upgrade: old tables keep their collation while new ones use the new server default.

### Quick workaround
Set the collation your existing tables use (the one in the error that is not `utf8mb4_unicode_ci`):
```bash
PAPERLESS_DB_OPTIONS="collation=utf8mb4_general_ci"
```

### Permanent fix
Back up, then convert the database and every table to one collation and remove the override:
```sql
ALTER DATABASE paperless CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
ALTER TABLE <table_name> CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## "Data too long for column 'transaction_id'"
Seen when deleting documents on installs that upgraded from a Django 4 era release (before v2.13.0) with MariaDB or MySQL. Django 5 changed the column type, so recreate the column once:
```bash
python3 manage.py convert_mariadb_uuid
```
Run it with the usual management command prefix for your install (`docker compose exec webserver ...` in Docker).

## Checked
2026-11-04. Compared with the Illegal mix of collations and transaction_id sections of troubleshooting (Markdown source of the Paperless-ngx docs; the rendered site blocks scripts). Confirmed: error text, cause, PAPERLESS_DB_OPTIONS workaround, permanent fix statements, Django 5 column re-creation, convert_mariadb_uuid, management command prefix from administration. Nothing removed.

Method: documentation only; no commands were run.
