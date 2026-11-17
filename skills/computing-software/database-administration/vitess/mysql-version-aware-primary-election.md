---
id: computing-software.database-administration.vitess.mysql-version-aware-primary-election
name: mysql-version-aware-primary-election
category: computing-software
field: database-administration
product: vitess
tags: [reparenting, primary-election, mysql-upgrade, rolling-upgrade, allow-cross-cell-promotion, wait-replicas-timeout]
level: sme
status: docs-checked
description: "Predict which tablet PRS or ERS elects during a rolling MySQL upgrade: version-first versus position-first ordering, family and file-position limits, and the related flags."
sources:
  - https://vitess.io/docs/25.0/user-guides/configuration-advanced/reparenting/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Both reparent commands prefer a candidate with a lower MySQL version, because MySQL only guarantees replication from an older source to a newer replica. Version is an additional factor layered on durability policy and GTID position.

Orderings:
- Version-first: promotion rules, then MySQL version (lower preferred), then GTID position, then InnoDB buffer pool size, then tablet alias.
- Position-first: GTID position, then promotion rules, then version, then buffer pool size, then alias.

`EmergencyReparentShard` always uses position-first. `PlannedReparentShard` uses version-first when a healthy current primary exists (the elect catches up first) or when the shard has never had a primary; it uses position-first when there is no healthy primary but there once was, and may then elect a higher-version tablet and log a warning.

Limits:
- Version is compared by MAJOR.MINOR, except when the lower version is an 8.0 release earlier than 8.0.34, where the patch is compared too.
- MySQL and Percona Server are one family; MariaDB is separate. Across families the feature is disabled. ERS also needs MySQL GTID replication.
- On file-position shards, PRS that must self-elect fails: pass `--new-primary`. A shard mixing GTID and file-position tablets is rejected with no override.
- Tablets reporting no version sort last.

Rolling-upgrade advice: PRS may pick a lower-version, slightly-behind tablet and catch it up, so keep `--wait-replicas-timeout` (default 15s) generous. The cell boundary filters before version: PRS needs `--allow-cross-cell-promotion` to prefer a lower-version tablet in another cell, while ERS allows cross-cell unless `--prevent-cross-cell-promotion` is set. Upgrade RDONLY tablets before REPLICA tablets (operational guidance, not enforced).

## Checked

2026-11-04. Orderings, limitations and upgrade notes confirmed in the MySQL version-aware primary election section of the Reparenting (advanced) page.

Method: documentation only; no commands were run.
