---
id: computing-software.cloud-infrastructure-engineering.longhorn.disaster-recovery-volumes
name: disaster-recovery-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: longhorn
tags: [disaster-recovery, dr-volume, standby, activation, rpo]
level: advanced
status: docs-checked
description: "Create and activate Longhorn standby disaster recovery volumes from backups on a secondary cluster, with RPO and RTO, status colours and limits."
sources:
  - https://longhorn.io/docs/1.13.0/snapshots-and-backups/setup-disaster-recovery-volumes/
  - https://longhorn.io/docs/1.13.0/concepts/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: keep a standby volume on a second cluster.

Create:
- UI: on the secondary cluster's Backup page select a backup and choose Create Disaster Recovery Volume; using the original volume's name is recommended. It appears with Standby status.
- kubectl: copy the backup URL from the source cluster, create a `Volume` (`longhorn.io/v1beta2`, `longhorn-system`) with `fromBackup` and `Standby` set to true, and apply it on the secondary cluster. The flag is essential to create a standby volume.

Activate:
- Allowed when healthy, or degraded only if Allow Volume Creation with Degraded Availability is enabled; otherwise it sticks in `Attached`, and enabling the setting lets it finish `Detached`.
- UI: Volumes page, Operation dropdown, Activate Disaster Recovery Volume.
- kubectl: patch the volume `spec` to set `Standby` false and `frontend` `blockdev`.

Status icons: gray means restoring and not activatable; blue means fully synced and ready.

Until activated a DR volume cannot create, delete or revert snapshots, create backups, or create PVs or PVCs. After activation it cannot be deactivated.

Objectives (concepts page): RPO equals the recurring backup interval (hourly gives 1 hour). With hourly backups and 5 minutes per restore, a 30 minute poll gives about 5 minutes RTO and a 12 hour poll about 60 minutes.

## Checked

2026-11-04: read the source page(s) in full against every claim above: https://longhorn.io/docs/1.13.0/snapshots-and-backups/setup-disaster-recovery-volumes/, https://longhorn.io/docs/1.13.0/concepts/

No claim needed changing.

Method: documentation only; no commands were run.
