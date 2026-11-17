---
id: computing-software.cybersecurity-defensive.zitadel.postgres-connection-and-managed-databases
name: postgres-connection-and-managed-databases
category: computing-software
field: cybersecurity-defensive
product: zitadel
tags: [zitadel, postgresql, database, dsn, managed-database, init-schema]
level: advanced
status: docs-checked
description: "Connect ZITADEL to PostgreSQL by DSN, tune the pool, and prepare managed databases where you have no superuser using zitadel init schema."
sources:
  - https://zitadel.com/docs/self-hosting/manage/database
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
PostgreSQL is ZITADEL's database; versions 14 to 18 are supported. Provide a DSN through the environment:

```bash
export ZITADEL_DATABASE_POSTGRES_DSN=postgresql://zitadel:password@localhost:5432/zitadel?sslmode=disable
```

or in YAML under `Database.postgres` with `DSN`, `MaxOpenConns: 15`, `MaxIdleConns: 10`, `MaxConnLifetime: 1h` and `MaxConnIdleTime: 5m` as the documented example. TLS is set by DSN query parameters, for example `sslmode=verify-full&sslrootcert=/path/to/ca.crt`.

Managed services such as RDS, Cloud SQL or Azure Database give no superuser. Init does two things: provisioning (`CREATE ROLE`, `CREATE DATABASE`, `GRANT`, needs an admin) and schema bootstrapping (creates the `eventstore`, `projections` and `system` schemas and tables, needs only database owner privileges). Create the role and database yourself with a strong password, set `Database.postgres.Admin.ExistingDatabase`, and still run:

```bash
zitadel init schema
```

Skipping it causes `relation "eventstore.events" does not exist` errors. The alias `zitadel init zitadel` also works.

Do not use trivial passwords in production; store the password in a secret manager. Pool values and the DSN can be given as environment variables or in a configuration file.

## Checked

2026-11-08. Read in full: the database page. Dropped the configuration reference source, which was not read in full (it is very large). Removed the unsupported backup advice and reworded the credentials advice to what the page states.

Method: documentation only; no commands were run.
