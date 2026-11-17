---
id: computing-software.cloud-infrastructure-engineering.kubernetes.immutable-node-replacement-vs-in-place-upgrade
name: immutable-node-replacement-vs-in-place-upgrade
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, immutable-node-replacement, node-upgrade, cluster-upgrade, cluster-api, karpenter-drift]
level: practitioner
status: docs-checked
description: "Decide between upgrading nodes in place and replacing them with new images, and run a surge-based node replacement that respects PDBs."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/upgrading-linux-nodes/", "https://cluster-api.sigs.k8s.io/user/guide/lifecycle/upgrades", "https://kubernetes.io/docs/tasks/administer-cluster/safely-drain-node/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# In-place vs immutable node replacement

| | In-place | Replace |
|---|---|---|
| How | drain, `apt install kubelet=...`, `kubeadm upgrade node`, restart | build a new image, add new nodes, drain and delete old |
| Drift | config drift accumulates | every node matches the image |
| Rollback | downgrade packages (risky) | point the group back at the old image |
| Needs | nothing extra | image pipeline, surge capacity, automation |
| Stateful local disks | data stays | data lost; needs replication or migration |

Use replacement wherever node groups are automated (cloud node groups, Cluster API,
Karpenter). Keep in-place for bare metal with local data or no spare capacity.

## Replacement procedure (generic)
1. Build and test the new image (kubelet version, kernel, containerd).
2. Add surge nodes with the new image; confirm `Ready` and DaemonSets running.
3. Cordon all old nodes so evicted pods land only on new ones:
   `kubectl cordon -l nodegroup=old`
4. Drain one at a time: `kubectl drain <node> --ignore-daemonsets --delete-emptydir-data --timeout=10m`
5. Delete the node object and the machine.

Automated forms: Cluster API triggers a rollout of the machines controlled by a MachineDeployment
once you change its Kubernetes version or template references (see its upgrade guide). Node
autoscalers and managed node groups have their own provider-specific replacement mechanisms;
check their documentation for drift and surge behaviour.

## Gotchas
- PDBs with `maxUnavailable: 0` block drains forever; find them first.
- Local PVs pin pods to old nodes; plan data migration before replacing.
- Surge needs quota and IPs (subnet sizing with VPC CNIs).

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: kubeadm upgrading-linux-nodes and kubeadm-upgrade pages (in-place sequence: drain, upgrade packages, kubeadm upgrade node, restart kubelet, uncordon), kubectl drain source flags (--ignore-daemonsets, --delete-emptydir-data, --timeout) and the Cluster API upgrade guide (a MachineDeployment change triggers a rollout of its machines). Removed the unverified Karpenter drift and managed node group claims.

Method: documentation only; no commands were run.
