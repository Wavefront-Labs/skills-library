---
id: computing-software.cloud-infrastructure-engineering.velero.restore-detailed-workflow
name: restore-detailed-workflow
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [restore-phases, partiallyfailed, fs-backup-timeout, restoreitemaction, restore-controller]
level: advanced
status: docs-checked
description: "Step through a Velero restore: accepted backup phases, preprocessing, per-resource steps, the 4h fs-backup timeout and CRD wait."
sources:
  - https://velero.io/docs/main/restore-reference/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
After `velero restore create`, the RestoreController runs these steps.

1. Validation: only backups in `Completed` or `PartiallyFailed` phase are accepted as restore sources.
2. Fetch: backup location info, the resource tarball, fs-backup volumes and volume snapshots.
3. Preprocess: it extracts the tarball to the /tmp folder, sorts resources for restore order, discovers them by Group Version Resource (undiscoverable resources are excluded), applies resource filters and verifies namespace mappings.
4. Per resource, one at a time: ensure the target namespace exists (create if not), rename and remap PVs, modify PVC metadata, run `RestoreItemAction` plugins, update the namespace if remapped, and add `velero.io/backup-name` and `velero.io/restore-name` labels.
5. Create the object. If it already exists it is skipped, except ServiceAccounts, unless `--existing-resource-policy` is set.
6. Wait steps: for a Pod it runs restore hooks and waits; for a PV restored by file system backup it starts the fs restore and keeps restoring other resources, but the restore will not finish until the fs restore completes or times out (default 4 hours, set with `--fs-backup-timeout`); for a CRD it waits for availability for 1 minute.

Failures in these steps are logged to the restore result and restoring continues.

The restore command group has `create`, `delete`, `describe`, `get` and `logs` subcommands.

## Checked

Checked 2026-11-08 against the Velero Restore Reference page ("Detailed Restore workflow", read in full). All workflow claims confirmed. Replaced the unsourced inspect advice with the documented subcommand list.

Method: documentation only; no commands were run.
