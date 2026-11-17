---
id: computing-software.database-administration.cloudnative-pg.synchronous-replication-quorum-and-priority
name: synchronous-replication-quorum-and-priority
category: computing-software
field: database-administration
product: cloudnative-pg
tags: [synchronous-replication, quorum, priority, synchronous-standby-names, standbynamespre, maxstandbynamesfromcluster]
level: advanced
status: docs-checked
description: "Enable synchronous replication via spec.postgresql.synchronous (method any or first, number) and tune it with standbyNamesPre, standbyNamesPost and maxStandbyNamesFromCluster."
sources:
  - https://github.com/cloudnative-pg/cloudnative-pg/blob/main/docs/src/replication.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Direct `synchronous_standby_names` is forbidden. Instead, define `.spec.postgresql.synchronous` (disabled when absent). Two fields are mandatory: `method` (`any` = quorum, `first` = priority) and `number` (standbys a commit waits for). Plan synchronous replication for clusters of at least three instances.

```yaml
postgresql:
  synchronous:
    method: any
    number: 1
```

For `cluster-example` the operator writes `ANY 1 (cluster-example-2, cluster-example-3, cluster-example-1)`. Quorum (`any`) is the most common setup. Priority (`first`) picks standbys by list order and replaces a disconnected one with the next in line; it is most useful when extending beyond the cluster.

Extend or limit the list with optional fields: `maxStandbyNamesFromCluster` (cap on local pod names), `standbyNamesPre` and `standbyNamesPost` (`application_name` values prepended or appended). Examples from the page:

```yaml
postgresql:
  synchronous:
    method: first
    number: 2
    maxStandbyNamesFromCluster: 1
    standbyNamesPre:
      - angus
    standbyNamesPost:
      - malcolm
```

yields `FIRST 2 (angus, cluster-example-2, malcolm)`. With `method: any`, `number: 1`, `maxStandbyNamesFromCluster: 0` and `standbyNamesPre: [angus, malcolm]` the result is `ANY 1 (angus, malcolm)`.

Warning: you must ensure the names in `standbyNamesPre`/`Post` are correct and that you manage those standbys' availability; wrong entries can jeopardise uptime.

The deprecated `minSyncReplicas`/`maxSyncReplicas` (before 1.24) is mutually exclusive with this API; migrate by replacing them with `synchronous` plus `dataDurability: required`.

## Checked

2026-11-04. method/number requirements, generated synchronous_standby_names values and the three worked examples confirmed on the Replication page.

Method: documentation only; no commands were run.
