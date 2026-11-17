---
id: computing-software.database-administration.patroni.patroni-pg-hba-and-ident-management
name: patroni-pg-hba-and-ident-management
category: computing-software
field: database-administration
product: patroni
tags: [patroni, pg-hba, pg-ident, authentication, bootstrap]
level: practitioner
status: docs-checked
description: "Let Patroni generate pg_hba.conf and pg_ident.conf from YAML lines, and the replication line it requires."
sources:
  - https://patroni.readthedocs.io/en/latest/yaml_configuration.html
  - https://patroni.readthedocs.io/en/latest/dynamic_configuration.html
  - https://patroni.readthedocs.io/en/latest/existing_data.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: manage host-based authentication through Patroni.

```
postgresql:
  pg_hba:
    - host all all 0.0.0.0/0 md5
    - host replication replicator 127.0.0.1/32 md5
  pg_ident:
    - mapname1 systemname1 pguser1
```

- Patroni uses `pg_hba` lines to generate pg_hba.conf and `pg_ident` lines to generate pg_ident.conf.
- Each is ignored if the PostgreSQL parameter `hba_file` (or `ident_file`) is set to a non-default value.
- A replication line like the second above is required for replication.
- The same keys can be placed in dynamic configuration, which together simplifies managing the files cluster-wide.

Related items:
- `authentication.superuser`, `replication` and `rewind` blocks hold usernames and passwords; the replication user is created during initialization. The rewind user is created on PostgreSQL 11+ with the needed permissions.
- Each block accepts optional libpq-mapped keys such as `sslmode` (default `prefer`), `sslkey`, `sslcert`, `sslrootcert`, `sslcrl`.
- If `postgresql.config_dir` is used and PGDATA is not empty on first start, no bootstrap happens (Patroni generates pg_hba.conf from the bootstrap section only when it bootstraps a new cluster), so the pg_hba.conf file must exist beforehand; see the standalone conversion page.

## Checked

2026-11-08: pg_hba and pg_ident behaviour, authentication blocks and ssl keys confirmed in the YAML configuration page; the required replication line and dynamic configuration use confirmed in the dynamic configuration page; the config_dir caveat confirmed in the existing data page. Removed: the claim about PostgreSQL 10 divergence checks connecting to the postgres database, which no fetched page states. Pages were read in full except where noted. Partial reads: the YAML configuration and existing data pages were searched for the relevant passages.

Method: documentation only; no commands were run.
