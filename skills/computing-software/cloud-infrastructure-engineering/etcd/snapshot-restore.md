---
id: computing-software.cloud-infrastructure-engineering.etcd.snapshot-restore
name: snapshot-restore
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [snapshot-restore, restore, etcdutl, initial-cluster, data-dir, bump-revision, mark-compacted, skip-hash-check, disaster-recovery]
level: advanced
status: docs-checked
description: "Restore a cluster from a snapshot with etcdutl snapshot restore, including per-member data dirs, bump-revision and mark-compacted."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/recovery/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Restoring creates new data directories from a snapshot file. Do it on every member, then start them as a new cluster.

```bash
etcdutl snapshot restore snapshot.db   --name m1   --initial-cluster m1=http://host1:2380,m2=http://host2:2380,m3=http://host3:2380   --initial-cluster-token etcd-cluster-1   --initial-advertise-peer-urls http://host1:2380   --data-dir /path/to/m1.etcd
```

Repeat for m2 and m3 with their own name, peer URL and data dir, then start each etcd with `--name`, `--data-dir` pointing at the restored directory, and its client and peer listen and advertise URLs.

Facts:

- Restore overwrites snapshot metadata (member ID and cluster ID), so the restored members lose their former identity; this prevents a new member from inadvertently joining an existing cluster, so the restore starts a new logical cluster. All members should restore from the same snapshot. Supplying `--initial-cluster` and `--initial-cluster-token` makes the new cluster connect only to the other restored members.
- A snapshot taken with `etcdctl snapshot save` carries an integrity hash that restore checks; a snapshot copied from `member/snap/db` has no hash and restores only with `--skip-hash-check` (and a copy may lose data still in the WAL).
- Clients may see the revision go back after a restore, which is a particular problem for Kubernetes informers and watch-based caches. `--bump-revision N` adds N revisions to the snapshot's revision (the page suggests 1,000,000,000 for a week-old snapshot at under 1500 writes per second), and `--mark-compacted` marks all revisions including the bump as compacted so watches terminate.
- `etcd --force-new-cluster` can overwrite membership while keeping data, but the page strongly discourages it because it panics if other members of the previous cluster are still alive.

Use `etcdutl snapshot status snapshot.db -w table` to see hash, revision, total keys and size.

## Checked

2026-11-03. Confirmed on the v3.5 disaster recovery guide: etcdutl snapshot restore command and flags, per-member restore example, identity overwrite and new logical cluster, integrity hash and --skip-hash-check, revision difference and Kubernetes warning, --bump-revision and --mark-compacted semantics and example, --force-new-cluster warning, etcdutl snapshot status. Removed: the etcdctl snapshot restore deprecation, the stop-old-members instruction and the endpoint health verification, which the page does not state.

Method: documentation only; no commands were run.
