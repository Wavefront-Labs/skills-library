---
id: computing-software.systems-network-administration.immich.postgres-standalone-setup
name: postgres-standalone-setup
category: computing-software
field: systems-network-administration
product: immich
tags: [postgres, db-url, vectorchord, pgvector, shared-preload-libraries]
level: advanced
status: docs-checked
description: "Point Immich at a pre-existing Postgres server: pgvector, VectorChord install, shared_preload_libraries, supported versions and the DB_URL setting."
sources:
  - https://docs.immich.app/administration/postgres-standalone
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: run Immich against your own Postgres server instead of the bundled container. This is not officially recommended; you need baseline Postgres and Linux skills.

Prerequisites:

1. Install pgvector, a prerequisite for VectorChord. On Debian or Ubuntu, add the PostgreSQL Apt repository and run `apt install postgresql-NN-pgvector`, where NN is your Postgres major version.
2. Install VectorChord using its own instructions.
3. Add it to preloaded libraries in `postgresql.conf`:

```
shared_preload_libraries = 'vchord.so'
```

If other libraries are already listed, comma-separate them, for example `'pg_stat_statements, vchord.so'`.

Supported versions: Postgres `>= 14, < 20`; pgvector `>= 0.7, < 0.9`; VectorChord `>= 0.3, < 2.0`. The server checks the VectorChord version at startup and refuses to start if it is incompatible.

Connection: set `DB_URL` in the `.env` file.

```
DB_URL='postgresql://immichdbusername:immichdbpassword@postgreshost:postgresport/immichdatabasename'
```

Append `?sslmode=require` to require SSL, or `?sslmode=require&sslmode=no-verify` to require SSL without checking the certificate name.

By default Immich expects superuser permission. Grant it at the `psql` prompt with:

```sql
ALTER USER <immichdbusername> WITH SUPERUSER;
```

Automated database backups need superuser because they use `pg_dumpall`. A standalone server also allows logical replication and write-ahead log backups with tools such as pgBackRest or Barman.

## Checked

2026-11-03. Confirmed against the Immich docs (https://docs.immich.app/) by reading: administration/postgres-standalone (intro, Prerequisites, Specifying the connection URL, With superuser permission).
Removed or reworded: nothing needed removal.
Method: documentation only; no commands were run.
