---
id: computing-software.database-administration.cloudnative-pg.pg-basebackup-clone-live-cluster
name: pg-basebackup-clone-live-cluster
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pg-basebackup, bootstrap, streaming-replication, clone, tablespacemapping, additionalargs, tls-client-cert]
level: advanced
status: docs-checked
description: "Clone a running PostgreSQL cluster into CloudNativePG with bootstrap.pg_basebackup: requirements, password versus TLS client certificate auth, additionalArgs and tablespaces."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/bootstrap.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Use `pg_basebackup` to create a physical copy for periodic BI or test clusters, quick replica clusters, or moving a cluster to another namespace or Kubernetes cluster. The community does **not** endorse it for migrating an external server into Kubernetes; use logical import instead.

Requirements: same architecture and major version; same tablespaces; enough `max_wal_senders` (one for the backup plus one for WAL streaming); network reachability; a role with `REPLICATION LOGIN` allowed in `pg_hba.conf` (create one with `createuser -P --replication streaming_replica`). A CloudNativePG source can reuse `streaming_replica`.

TLS client certificate (recommended):

```yaml
  bootstrap:
    pg_basebackup:
      source: cluster-example
  externalClusters:
  - name: cluster-example
    connectionParameters:
      host: cluster-example-rw.default.svc
      user: streaming_replica
      sslmode: verify-full
    sslKey:
      name: cluster-example-replication
      key: tls.key
    sslCert:
      name: cluster-example-replication
      key: tls.crt
    sslRootCert:
      name: cluster-example-ca
      key: ca.crt
```

Password auth uses `password: {name: source-db-replica-user, key: password}` instead and a source `pg_hba.conf` line such as `host replication streaming_replica all md5`.

`additionalArgs` (for example `--max-rate=50M`, `--checkpoint=fast`, `--sync-method=syncfs` on PG 17+) apply only to bootstrap; the operator rejects `-D`, `-F`, `-R`, `-X`, `-d`, `-h`, `-p`, `-U`, `-T`, `-C` and similar. For tablespaces, declare each in `spec.tablespaces` and map non-CloudNativePG paths with `tablespaceMapping` (`name`, `sourceLocation`); never run `CREATE TABLESPACE` on the source during the copy.

The result is a snapshot: the target starts on a new timeline and diverges, so stop writes to the source before cutover unless it is a replica cluster. Test the procedure repeatedly to measure downtime.

## Checked

2026-11-04. Requirements, both auth manifests, additionalArgs rejection list, tablespaceMapping and snapshot limitation confirmed on the Bootstrap page.

Method: documentation only; no commands were run.
