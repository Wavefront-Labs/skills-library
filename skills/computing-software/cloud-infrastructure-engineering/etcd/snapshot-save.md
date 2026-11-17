---
id: computing-software.cloud-infrastructure-engineering.etcd.snapshot-save
name: snapshot-save
category: computing-software
field: cloud-infrastructure-engineering
product: etcd
tags: [snapshot, snapshot-save, backup, etcdctl-snapshot, etcdutl, snapshot-status, disaster-recovery]
level: practitioner
status: docs-checked
description: "Back up etcd with etcdctl snapshot save and inspect it with etcdutl snapshot status."
sources:
  - "https://etcd.io/docs/v3.5/op-guide/recovery/"
  - "https://etcd.io/docs/v3.5/op-guide/maintenance/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A snapshot is a point-in-time copy of the keyspace in a single file. Snapshotting regularly gives a durable backup that lets the cluster be recovered to a known good state after operational error, data corruption or permanent member loss.

```bash
ETCDCTL_API=3 etcdctl --endpoints $ENDPOINT snapshot save snapshot.db
etcdutl snapshot status snapshot.db -w table
# HASH | REVISION | TOTAL KEYS | TOTAL SIZE
```

- A snapshot is taken either from a live member with `etcdctl snapshot save`, which snapshots the keyspace served by the endpoint you give, or by copying the `member/snap/db` file from a data directory.
- A copy of `member/snap/db` might lose data that has not been written yet but is in the WAL folder.
- A snapshot from `etcdctl snapshot save` carries an integrity hash that `etcdutl snapshot restore` checks. A copied db file has no hash and restores only with `--skip-hash-check`.
- `etcdutl snapshot status` shows hash, revision, total keys and total size, which tells you which revision a snapshot holds.
- The disaster recovery guide advises saving snapshots periodically.

Restoring creates new data directories and a new logical cluster; see the snapshot-restore skill.

## Checked

2026-11-08. Read the v3.5 disaster recovery guide and the maintenance guide in full. Confirmed: snapshot save command, copying member/snap/db with the possible WAL data loss, integrity hash and --skip-hash-check, etcdutl snapshot status columns. Removed: etcdctl snapshot status deprecation, non-leader advice, off-machine storage, encryption, TLS flags and root role claims, none stated on the pages.

Method: documentation only; no commands were run.
