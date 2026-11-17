---
id: computing-software.cloud-infrastructure-engineering.rook.rbd-node-loss-and-network-fencing
name: rbd-node-loss-and-network-fencing
category: computing-software
field: cloud-infrastructure-engineering
product: rook
tags: [network-fencing, out-of-service-taint, blocklist, csi-addons, node-loss, rbd]
level: sme
status: docs-checked
description: "Recover RBD volumes after node loss with network fencing: the out-of-service taints, 3-year blocklist entry, and the full power-cycle rule."
sources:
  - https://rook.io/docs/rook/latest-release/Storage-Configuration/Block-Storage-RBD/block-storage/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A volume mounted by a pod on a failed node cannot automatically mount elsewhere; the node must be guaranteed offline first. Network fencing stops the failed node from accessing the volume before it is remounted. It is not enabled by default. Setup examples live in the Network Fencing sections of the CSI configuration docs (Driver CR) and the Ceph-CSI drivers Helm chart docs.

When a node is confirmed down, taint it:
```
kubectl taint nodes <node-name> node.kubernetes.io/out-of-service=nodeshutdown:NoExecute
kubectl taint nodes <node-name> node.kubernetes.io/out-of-service=nodeshutdown:NoSchedule
```
With fencing configured, the CSI driver reads the stored client address from the RBD image metadata and, seeing the taint, adds that address to the Ceph blocklist. The blocklist entry lasts about 3 years so protection persists until the node fully power cycles.

Warning: mounts and device mappings on an out-of-service node persist until a complete power lifecycle (shutdown and startup). Never remove the out-of-service taint before that finishes, because stale device states, client sessions or mounts can cause serious data integrity problems.

Recovery: once the node is back and the taints are removed, workloads can be rescheduled onto it. If the 5-minute cool-down has passed, the CSI-Addons controller automatically removes the client address from the blocklist. Remove taints manually after the power cycle with `kubectl taint nodes <node-name> node.kubernetes.io/out-of-service=` plus the effect suffix.

## Checked

2026-11-03. Confirmed against the Block Storage page: the out-of-service taints, the roughly 3-year blocklist entry, the 5-minute cool-down before CSI-Addons unblocks, and the full power cycle warning. Removed: nothing.

Method: documentation only; no commands were run.
