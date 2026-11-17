---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-restore-multi-server
name: k3s-etcd-restore-multi-server
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, etcd-restore, multi-server, db-directory]
level: advanced
status: docs-checked
description: "Restore an etcd snapshot across a multi-server K3s cluster and rejoin the other servers, including restoring to new hosts."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Example with servers S1, S2, S3; the snapshot is on S1.

1. Stop K3s on all servers: `systemctl stop k3s`.
2. On S1:

```
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=<PATH-TO-SNAPSHOT>
```

3. On S1 start K3s: `systemctl start k3s`.
4. On S2 and S3 delete the old database directory, then start so they rejoin:

```
rm -rf /var/lib/rancher/k3s/server/db/
systemctl start k3s
```

Back up the directory before deleting it. For S3 snapshots pass the S3 flags and only the filename.

Restoring to new hosts: the snapshot can be restored on a different host, but you must supply the original server token because it decrypts the bootstrap data inside. Save /var/lib/rancher/k3s/server/token on the source, copy the snapshot to the new node, and run:

```
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=<PATH-TO-SNAPSHOT> \
  --token=<BACKED-UP-TOKEN-VALUE>
```

The token can also be in the config file; if a token is set there it must equal the backed-up value or K3s will fail to start.

Warning: node resources are in the snapshot, so on new nodes manually delete old nodes that no longer exist.

## Checked

2026-11-08: read the whole k3s etcd-snapshot page (raw markdown from the k3s-io/docs repo, which backs docs.k3s.io/cli/etcd-snapshot). Confirmed the multi-server restore steps, the backup-and-delete message, the S3 filename-only rule, and the new-host token procedure and warnings.

Method: documentation only; no commands were run.
