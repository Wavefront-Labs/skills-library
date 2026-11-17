---
id: computing-software.cloud-infrastructure-engineering.garage.major-version-upgrade-procedure
name: major-version-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: garage
tags: [major-upgrade, garage-migrate, meta-snapshot-all, cluster-layout-backup]
level: advanced
status: docs-checked
description: "Plan a major Garage upgrade with full downtime or a simultaneous restart, with metadata backups."
sources:
  - https://garagehq.deuxfleurs.fr/documentation/operations/upgrading/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Major upgrades need the changelog and a staging test; per-upgrade guides live under Working Documents.

Full downtime route: disable API access (reverse proxy, or comment the API section and restart), check the cluster is idle and healthy, stop the whole cluster, back up every node's metadata folder (data blocks are immutable and unaffected), install the new binary and configuration, start everything, run any required `garage migrate`, check health, re-enable the API, and monitor.

Minimal downtime route: only the internal RPC protocol version must switch cluster-wide, so restart all nodes at the same moment in the new version. Downtime is the stop-and-start time, under a minute. Nodes on different protocol versions cannot talk to each other, so a node that misses the simultaneous restart is temporarily shut out.

Back up carefully: never copy the metadata folder of a running node. Since v0.9.4 `garage meta snapshot --all` snapshots every node at once. Automatic snapshots keep only the last two, so consider disabling automatic snapshotting in the upgraded config until success is confirmed. Also back up the `cluster_layout` file of one instance, which can be copied while running.

Specific migrations run either online afterwards or offline node by node.

## Checked

2026-11-04. Read the Upgrading Garage page in full. Confirmed both routes step by step, the under-a-minute downtime, the RPC protocol lockout, the backup warnings, garage meta snapshot --all since v0.9.4, the two-snapshot retention and the cluster_layout backup. Nothing removed.
Method: documentation only; no commands were run.
