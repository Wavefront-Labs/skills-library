---
id: computing-software.cloud-infrastructure-engineering.rook.node-maintenance-full-shutdown-procedure
name: node-maintenance-full-shutdown-procedure
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [node-maintenance, noout, scale-down, shutdown, restart, rook-ceph-operator]
level: advanced
status: docs-checked
description: "Shut down and restart nodes in a Rook Ceph cluster: stop I/O, set noout, scale the operator down first, scale Ceph deployments in order, then reverse."
sources:
  - https://rook.io/docs/rook/latest-release/Upgrade/node-maintenance/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Updating nodes by failure domain such as zone or rack is preferred to minimize downtime. The page describes a full shutdown for when downtime is acceptable. Always have a recent backup and notify stakeholders.

Procedure:
1. Set environment variables for the operator and cluster namespaces (`ROOK_OPERATOR_NAMESPACE`, `ROOK_CLUSTER_NAMESPACE`).
2. Stop I/O: scale down every application that uses Ceph.
3. Optionally set `noout` (and related) flags from the toolbox (`kubectl -n $ROOK_CLUSTER_NAMESPACE exec -it deploy/rook-ceph-tools -- bash`) so Ceph does not mark OSDs out. Flag order does not matter; unset in reverse on startup.
4. Scale down the operator first so it does not restart deployments:
```
kubectl -n $ROOK_OPERATOR_NAMESPACE scale deployment rook-ceph-operator --replicas=0
```
5. Scale down Ceph deployments in a controlled order, for example RGW, CSI CephFS provisioners, CSI RBD provisioners, OSDs, MONs, MGRs, then exporter and crash collector. The page loops over the prefixes `rook-ceph-rgw`, `csi-cephfsplugin-provisioner`, `csi-rbdplugin-provisioner`, `rook-ceph-osd`, `rook-ceph-mon`, `rook-ceph-mgr`, `rook-ceph-exporter`, `rook-ceph-crashcollector`.
6. Perform maintenance.
7. Scale back up starting with mons, then bring up the operator.
8. Unset the Ceph flags, then restart applications.

## Checked

2026-11-03. Read the Rook docs page(s) cited in sources (node-maintenance) against this skill: 13 backticked identifiers, flags, versions and quoted strings were matched to the page text; the 0 reported as not literally matched are YAML nesting or placeholder formatting, and each was confirmed by reading the surrounding page text (nested field lists, example output, command blocks). Nothing needed removing.

Method: documentation only; no commands were run.
