---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-restore-single-server
name: k3s-etcd-restore-single-server
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, cluster-reset, cluster-reset-restore-path, etcd-restore]
level: advanced
status: docs-checked
description: "Restore an embedded etcd snapshot on a single K3s server with --cluster-reset and --cluster-reset-restore-path."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Steps:

1. Stop K3s: `systemctl stop k3s`.
2. Reset and restore:

```
k3s server \
  --cluster-reset \
  --cluster-reset-restore-path=<PATH-TO-SNAPSHOT>
```

3. When it prints `Managed etcd cluster membership has been reset, restart without --cluster-reset flag now.` start K3s: `systemctl start k3s`.

Using --cluster-reset without a snapshot path only resets etcd to a single member.

What the restore does: downloads the snapshot from S3 if needed, decompresses it, moves current etcd files to ${data-dir}/server/db/etcd-old-$TIMESTAMP/, extracts the snapshot and verifies the checksum, starts etcd and removes all other members, and extracts CA certificates and other confidential data to disk.

S3: pass the S3 flags (--etcd-s3, --etcd-s3-bucket and so on) on the CLI and give only the snapshot filename as the restore path. If an etcd-s3 backup config is in the config file, restores pull from S3 by default (pass only the filename); to restore a local file, add `--etcd-s3=false` and the full local path.

Safety: K3s creates an empty file /var/lib/rancher/k3s/server/db/reset-flag to stop repeated cluster resets; it is deleted on a normal start.

Versions: restoring does not require the exact K3s version, a higher patch or minor is fine within version skew. Do not restore a snapshot from an older version you could not upgrade directly from.

## Checked

2026-11-03: read docs.k3s.io cli/etcd-snapshot. Confirmed: the --cluster-reset and --cluster-reset-restore-path procedure, the restore step list, S3 restore behaviour and the reset-flag safety file.

Method: documentation only; no commands were run.
