---
id: computing-software.cloud-infrastructure-engineering.talos-linux.etcd-snapshot-backup
name: etcd-snapshot-backup
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [etcd, snapshot, backup, talosctl-etcd-snapshot, machine-config, quorum]
level: practitioner
status: docs-checked
description: "Back up a Talos cluster: take a consistent etcd snapshot, copy the raw db file when quorum is lost, and save the machine config needed to rebuild failed control plane nodes."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/build-and-extend-talos/cluster-operations-and-maintenance/disaster-recovery.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
etcd holds Kubernetes control plane state, and Raft tolerates losing nodes only while more than half remain. A three-node control plane survives one failure; losing two at once loses service. Take routine backups, ideally on a schedule so the latest snapshot gives point-in-time recovery. A single control plane node cluster needs snapshots even more, since losing the node can make the cluster unrecoverable.

Consistent snapshot from any healthy control plane node (all etcd instances hold identical data):

```bash
$ talosctl -n <IP> etcd snapshot db.snapshot
etcd snapshot saved to "db.snapshot" (2015264 bytes)
snapshot info: hash c25fd181, revision 4193, total keys 1287, total size 3035136
```

The file name is arbitrary. If etcd is unhealthy (quorum lost) the command can fail; copy the database directly instead:

```bash
talosctl -n <IP> cp /var/lib/etcd/member/snap/db .
```

This copy may not be fully consistent while etcd runs, but it enables recovery when no regular snapshot exists.

Also back up the node machine configuration, which is needed to recreate a node after hardware failure with the same secret material and control plane settings:

```bash
talosctl -n IP get mc v1alpha1 -o yaml | yq eval '.spec' -
```

## Checked

2026-11-04. Snapshot, disaster copy and machine configuration backup commands and the quorum explanation confirmed on the Disaster Recovery page.

Method: documentation only; no commands were run.
