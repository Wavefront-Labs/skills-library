---
id: computing-software.database-administration.yugabytedb.disk-full-handling
name: disk-full-handling
category: computing-software
field: database-administration
product: yugabytedb
tags: [disk-full, low-disk-space, reject-writes-min-disk-space-mb, drive-fault, capacity, troubleshooting, pitr]
level: practitioner
status: docs-checked
description: "Handle YugabyteDB disk-full conditions: the write-rejection error and 3 GB threshold, quick space recovery options, crash loops, and automatic blacklisting."
sources: ["https://github.com/yugabyte/yugabyte-db/blob/master/docs/content/stable/troubleshoot/nodes/disk-full.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Disk full handling

When a data drive nears full, writes to tablets on it are rejected while reads continue. The error reads: Write to tablet <id> rejected. Node <id> has insufficient disk space. The tserver log first warns "Low disk space on ..." and later "Not enough disk space available on ...". The threshold is controlled by `reject_writes_min_disk_space_mb`, 3GB by default. Alert on low disk well before it.

Ways to recover space:
- Scale up (bigger disks or machines) or scale out (more nodes; the balancer moves tablets).
- Delete unneeded logs and old core dumps. Never touch data, bin, WAL, snapshot or config directories.
- Drop unused tables, databases or YCQL namespaces. With PITR enabled, dropped tables become HIDDEN and persist until their snapshot schedules expire. Ensure the master has disk space too, since YSQL drops update the catalog.
- Turn off features that consume space: TTL, PITR, xCluster, CDC.
- Run manual compaction on tables or tablets.

Failure modes:
- A full log drive can crash-loop a server at tablet bootstrap.
- If a disk has only a few KB left, bootstrap succeeds but a later write fatals with "No space left on device" and the server restarts repeatedly.
- At startup a completely full drive fails the test-file check, is marked faulty (`drive_fault` metric) and the master blacklists that tserver from creating tablets.

Other activity such as remote bootstrap can also consume disk and fill the drive even after one of the steps above. From 2.20.3.0 and 2024.1.0.0 the load balancer may move tablets off a tserver that the master blacklisted for a faulty drive; earlier releases can hit a fatal Tablet Manager init error at startup.

## Checked

2026-11-04. Confirmed against the Disk full troubleshooting page: write rejection with reads unaffected, the error and the Low disk space / Not enough disk space log messages, 3GB default of `reject_writes_min_disk_space_mb`, recovery options (scale up or out, remove logs and cores but never data, bin, WAL, snapshot or config directories, drop objects with HIDDEN state under PITR, disable TTL, PITR, xCluster and CDC, manual compaction), crash loops, and automatic blacklisting with the `drive_fault` metric. Removed the unsupported '20 percent headroom' advice.

Method: documentation only; no commands were run.
