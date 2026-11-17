---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-advanced-options
name: external-cluster-advanced-options
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [external-object-store, object-external-yaml, client-admin, rook-ceph-mon-secret, exporting-rook]
level: advanced
status: docs-checked
description: "Advanced external-mode options: exporting a Rook cluster to other clusters, admin keyring use, and connecting to an external object store."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/advance-external/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Exporting Rook to another cluster: to use a local rook-ceph cluster as central storage for several Kubernetes clusters, copy the export script into the toolbox and run it there:
```
toolbox=$(kubectl get pod -l app=rook-ceph-tools -n rook-ceph -o jsonpath='{.items[*].metadata.name}')
kubectl -n rook-ceph cp deploy/examples/external/create-external-cluster-resources.py $toolbox:/etc/ceph
```
Exec into the toolbox and run it with the needed options. Other clusters can only connect if Rook uses a network configuration reachable from them, most commonly host networking in the CephCluster CR so daemons are addressable by host IPs.

Admin privileges: sharing the admin key is generally not recommended. If needed, take it from `ceph auth get client.admin` and set two values in the `rook-ceph-mon` secret: `ceph-username` to `client.admin` and `ceph-secret` to the keyring. After restarting the Rook operator (and the toolbox if used), Rook configures Ceph with admin privileges.

External object store: from `deploy/examples/external` run `kubectl create -f object-external.yaml` to connect to existing gateways. Consume S3 either by creating an object store user (`object-user.yaml`) or by creating a bucket storage class and an Object Bucket Claim (`storageclass-bucket-delete.yaml`, `object-bucket-claim-delete.yaml`).

For NFS on an external standalone cluster, Rook suggests a different mechanism than the one used for internal clusters.

## Checked

2026-11-03. Confirmed against the Advanced external cluster page: the export script copy into the toolbox, host networking advice, the client.admin keyring in the rook-ceph-mon secret, object-external.yaml and the object user / OBC options. Removed: nothing.

Method: documentation only; no commands were run.
