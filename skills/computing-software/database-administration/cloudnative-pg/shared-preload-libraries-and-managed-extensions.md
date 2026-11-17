---
id: computing-software.database-administration.cloudnative-pg.shared-preload-libraries-and-managed-extensions
name: shared-preload-libraries-and-managed-extensions
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [shared-preload-libraries, auto-explain, pg-stat-statements, pgaudit, pg-failover-slots, extensions]
level: advanced
status: docs-checked
description: "Enable auto_explain, pg_stat_statements, pgaudit and pg_failover_slots by setting prefixed parameters and let the operator manage shared_preload_libraries and CREATE EXTENSION."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/postgresql_conf.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`shared_preload_libraries` is empty by default and expert-only to set: if a listed library is missing the server will not start and self-healing cannot help. Extra libraries go in `.spec.postgresql.shared_preload_libraries` as a list and are merged with the managed ones. Removing a library requires a restart of all instances.

Managed extensions: `auto_explain`, `pg_stat_statements`, `pgaudit`, `pg_failover_slots`. When any parameter starting with the extension name and a dot appears, the operator adds the library and, where needed, runs `CREATE EXTENSION` in every database from `SELECT datname FROM pg_database WHERE datallowconn` (this includes `template1`); it removes them when no parameter needs them. The page notes that declarative extensions in the `Database` CRD may supersede this feature.

```yaml
  postgresql:
    parameters:
      auto_explain.log_min_duration: "10s"
      pg_stat_statements.max: "10000"
      pg_stat_statements.track: all
      pgaudit.log: "all, -misc"
      pgaudit.log_catalog: "off"
      pgaudit.log_parameter: "on"
      pgaudit.log_relation: "on"
```

`auto_explain` can cause performance issues. The page notes native support for PGAudit logs (see its PGAudit logs section).

`pg_failover_slots` (EDB) lets logical replication slots survive failover. Besides any `pg_failover_slots.*` parameter, each database you use with it needs a `pg_hba` entry so replicas can connect to the primary, for example for the `app` database:

```yaml
  postgresql:
    pg_hba:
      - hostssl app streaming_replica all cert
```

## Checked

2026-11-04. Trimmed claims the page does not state. Managed extension list, parameter-prefix trigger, extension creation query and pg_failover_slots pg_hba entry confirmed on the PostgreSQL Configuration page.

Method: documentation only; no commands were run.
