---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-snapshot-s3
name: k3s-etcd-snapshot-s3
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, etcd-s3, s3-bucket, s3-snapshots]
level: advanced
status: docs-checked
description: "Replicate and restore etcd snapshots through an S3-compatible object store with the --etcd-s3 flags."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
S3 works for both on-demand and scheduled snapshots. Flags:

- --etcd-s3: enable S3 backup
- --etcd-s3-endpoint, --etcd-s3-endpoint-ca, --etcd-s3-skip-ssl-verify
- --etcd-s3-access-key, --etcd-s3-secret-key, --etcd-s3-session-token
- --etcd-s3-bucket, --etcd-s3-bucket-lookup-type (auto, dns or path; default auto)
- --etcd-s3-region (default us-east-1), --etcd-s3-folder
- --etcd-s3-retention (default 5), --etcd-s3-proxy, --etcd-s3-insecure
- --etcd-s3-timeout (default 5m0s)
- --etcd-s3-config-secret

--etcd-snapshot-retention sets --etcd-s3-retention if the latter is not set explicitly.

On-demand example with the CLI:

```
k3s etcd-snapshot --s3 --s3-bucket=test-bucket --s3-access-key=test --s3-secret-key=secret save
k3s etcd-snapshot --s3 --s3-bucket=test-bucket --s3-access-key=test --s3-secret-key=secret ls
k3s etcd-snapshot --s3 --s3-bucket=test-bucket --s3-access-key=test --s3-secret-key=secret delete <name>
```

`ls` shows an s3:// location and a file:// location for the same snapshot.

S3 retention is cluster-wide, not per node: each node prunes the bucket and prefix to at most N snapshots regardless of which node uploaded them, so replaced nodes do not leave orphans. With N etcd nodes, each cycle uploads about N objects, so to keep C cycles set retention to roughly N x C (3 nodes, 2 cycles: 6).

## Checked

2026-11-03: read docs.k3s.io cli/etcd-snapshot. Confirmed: the --etcd-s3-* flag list with defaults (region us-east-1, retention 5, timeout 5m0s, bucket-lookup-type), the retention-sets-S3-retention rule, and the cluster-wide S3 retention scope with the N x C sizing example.

Method: documentation only; no commands were run.
