---
id: computing-software.cloud-infrastructure-engineering.longhorn.orphaned-data-cleanup
name: orphaned-data-cleanup
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [orphans, orphaned-data, replica-data, auto-deletion, cleanup]
level: practitioner
status: docs-checked
description: "Find and delete Longhorn orphaned replica directories with orphan CRs, enable orphan-resource-auto-deletion and know when no orphan is created."
sources:
  - https://longhorn.io/docs/1.13.0/advanced-resources/data-cleanup/orphaned-data-cleanup/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: reclaim disk used by replica directories Longhorn no longer tracks.

Longhorn detects them and creates `orphan` CRs. By default it does not delete orphans or their directories automatically.

```bash
kubectl -n longhorn-system get orphans -l "longhorn.io/orphan-type=replica"
kubectl -n longhorn-system get orphan <name> -o yaml
kubectl -n longhorn-system delete orphan <name>
```

Labels: `longhorn.io/orphan-type=replica`, `longhornnode=<node>`. Useful `spec.parameters` fields: `DataName`, `DiskName`, `DiskPath`, `DiskUUID`. Deleting the CR deletes the directory, immediately and ignoring the grace period.

Automatic deletion: add `replica-data` to the semicolon-separated `orphan-resource-auto-deletion` setting. Deletion then waits for `orphan-resource-auto-deletion-grace-period`.

UI: Setting, Orphan Resources, Replica Data, Operation, Delete.

No orphan CR is created when:
- the directory name does not match the replica naming convention
- `volume.meta` is missing
- the directory is on an evicted node or disk
- the replica is a stale (error) replica; those are cleaned according to `staleReplicaTimeout`

Check the label on the CR before bulk-deleting with a label selector: the page's bulk-delete example uses `orphan-type=replica-instance` while the rest of the page uses `replica`.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/advanced-resources/data-cleanup/orphaned-data-cleanup/

Added page conflict: the bulk-delete example uses orphan-type=replica-instance while the rest of the page uses replica.

Method: documentation only; no commands were run.
