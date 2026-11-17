---
id: computing-software.database-administration.cloudnative-pg.bootstrap-methods-initdb-recovery-pg-basebackup
name: bootstrap-methods-initdb-recovery-pg-basebackup
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [bootstrap, initdb, recovery, pg-basebackup, externalclusters, postgres-user]
level: practitioner
status: docs-checked
description: "Pick a CloudNativePG bootstrap method (initdb, recovery, pg_basebackup), what each needs from externalClusters, and never delete postgres."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/bootstrap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Exactly one method is allowed in `spec.bootstrap`; defining several fails validation.

- `initdb` (default): create a new cluster from scratch, optionally importing databases from another server (see the import skill).
- `recovery`: restore a physical base backup and replay WAL, fully or to a point in time.
- `pg_basebackup`: clone a live cluster of the **same major version** over streaming replication.

`recovery` and `pg_basebackup` both create a cluster based on another one and rely on `externalClusters`, which makes them usable for replica clusters. An entry needs a `name` (referenced by `source`) plus a streaming connection, a Barman-Cloud-compatible recovery object store, or both:

| Content of externalClusters | pg_basebackup | recovery |
|:----------------------------|:-------------:|:--------:|
| Only streaming              | yes           |          |
| Only object store           |               | yes      |
| Streaming and object store  | yes           | yes      |

The object store holds the WAL archive (needed for PITR) and the base-backup catalog. By default `recovery` uses the external cluster `name` as the folder (server name) in the store; plugins can override it, for example the Barman Cloud Plugin `serverName` parameter.

Never delete the `postgres` user or `postgres` database. The operator connects over the local Unix socket as `postgres` with `peer` authentication to administer the cluster.

When a password is supplied in an `externalClusters` entry, the operator manages a password file at `/controller/external/NAME/pgpass` and references it through the `passfile` connection parameter, so passwords never appear in connection strings.

## Checked

2026-11-08. Read in full: docs/src/bootstrap.md (sections bootstrap, externalClusters, password files, recovery name note). Bootstrap methods, the externalClusters compatibility table and the postgres user warning confirmed on the Bootstrap page.

Method: documentation only; no commands were run.
