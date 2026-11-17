---
id: computing-software.database-administration.cloudnative-pg.pooler-pgbouncer-quickstart-and-lifecycle
name: pooler-pgbouncer-quickstart-and-lifecycle
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [pooler, pgbouncer, connection-pooling, poolmode, rw-service, lifecycle]
level: practitioner
status: docs-checked
description: "Deploy a PgBouncer Pooler for a CloudNativePG cluster with poolMode and parameters; its lifecycle is independent, spec.cluster is immutable and the name must be unique."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/connection_pooling.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `Pooler` is a Deployment of PgBouncer pods in front of a cluster service such as `rw`, giving a scalable, highly available database access layer. PgBouncer 1.19 or higher is required because CloudNativePG relies on `auth_dbname`.

```yaml
apiVersion: postgresql.cnpg.io/v1
kind: Pooler
metadata:
  name: pooler-example-rw
spec:
  cluster:
    name: cluster-example

  instances: 3
  type: rw
  pgbouncer:
    poolMode: session
    parameters:
      max_client_conn: "1000"
      default_pool_size: "10"
```

Rules:

- The pooler name cannot equal any cluster name in the namespace.
- It must live in the same namespace as the Postgres cluster.
- `spec.cluster` is immutable; to retarget, create a new `Pooler`.
- The operator also creates a Secret named like the pooler with the PgBouncer configuration files.
- Only the `*` fallback database is set in PgBouncer, so client connection-string parameters are relayed to PostgreSQL.

Poolers are not created automatically. You can run none, one or several per cluster (for example one per application). The lifecycles are independent: deleting a cluster does not remove its poolers and deleting a pooler does not touch the cluster. When the operator is upgraded, the pooler pods are rolled too, so the instance manager inside stays consistent.

The exposed service distributes clients randomly across the pooler pods. With multiple availability zones and high latency between them, remember the extra network hops (app in zone 2, PgBouncer in zone 3, primary in zone 1).

## Checked

2026-11-04. Trimmed claims the page does not state. Pooler manifest, name and immutability rules and lifecycle notes confirmed on the Connection pooling page.

Method: documentation only; no commands were run.
