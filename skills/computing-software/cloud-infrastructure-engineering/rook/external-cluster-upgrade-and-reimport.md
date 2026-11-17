---
id: computing-software.cloud-infrastructure-engineering.rook.external-cluster-upgrade-and-reimport
name: external-cluster-upgrade-and-reimport
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [external-cluster-upgrade, upgrade-flag, external-cluster-user-command, restricted-caps, config-ini]
level: advanced
status: docs-checked
description: "Upgrade the Ceph user caps for an external cluster with the script upgrade flag and re-run the import using the stored external-cluster-user-command ConfigMap."
sources:
  - https://rook.io/docs/rook/latest-release/CRDs/Cluster/external-cluster/upgrade-external/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Ceph and Rook upgrade independently in external mode, and the provider connection must be refreshed with settings and permissions for new features.

Mandatory step: update the CSI user caps.
- Without restricted caps, upgrade all default CSI users with `python3 create-external-cluster-resources.py --upgrade`.
- With restricted caps (users made with `--restricted-auth-permission`), also pass `--rbd-data-pool-name` for RBD users, `--k8s-cluster-name` and `--run-as-user`, plus `--cephfs-filesystem-name` if it was used when creating CephFS users:
```
python3 create-external-cluster-resources.py --upgrade --rbd-data-pool-name replicapool \
  --k8s-cluster-name rookstorage --run-as-user client.csi-rbd-node-rookstorage-replicapool
```
User names follow csi-user-clusterName-poolName; key rotation adds a `.{x}` suffix.

Notes: an existing non-restricted user cannot be converted to restricted by upgrading, and `--upgrade` should only append permissions, never change which pools a user can access.

Optional step: to adopt a new feature, re-run the script with the same options as before plus the new ones. Since Rook v1.15 the script stores its arguments in the `external-cluster-user-command` ConfigMap:
```
kubectl get configmap -namespace rook-ceph external-cluster-user-command --output jsonpath='{.data.args}'
```
Copy that to `config.ini`, edit it, run the script with the config file, copy the bash output and repeat the import.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (upgrade-external) against this skill: 16 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
