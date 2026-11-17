---
id: computing-software.data-engineering.apache-hadoop.yarn-nodemanager-health-checks
name: yarn-nodemanager-health-checks
category: computing-software
field: data-engineering
product: apache-hadoop
tags: [data-engineering, apache-hadoop, yarn, nodemanager, health-checker, disk-checker, unhealthy-node]
level: practitioner
status: docs-checked
description: "YARN NodeManager health checks: the health-checker script keys and ERROR output rule, plus disk checker thresholds min-healthy-disks, utilisation and free space."
sources:
  - https://hadoop.apache.org/docs/stable/hadoop-yarn/hadoop-yarn-site/NodeManager.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NodeManager health checks

If any health check fails the NodeManager marks the node unhealthy and reports it to the ResourceManager in the heartbeat; the RM then stops assigning containers to it. The checker intervals do not change the heartbeat interval.

Script checker (yarn-site.xml; optional, if none is set only the disk checker decides):
- `yarn.nodemanager.health-checker.script`: comma-separated keywords for up to 4 scripts (default `script`)
- `yarn.nodemanager.health-checker.interval-ms`: default 10 minutes
- `yarn.nodemanager.health-checker.timeout-ms`: default 20 minutes
- Per keyword (`%s`): `yarn.nodemanager.health-checker.%s.path` (absolute, required), `.opts` (required), and optional `.interval-ms` / `.timeout-ms` overrides

The node is marked unhealthy if the script times out, throws, cannot run (bad path or permissions), or prints a line beginning with `ERROR`. A non-zero exit code alone is not a failure.

Disk checker:
- `yarn.nodemanager.disk-health-checker.enable`
- `...interval-ms`: default 2 minutes
- `...min-healthy-disks`: 0 to 1, default 0.25
- `...max-disk-utilization-per-disk-percentage`: 0 to 100, default 90
- `...min-free-space-per-disk-mb`: default 0

It checks `yarn.nodemanager.local-dirs` and `yarn.nodemanager.log-dirs` for permissions, free space and read-only state. A disk that fails is dropped from use while the node still reports healthy; the node is reported unhealthy only when the fraction of passing disks falls below `min-healthy-disks`.

Verify: make the script print `ERROR disk full`; the node shows as unhealthy in the RM UI.

## Checked
Confirmed 2026-11-08 against the Apache Hadoop YARN NodeManager page (Health Checker Service, Disk Checker, External Health Script; the fetched copy was labelled version 3.3.5): every key, default, allowed range and the ERROR / exit-code / timeout rules. Added the unhealthy-reporting behaviour from the same page. Removed the claim that the node shows unhealthy "within one interval" (the page ties the report to the heartbeat).
Method: docs-only read of cited pages, 2026-11-08
