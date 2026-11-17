---
id: computing-software.cloud-infrastructure-engineering.velero.backup-ttl-and-garbage-collection
name: backup-ttl-and-garbage-collection
category: computing-software
field: cloud-infrastructure-engineering
product: velero
tags: [ttl, garbage-collection, gc-failure, backup-expiry, garbage-collection-frequency]
level: practitioner
status: docs-checked
description: "Set backup retention with --ttl, understand what expiry removes, the hourly GC loop and the velero.io/gc-failure label reasons."
sources:
  - https://velero.io/docs/main/how-velero-works/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Set retention at creation with `velero backup create NAME --ttl 24h0m0s`. If you omit it, the default TTL is 30 days.

When Velero sees an expired backup it removes four things: the backup resource, the backup file in object storage, all PersistentVolume snapshots, and all associated Restores.

Expiry is not immediate. The gc-controller runs its reconciliation loop every hour by default. Change the frequency with `--garbage-collection-frequency <DURATION>`.

If deletion fails, Velero adds the label `velero.io/gc-failure=<Reason>` to the backup resource. Use the label to filter and select backups that failed to delete. Reasons:
- `BSLNotFound`: backup storage location not found
- `BSLCannotGet`: location cannot be retrieved from the API server for a reason other than not found
- `BSLReadOnly`: the location is read-only

`BSLReadOnly` means deleting an expired backup fails while its location is read-only, so a location left read-only after a restore will hold up expiry.

## Checked

2026-11-08. Read in full: the How Velero Works page. Every remaining claim was confirmed there. Removed or reworded: the kubectl label-selector command and the claim that the GC flag is set on a specific component.

Method: documentation only; no commands were run.
