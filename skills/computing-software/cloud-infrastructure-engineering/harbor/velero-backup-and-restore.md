---
id: computing-software.cloud-infrastructure-engineering.harbor.velero-backup-and-restore
name: velero-backup-and-restore
category: computing-software
field: cloud-infrastructure-engineering
product: harbor
tags: [velero, backup, restore, readonly, harbor-backup]
level: advanced
status: docs-checked
description: "Back up and restore a Helm-deployed Harbor with Velero: set read-only, exclude Redis, choose snapshot or file system backup, and know the limits."
sources:
  - https://goharbor.io/docs/main/administration/backup-restore/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The documented procedure applies to Harbor deployed on Kubernetes with the Helm chart. It backs up Kubernetes resources and PersistentVolume data for the internal database, registry, jobservice and Trivy. Redis is not backed up and the backup is crash consistent, not application consistent.

Steps:
1. Install the Velero CLI and server.
2. In the portal, Administration, Configuration, System Settings, tick **Repository Read Only** and save.
3. Exclude Redis by labelling its pod, PVC and PV:
`kubectl -n harbor label pod/harbor-redis-0 velero.io/exclude-from-backup=true` (same label on `pvc/data-harbor-redis-0` and the PV).
4. Back up with one of:
`velero backup create harbor-backup --include-namespaces harbor --snapshot-volumes --wait` (CSI or native snapshot), add `--snapshot-move-data` for CSI snapshot with data move, or use `--default-volumes-to-fs-backup` for file system backup.
5. Untick Repository Read Only.
6. Restore: `velero restore create harbor-restore --from-backup harbor-backup --wait`. The restored instance is still read-only, so untick the box again.

Limitations: the registry pod runs upload purging (default interval 168h) that can fail file system backups, so back up between purge rounds. In-memory pull times not yet synced to the database are lost. Replication, GC or scan tasks may hang in progress after restore and can be stopped in the portal. Logged-in sessions are lost. External databases are not supported.

## Checked

- 2026-11-03: concrete claims (parameter names, defaults, steps, limits, UI labels) read against the official Harbor docs: Backup And Restore Harbor With Velero (docs source on GitHub).
Method: documentation only; no commands were run.
