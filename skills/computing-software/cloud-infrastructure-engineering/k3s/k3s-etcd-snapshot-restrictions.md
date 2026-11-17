---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-snapshot-restrictions
name: k3s-etcd-snapshot-restrictions
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, etcd-snapshot-restrictions, snapshot-dir, s3-endpoint]
level: sme
status: docs-checked
description: "Stop the etcd-snapshot CLI overriding server-side snapshot paths and S3 targets with etcd-snapshot-restrictions."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Version gate: available as of the October 2026 releases v1.37.2+k3s1, v1.36.6+k3s1, v1.35.10+k3s1 and v1.34.13+k3s1.

By default there are no restrictions. With the k3s etcd-snapshot CLI, snapshots can be saved to or deleted from any host path or any valid S3 endpoint, because the CLI inherits server config defaults but flags can override them. Neither the CLI nor the server-side snapshot management API validates target paths or checks that files targeted for deletion are really etcd snapshots.

Set `etcd-snapshot-restrictions` on the server to disable CLI overrides of server-side settings. Values:

- all: every effect below
- snapshot-dir: cannot override etcd-snapshot-dir, so save/delete of local snapshots stays inside the server's configured path
- s3-endpoint: cannot override etcd-s3-endpoint
- s3-bucket: cannot override etcd-s3-bucket
- s3-folder: cannot override etcd-s3-folder (prefix in the bucket)
- s3-proxy: cannot override etcd-s3-proxy, so the server's HTTP proxy is used

Example config:

```
etcd-snapshot-restrictions: all
```

This covers both on-demand saves and deletion of existing snapshots.

## Checked

2026-11-03: read docs.k3s.io cli/etcd-snapshot. Confirmed: the October 2026 release gate and the etcd-snapshot-restrictions values (all, snapshot-dir, s3-endpoint, s3-bucket, s3-folder, s3-proxy).

Method: documentation only; no commands were run.
