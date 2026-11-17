---
id: computing-software.database-administration.patroni.patroni-kubernetes-health-probes
name: patroni-kubernetes-health-probes
category: computing-software
field: database-administration
product: patroni
tags: [patroni, kubernetes, liveness, readiness, probes]
level: practitioner
status: docs-checked
description: "Use /liveness and /readiness REST endpoints as Kubernetes probes with the documented example settings."
sources:
  - https://patroni.readthedocs.io/en/latest/rest_api.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: gate pod readiness on replication catch-up.

- `GET /liveness`: 200 if the Patroni heartbeat loop runs properly; 503 if the last run was more than `ttl` seconds ago on the primary or `2*ttl` on a replica. It is lightweight and runs no SQL. Probes should start failing about when the leader key is expiring.
- `GET /readiness?lag=<max-lag>&mode=apply|write`: 200 when the node is the leader, or when PostgreSQL is up, replicating and not too far behind. `lag` defaults to `maximum_lag_on_failover` and accepts bytes or human values such as 16kB, 64MB, 1GB. `mode` sets whether WAL must be replayed (`apply`, the default) or just received (`write`).

Used as a `readinessProbe`, freshly started pods become ready only once caught up. Combined with a PodDisruptionBudget this protects against terminating the leader too early during a rolling restart, and keeps replicas that cannot keep up from serving read-only traffic. Release 4.1.0 introduced the replication check on replicas.

Example for default `ttl` of 30s:

```
readinessProbe:
  httpGet: {scheme: HTTP, path: /readiness, port: 8008}
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  successThreshold: 1
  failureThreshold: 3
livenessProbe:
  httpGet: {scheme: HTTP, path: /liveness, port: 8008}
  initialDelaySeconds: 3
  periodSeconds: 10
  timeoutSeconds: 5
  failureThreshold: 3
```

## Checked

2026-11-03. Confirmed against the REST API page (`/liveness` and `/readiness` semantics, `lag` and `mode` parameters) and the release notes entry for 4.1.0.

Method: documentation only; no commands were run.
