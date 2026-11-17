---
id: computing-software.database-administration.cloudnative-pg.safe-primary-election-lease
name: safe-primary-election-lease
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [primary-lease, lease, leaseduration, split-brain, primary-isolation, promotion, leader-election]
level: advanced
status: docs-checked
description: "Understand and tune the per-cluster Lease that guards promotion: what it prevents, how to inspect the holder with kubectl, the primaryLease fields and their webhook invariants."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failover.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CloudNativePG backs every promotion with a Kubernetes `Lease` named after the `Cluster` in its namespace. An instance must hold it before promoting; on a clean shutdown the old primary releases it so a replica can take over at once.

It protects against a replica catching up from the **archive** promoting while the old primary still has unarchived WAL: PostgreSQL reads "file not found" as end of stream, forks a timeline at an earlier LSN and loses acknowledged writes. On a clean shutdown the lease is released only after WAL is flushed and archived. After a crash the replica can promote once the lease is unchanged for `leaseDurationSeconds`, and writes not yet archived are lost.

Keep the primary isolation check enabled too: the lease prevents premature promotion, while isolation shuts down a primary that lost the API server. The lease alone cannot prevent split-brain.

```sh
kubectl get lease cluster-example
kubectl get lease cluster-example -o yaml
```

`HOLDER` shows the current primary pod.

Tuning under `.spec.primaryLease` (defaults): `leaseDurationSeconds` 15, `renewDeadlineSeconds` 10, `retryPeriodSeconds` 2, `releasedLeaseDurationSeconds` 1.

```yaml
spec:
  primaryLease:
    leaseDurationSeconds: 60
    renewDeadlineSeconds: 40
    retryPeriodSeconds: 15
```

The webhook requires `leaseDurationSeconds` > `renewDeadlineSeconds` > `retryPeriodSeconds` x 1.2. Longer values tolerate API server blips but slow legitimate promotions. After a clean switchover handover latency is bounded by `retryPeriodSeconds`. The primary captures the values when it first acquires the lease, so changes apply after that Pod restarts. RBAC for `leases` is required (see the 1.30 upgrade skill).

## Checked

2026-11-04. Lease rationale, inspection commands, default timings table and validation rules confirmed on the Automated failover page.

Method: documentation only; no commands were run.
