---
id: computing-software.cloud-infrastructure-engineering.kubernetes.well-known-node-labels-for-scheduling
name: well-known-node-labels-for-scheduling
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, scheduling, topology-kubernetes-io, well-known-node-labels, node-affinity, nodeselector]
level: practitioner
status: docs-checked
description: "Use well-known node labels (topology zone/region, instance-type, os, arch, hostname) and custom labels for scheduling, and label nodes safely."
sources: ["https://kubernetes.io/docs/reference/labels-annotations-taints/", "https://kubernetes.io/docs/concepts/scheduling-eviction/assign-pod-node/#built-in-node-labels"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Well-known node labels

## Set by kubelet or cloud provider
| Label | Example | Use |
|---|---|---|
| `kubernetes.io/hostname` | `ip-10-0-1-5` | per-node anti-affinity, local PVs |
| `kubernetes.io/os` | `linux`, `windows` | OS targeting |
| `kubernetes.io/arch` | `amd64`, `arm64` | multi-arch |
| `topology.kubernetes.io/zone` | `eu-west-1a` | zone spread, zonal volumes |
| `topology.kubernetes.io/region` | `eu-west-1` | |
| `node.kubernetes.io/instance-type` | `m6i.xlarge` | hardware targeting |
| `node-role.kubernetes.io/control-plane` | `""` | control-plane selection |

Provider and autoscaler labels vary; Karpenter, for example, labels nodes `karpenter.sh/nodepool` and
`karpenter.sh/capacity-type`. Read your provider's documentation for its node-pool labels.

## Custom labels
```bash
kubectl label node w1 workload=batch disktype=nvme
kubectl label node w1 disktype-            # remove
kubectl get nodes -L topology.kubernetes.io/zone,node.kubernetes.io/instance-type,workload
```
For autoscaled or replaced nodes, set labels in the node group / NodePool template or
`--node-labels` at registration, never by hand, or new nodes will not have them.

## Use them
```yaml
nodeSelector:
  kubernetes.io/arch: arm64
topologySpreadConstraints:
- maxSkew: 1
  topologyKey: topology.kubernetes.io/zone
  whenUnsatisfiable: DoNotSchedule
  labelSelector: {matchLabels: {app: web}}
```

## Gotchas
- With the `NodeRestriction` admission plugin, kubelets cannot set labels under the
  `node-restriction.kubernetes.io/` or `node-role.kubernetes.io/` prefixes; they may set
  `kubernetes.io/hostname`, `kubernetes.io/arch`, `kubernetes.io/os` and a few other allowed labels.
  Set restricted ones from the API with admin rights.
- The deprecated beta labels (`failure-domain.beta.kubernetes.io/zone`, `beta.kubernetes.io/arch`)
  have GA replacements; migrate selectors to the GA names.
- Bare-metal clusters have no zone labels unless you add them; spread constraints on a missing
  key make pods unschedulable with DoNotSchedule.

## Checked
2026-10-23, against the Kubernetes website well-known labels, annotations and taints reference (hostname, os, arch, zone, region, instance-type, control-plane role label and taint, deprecated beta labels), the admission-controllers page (NodeRestriction label rules), and the Karpenter labels source (nodepool and capacity-type keys). EKS, GKE and AKS node-pool labels were removed as unconfirmed.
Method: documentation only; no commands were run.
