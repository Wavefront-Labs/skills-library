---
id: computing-software.collaboration-platform-administration.matrix-synapse.postgres-database-setup
name: postgres-database-setup
category: computing-software
field: collaboration-platform-administration
product: matrix-synapse
tags: [matrix, synapse, postgresql, psycopg2, database, createdb, connection-pool, keepalives]
level: practitioner
status: docs-checked
description: "Create the Synapse PostgreSQL user and UTF8 C-locale database, configure the database section with psycopg2 args and cp_ pool keys, and tune TCP keepalives and memory settings."
sources:
  - https://element-hq.github.io/synapse/latest/postgres.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Synapse needs the Python Postgres client library. With the matrix.org Debian/Ubuntu packages it is already installed but you must add the low-level library (`apt install libpq5`). In a virtualenv, install `"matrix-synapse[postgres]"` with pip; building needs the Postgres development files (`libpq-dev` on Debian-derived systems). The minimum supported PostgreSQL version follows the Dependency Deprecation Policy.

Create the role and database as the postgres user:

```sh
createuser --pwprompt synapse_user

createdb --encoding=UTF8 --locale=C --template=template0 --owner=synapse_user synapse
```

The encoding must be correct or UTF8 strings cannot be stored. You may also need to enable password authentication in `pg_hba.conf` so the role can connect.

Then point the `database` section at it:

```yaml
database:
  name: psycopg2
  args:
    user: <user>
    password: <pass>
    dbname: <db>
    host: <host>
    cp_min: 5
    cp_max: 10
```

Every key under `args` goes to `psycopg2.connect(..)` except keys starting `cp_`, which configure the Twisted adbapi connection pool. If the link between homeserver and database may drop, set the `keepalives_idle`, `keepalives_interval` and `keepalives_count` args (the page suggests 10, 10 and 3), otherwise Synapse can block for a long time waiting for a reply.

For larger deployments the page says the defaults are fine for most, but tuning `shared_buffers`, `effective_cache_size`, `work_mem`, `maintenance_work_mem` and `autovacuum_work_mem` helps; right values depend on free memory on the database host. Huge pages may help with large `shared_buffers`.

Before a PostgreSQL major-version upgrade, stop Synapse and companion services, and back up the database first.

## Checked

2026-11-04. Confirmed against the Synapse Using Postgres page: client library install, createuser and createdb commands, database config block, cp_ keys, keepalives, tuning list, huge pages, major-version upgrade note. Nothing removed.
Method: documentation only; no commands were run.
