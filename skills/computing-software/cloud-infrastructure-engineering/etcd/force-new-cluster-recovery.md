---
id: computing-software.cloud-infrastructure-engineering.etcd.force-new-cluster-recovery
name: force-new-cluster-recovery
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [force-new-cluster, quorum-loss, disaster-recovery, majority-failure, single-member, recovery, data-dir]
level: advanced
status: docs-checked
description: "What --force-new-cluster does, why the docs discourage it, and the snapshot restore path for recovering after quorum loss."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/recovery/"
  - "https://etcd.io/docs/v3.5/op-guide/configuration/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A cluster of N members tolerates up to (N-1)/2 permanent failures. If it permanently loses more than that, it irrevocably loses quorum and cannot accept updates. The documented recovery is snapshot and restore.

Preferred path: restore from a snapshot.

- Take snapshots regularly with `etcdctl snapshot save snapshot.db`, or copy `member/snap/db` from a data directory (a copy may lose data that is only in the `wal` folder and has no integrity hash, so restore needs `--skip-hash-check`).
- `etcdutl snapshot status snapshot.db -w table` shows hash, revision, total keys and total size.
- `etcdutl snapshot restore snapshot.db --data-dir output-dir` creates new data directories. All members should restore from the same snapshot. Restore overwrites the member ID and cluster ID so a restored member cannot join an existing cluster; it starts a new logical cluster.
- To form the cluster on new members, pass membership at restore time: `--name`, `--initial-cluster`, `--initial-cluster-token` and `--initial-advertise-peer-urls`, run once per member, then start each `etcd` with its restored `--data-dir`.
- Clients may see the revision go backwards after a restore. `--bump-revision N` adds N to the snapshot revision, and `--mark-compacted` marks all revisions including the bump as compacted, which terminates watches. This is highly recommended for Kubernetes and other watch or cache consumers.

`--force-new-cluster` (default false, listed under Unsafe features: it may break the guarantees given by the consensus protocol) forces creation of a new one-member cluster. The recovery guide says that when starting etcd it overwrites cluster membership while keeping existing application data, and that this is strongly discouraged because it panics if other members from the previous cluster are still alive.

`--unsafe-no-fsync` disables fsync; it is unsafe and will cause data loss.

## Checked

2026-11-08. Read in full: etcd v3.5 Disaster recovery page and Configuration options page. Confirmed the failure tolerance formula, snapshot/restore commands and options, and the force-new-cluster and unsafe-no-fsync descriptions. Removed: the stop-all, member list/remove and learner re-adding procedure, the highest-raft-index selection advice and the two-members-with-the-flag caution (not on the pages read).
Method: documentation only; no commands were run.
