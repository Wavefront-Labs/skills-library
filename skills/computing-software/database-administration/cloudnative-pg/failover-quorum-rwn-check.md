---
id: computing-software.database-administration.cloudnative-pg.failover-quorum-rwn-check
name: failover-quorum-rwn-check
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [failover-quorum, synchronous-replication, quorum, promotion, failoverquorum, data-loss]
level: advanced
status: docs-checked
description: "Enable synchronous.failoverQuorum so the operator promotes only a replica provably holding all synchronously committed data, using the R plus W greater than N check."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/failover.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Without synchronous replication, some loss at failover is expected. Even with `ANY 1 (...)` a commit can sit on the primary and one standby only; if both vanish in a partition, the survivor may lack data the application saw as committed. **Failover quorum** makes the operator promote only when it can confirm the instance to promote has all synchronous commits, otherwise it waits.

```yaml
  postgresql:
    synchronous:
      method: any
      number: 1
      failoverQuorum: true
```

The legacy annotation `alpha.cnpg.io/failoverQuorum` still works and **overrides** the spec (`"true"` with a synchronous stanza sets the field; `"false"` always disables). It is deprecated: migrate to the field and remove the annotation.

Check (Dynamo `R + W > N`): `R` promotable replicas (in the cluster, reporting state, potentially synchronous), `W` replicas that must acknowledge a commit, `N` total potentially synchronous replicas. If `R + W > N` a safe promotion exists.

- 3 instances, `number: 1`, required: primary alone fails, R=2, W=1, N=2, failover allowed; primary plus one replica fail, R=1, not allowed.
- 5 instances, `number: 2`: failover needs R=3 (N=4); R=2 is refused.
- `standbyNamesPre/Post` entries count in `N` but not `R`; the webhook rejects configurations where `number <= len(standbyNamesPre) + len(standbyNamesPost)`.

A `FailoverQuorum` resource with the cluster's name tracks the latest known synchronous configuration; do not edit it. During configuration changes it is reset, blocking failover until the new configuration applies. Force a promotion anyway with `kubectl cnpg promote`, as a last resort only. Commits made with `SET synchronous_commit TO local` carry no guarantee.

## Checked

2026-11-04. failoverQuorum field, legacy annotation precedence, R/W/N semantics, scenarios and FailoverQuorum resource confirmed on the Automated failover page.

Method: documentation only; no commands were run.
