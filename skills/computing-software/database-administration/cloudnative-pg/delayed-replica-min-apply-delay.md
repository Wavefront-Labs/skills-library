---
id: computing-software.database-administration.cloudnative-pg.delayed-replica-min-apply-delay
name: delayed-replica-min-apply-delay
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [delayed-replica, minapplydelay, recovery-min-apply-delay, human-error, replica-cluster, promotiontoken]
level: advanced
status: docs-checked
description: "Create a delayed replica with spec.replica.minApplyDelay as a buffer against accidental UPDATE or DELETE; no promotionToken."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replica_cluster.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A delayed replica intentionally lags the primary. `.spec.replica.minApplyDelay` maps to PostgreSQL `recovery_min_apply_delay`:

```yaml
  replica:
    enabled: true
    source: cluster-example
    # Enforce a delay of 8 hours
    minApplyDelay: '8h'
```

The aim is to limit the damage from unintended statements on the primary, such as an `UPDATE` or `DELETE` run without a `WHERE` clause. The delay gives you a window, here eight hours, to notice and correct the problem before it propagates to the replica. The documented use cases are:

1. Mitigating human error and the risk of corruption or loss from an unintentional SQL operation.
2. Faster recovery, because you can inspect the delayed replica and rectify issues before the change is applied there.
3. Extra data protection through a time buffer in which to intervene.

Restriction: `minApplyDelay` cannot be used together with `promotionToken`, so a delayed replica is not part of a token-driven distributed switchover.

Choose the delay from your recovery time objectives and the impact of a bad statement on the primary, and adjust it as needed. The page also advises measuring your goals: depending on the environment, recovery from a volume snapshot may be faster than relying on a delayed replica.

## Checked

2026-11-08. minApplyDelay example, use cases and the promotionToken incompatibility confirmed on the Replica clusters page, section Delayed replicas.

Method: documentation only; no commands were run.
