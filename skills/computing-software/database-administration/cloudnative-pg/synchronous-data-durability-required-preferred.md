---
id: computing-software.database-administration.cloudnative-pg.synchronous-data-durability-required-preferred
name: synchronous-data-durability-required-preferred
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [synchronous-replication, datadurability, required, preferred, self-healing, rpo-zero]
level: advanced
status: docs-checked
description: "Choose dataDurability required (writes pause, RPO 0) or preferred (writes continue) and see how synchronous_standby_names shrinks."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`dataDurability` lives in `.spec.postgresql.synchronous`, defaults to `required`, and can be `preferred` only when `standbyNamesPre` and `standbyNamesPost` are unset.

**required.** A commit counts only after WAL reaches the configured number of synchronous standbys. Writes **pause** if that many are unavailable: zero data loss (RPO=0) at the cost of availability during standby failures or network disruption. Candidates are ordered healthy, then unhealthy, then the primary, truncated by `maxStandbyNamesFromCluster`. For a 3-instance cluster `foo` with `method: any`, `number: 1`: initially `ANY 1 ("foo-2","foo-3","foo-1")`; when foo-2 fails it moves back (`"foo-3","foo-2","foo-1"`); when foo-3 also fails there is no healthy standby and writes stop until one returns.

**preferred** ("self-healing mode"). The required number adjusts to available standbys and writes continue. Only healthy replicas are listed. For `bar`, 5 instances, `number: 2`:

```yaml
postgresql:
  synchronous:
    method: any
    number: 2
    dataDurability: preferred
```

`ANY 2 ("bar-2","bar-3","bar-4","bar-5")` shrinks to `ANY 2 ("bar-4","bar-5")`, then `ANY 1 ("bar-5")`, and finally empty, which disables synchronous replication entirely. Data can be lost if the primary then fails.

Define what ready means for a replica: by default it is ready once it has connected to the source at least once, but startup and readiness probes based on maximum lag can be configured (see the instance manager page). The failover quorum feature can be combined with synchronous replication for extra safety.

## Checked

2026-11-08. required versus preferred behaviour and the foo and bar worked examples confirmed on the Replication page.

Method: documentation only; no commands were run.
