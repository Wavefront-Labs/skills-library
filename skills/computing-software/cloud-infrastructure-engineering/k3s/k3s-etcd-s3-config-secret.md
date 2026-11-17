---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-etcd-s3-config-secret
name: k3s-etcd-s3-config-secret
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, etcd-s3-config-secret, s3-config-secret, credential-rotation]
level: advanced
status: docs-checked
description: "Keep etcd S3 snapshot settings in a Kubernetes Secret instead of flags so credentials rotate without a restart."
sources:
  - https://docs.k3s.io/cli/etcd-snapshot
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: avoid hardcoding S3 credentials in flags or config.

Start K3s with only these two flags:

```
--etcd-s3 --etcd-s3-config-secret=<SECRET-NAME>
```

If any other S3 flag is set, the Secret is ignored. The Secret need not exist at startup; K3s checks it on every snapshot save, list, delete or prune. Because the Secret is read at operation time, credentials can be rotated without restarting K3s.

Limit: the Secret cannot be used when restoring a snapshot, since the apiserver is not available to provide it. S3 settings must then be passed on the CLI when restoring a snapshot stored on S3.

Secret format (kube-system namespace, type etcd.k3s.cattle.io/s3-config-secret):

```
apiVersion: v1
kind: Secret
metadata:
  name: k3s-etcd-snapshot-s3-config
  namespace: kube-system
type: etcd.k3s.cattle.io/s3-config-secret
stringData:
  etcd-s3-endpoint: ""
  etcd-s3-access-key: "AWS_ACCESS_KEY_ID"
  etcd-s3-secret-key: "AWS_SECRET_ACCESS_KEY"
  etcd-s3-bucket: "bucket"
  etcd-s3-folder: "folder"
  etcd-s3-region: "us-east-1"
  etcd-s3-insecure: "false"
  etcd-s3-timeout: "5m"
```

Keys match the --etcd-s3-* flags. The etcd-s3-endpoint-ca key takes a PEM bundle, or etcd-s3-endpoint-ca-name names a ConfigMap in kube-system holding PEM bundles.

## Checked

2026-11-03: read docs.k3s.io cli/etcd-snapshot. Confirmed: the two-flag startup rule, the ignored-if-other-S3-flags rule, read-at-operation time, the restore limitation and the Secret type and keys.

Method: documentation only; no commands were run.
