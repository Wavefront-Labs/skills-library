---
id: computing-software.cloud-infrastructure-engineering.rook.rook-operator-upgrade-procedure
name: rook-operator-upgrade-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [rook-upgrade, operator-image, common-yaml, helm-upgrade-order, msgr2, requiremsgr2]
level: advanced
status: docs-checked
description: "Upgrade the Rook operator: patch release steps, Helm chart order, StorageClass deletion and the msgrv2 requirement noted for 1.21."
sources:
  - https://rook.io/docs/rook/latest-release/Upgrade/rook-upgrade/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Rook upgrade guide covers the management layer; the Ceph upgrade guide covers the data layer. Upgrades are automated except where permissions or customizations need manual action, and only official releases are supported, never builds from master. Storage may be briefly unavailable, so read the guide in full first. The cluster must be healthy and consuming pods steady.

Patch releases need only updated common resources and the operator image:
```
git clone --single-branch --depth=1 --branch v1.21.1 https://github.com/rook/rook.git
kubectl apply -f common.yaml -f crds.yaml -f csi-operator.yaml
kubectl -n rook-ceph set image deploy/rook-ceph-operator rook-ceph-operator=rook/ceph:v1.21.1
```
Update optional resources such as Prometheus monitoring too.

Notes for 1.21 on the page:
- Helm OCI chart tags no longer carry the `v` prefix.
- Ceph msgrv2 is required by default and needs kernel 5.11; with an older kernel set `network.connections.requireMsgr2: false` (under `cephClusterSpec` in the chart). Existing volume mounts keep msgrv1 until remounted, and mons require msgrv2 only once new mons deploy via failover.
- The minimum Kubernetes version is v1.32.

Helm: upgrade charts in this order: `rook-ceph`, `ceph-csi-drivers`, `rook-ceph-cluster`. The drivers chart must be installed or the CSI driver fails for missing service accounts, using the recommended values file. Before upgrading to v1.20, the cluster must be at least v1.19.5. The cluster chart adds CSI secret parameters to the block StorageClass, which is immutable, so run `kubectl delete storageclass ceph-block` first; existing PVs are unaffected.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (rook-upgrade) against this skill: 18 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
