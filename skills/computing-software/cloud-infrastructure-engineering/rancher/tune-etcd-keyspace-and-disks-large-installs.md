---
id: computing-software.cloud-infrastructure-engineering.rancher.tune-etcd-keyspace-and-disks-large-installs
name: tune-etcd-keyspace-and-disks-large-installs
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [etcd, quota-backend-bytes, mvcc-database-space-exceeded, wal-dir, data-dir, rke2, k3s, performance]
level: advanced
status: docs-checked
description: "Tune etcd for a large Rancher install on RKE2 or K3s: raise quota-backend-bytes beyond 2 GB, spot the database space exceeded error, and use dedicated disks."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/advanced-user-guides/tune-etcd-for-large-installs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For large infrastructures the page recommends raising the etcd keyspace from the 2 GB default. The maximum is 8 GB, the host needs enough RAM to hold the whole dataset in memory, and the host should grow with the setting. It can also be raised on smaller installs expecting a high rate of pod change within the garbage collection interval.

Kubernetes cleans the etcd data set every five minutes. Deployment thrashing can write and delete enough events before that cleanup to fill the keyspace. If you see `mvcc: database space exceeded` in the etcd or kube-apiserver logs, increase it by setting `quota-backend-bytes` on the etcd servers. This snippet of RKE2/K3s `config.yaml` sets 5 GB:

```yaml
# RKE2/K3s config.yaml
---
etcd-arg:
  - "quota-backend-bytes=5368709120"
```

**Disk performance.** For RKE2 and K3s management clusters the page recommends mounting a dedicated high-performance flash device (SSD or NVMe), formatted with a filesystem such as XFS, at the database path: `/var/lib/rancher/rke2/server/db` for RKE2, `/var/lib/rancher/k3s/server/db` for K3s. Do not change the default etcd data directory with `etcd-arg` or other flags: RKE2 and K3s require the database at its default location, and moving it breaks snapshots and restores. Mount the device directly at the default path instead. The etcd documentation on disk priority also applies.

**Separate WAL.** Mirroring RAID is unnecessary because etcd replicates between nodes; striping RAID can raise available IOPS. If you use dedicated devices for data and WAL, mount the WAL disk at the default WAL path and declare `wal-dir` explicitly with that default path. Without it, etcd tries to manipulate the underlying WAL mount with insufficient permissions.

RKE2 `config.yaml`:

```yaml
etcd-arg:
  - "data-dir=/var/lib/rancher/rke2/server/db/etcd"
  - "wal-dir=/var/lib/rancher/rke2/server/db/etcd/wal"
```

K3s `config.yaml`:

```yaml
etcd-arg:
  - "data-dir=/var/lib/rancher/k3s/server/db/etcd"
  - "wal-dir=/var/lib/rancher/k3s/server/db/etcd/wal"
```

## Checked

2026-11-04. Checked against the Rancher Manager documentation pages: Tuning etcd for Large Installations. Fixed: the page now says to mount a dedicated device at the default RKE2/K3s database path and not to change the etcd data directory; the old /var/lib/etcd/data and /var/lib/etcd/wal paths were removed and replaced with the documented WAL examples.

Method: documentation only; no commands were run.
