---
id: computing-software.database-administration.cloudnative-pg.standalone-replica-cluster-streaming-and-archive
name: standalone-replica-cluster-streaming-and-archive
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [replica-cluster, standalone-replica, pg-basebackup, streaming, continuous-recovery, read-only, promotion]
level: practitioner
status: docs-checked
description: "Build a standalone replica cluster for read-only use with pg_basebackup or recovery and spec.replica.enabled; disabling is irreversible."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replica_cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A standalone replica cluster is in continuous recovery with `.spec.replica.enabled: true` and `.spec.replica.source` naming an `externalClusters` entry. It suits reporting or OLAP; for disaster recovery prefer the distributed topology. It can only be promoted: no controlled switchover exists, and the former primary must be re-cloned. Failover works the same as in a distributed topology.

Streaming bootstrap and continuous recovery:

```yaml
  bootstrap:
    pg_basebackup:
      source: cluster-example

  replica:
    enabled: true
    source: cluster-example
```

Connect over TLS; copy the `-replication` and `-ca` secrets if the replica lives in another namespace, and use the right namespace in `host`:

```yaml
  externalClusters:
  - name: <MAIN-CLUSTER>
    connectionParameters:
      host: <MAIN-CLUSTER>-rw.<NAMESPACE>.svc
      user: streaming_replica
      sslmode: verify-full
      dbname: postgres
    sslKey:
      name: <MAIN-CLUSTER>-replication
      key: tls.key
    sslCert:
      name: <MAIN-CLUSTER>-replication
      key: tls.crt
    sslRootCert:
      name: <MAIN-CLUSTER>-ca
      key: ca.crt
```

To bootstrap from an object store or volume snapshot, use `bootstrap.recovery.source` instead; the example then mixes streaming (basic authentication with the superuser secret) and the object store for WAL. The defaults assume the app database and owner are `app`.

Setting `enabled: false` promotes the designated primary and detaches for good: the two clusters become independent. This is **irreversible**. Roles stay as in the source until promotion, so copy the app user secret if you plan to promote.

## Checked

2026-11-08. Bootstrap and replica snippets, externalClusters TLS example and the irreversible warning confirmed on the Replica clusters page, section Standalone Replica Clusters.

Method: documentation only; no commands were run.
