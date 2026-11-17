---
id: computing-software.cloud-infrastructure-engineering.openebs.hostpath-xfs-quota-enable-and-modify
name: hostpath-xfs-quota-enable-and-modify
category: computing-software
field: cloud-infrastructure-engineering
product: openebs
tags: [local-pv, hostpath, xfs, quota, softlimitgrace, hardlimitgrace, xfs-quota, storageclass]
level: advanced
status: docs-checked
description: "Enable XFSQuota on a Local PV Hostpath StorageClass, compute soft and hard limits from limit-grace percentages, verify with xfs_quota, and change or remove a quota."
sources:
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/advanced-operations/xfs-quota/enable-xfs-quota
  - https://openebs.io/docs/user-guides/local-storage-user-guide/local-pv-hostpath/advanced-operations/xfs-quota/modify-xfs-quota
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Add an `XFSQuota` entry with `enabled: "true"` to the hostpath StorageClass's `cas.openebs.io/config`, with `BasePath` pointing at the XFS mount (the guide uses `/var/openebs/local/` in a class named `openebs-hostpath-xfs`). Optionally add `data` with `softLimitGrace` and `hardLimitGrace`.

The limit is **PV storage request x (1 + LimitGrace%)**. With no values, both default to `0%`, so capacity is capped at the request. A 100Gi PV with soft 90% and hard 100% gets a 190Gi soft limit and a 200Gi hard limit. You can use either grace value alone.

The PVC stays Pending until a pod mounts it; then it binds and the quota applies. Verify on the node with `xfs_quota -x -c 'report -h' /var/openebs/local/`, which lists a project ID with its used, soft and hard sizes.

**Limitation stated in the guide: resizing of quota is not supported.** To change limits of an existing volume, find the node and base path (from `kubectl describe pv` and the StorageClass), note the project ID from the report, and use `xfs_quota` with `limit` and `bsoft`/`bhard` values in B, KB, MB or GB (not KiB, MiB or GiB), then report again. To remove the quota, set the project limits to 0 and clear the project from the directory tree; the report then shows only the unlimited project #0.

Commands from the modify page, all run on the node that holds the volume (find it from the PV's node affinity): `sudo xfs_quota -x -c 'limit -p bsoft=3G bhard=5G 1' <base-path>` to change limits for project ID 1; `sudo xfs_quota -x -c 'limit -p bsoft=0 bhard=0 1' <base-path>` then `sudo xfs_quota 'project -C -p <base-path> 1' <base-path>` to remove the project. The ID `1` is the project ID noted from the report.

## Checked

Method: 2026-11-08, read both source pages (openebs/website docs markdown for enable-xfs-quota and modify-xfs-quota) in full. Claims match the pages; added the page's exact commands.
