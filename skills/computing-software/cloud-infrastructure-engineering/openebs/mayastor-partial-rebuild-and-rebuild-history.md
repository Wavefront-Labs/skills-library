---
id: computing-software.cloud-infrastructure-engineering.openebs.mayastor-partial-rebuild-and-rebuild-history
name: mayastor-partial-rebuild-and-rebuild-history
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [replicated-pv-mayastor, rebuild, partial-rebuild, write-log, faulted-child-wait-period, rebuild-history]
level: advanced
status: docs-checked
description: "Understand Mayastor partial rebuilds: write logging for a faulted child, the 10 minute faulted-child-wait-period before a full rebuild, and viewing per-volume rebuild history."
sources:
  - https://openebs.io/docs/user-guides/replicated-storage-user-guide/replicated-pv-mayastor/advanced-operations/replica-rebuilds
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Earlier versions triggered a **full rebuild** whenever a volume target had a Degraded volume, even if the replica had only been unreachable briefly, for instance during a node restart. That is harmless for small replicas but costly for large ones.

The **partial rebuild** feature fixes this. When the volume target hits an I/O error on a child, it marks the child `Faulted`, removes it from the I/O path and starts a **write log** of all later writes. The core agent then waits for the replica to come back. If it returns in time, only the logged changes need to be applied, which makes the rebuild much faster.

The wait is controlled by `--faulted-child-wait-period`, which **defaults to 10 minutes**. Until it expires the control plane does not start a full rebuild; after that it falls back to removing the replica and creating and fully rebuilding a new one. Change the value by editing `values.yaml`.

**History.** The data plane handles both full and partial rebuilds. To see what rebuilds an existing volume target has undergone, run `kubectl mayastor get rebuild-history <volume-id>`, optionally with `-ojson` for JSON instead of a table. The history is kept as long as the volume target stays intact without disruptions from node failures or recreation.

## Checked

2026-11-04. Confirmed against the Replica Rebuilds page: full versus partial rebuild, the write log, the 10 minute `--faulted-child-wait-period` set in `values.yaml`, the `get rebuild-history` command and how long history is kept. Removed the upgrade note about `mayastor.agents.core.rebuild.partial.enabled`, which is not on this page.

Method: documentation only; no commands were run.
