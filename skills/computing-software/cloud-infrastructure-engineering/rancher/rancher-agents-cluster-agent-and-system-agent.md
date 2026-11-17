---
id: computing-software.cloud-infrastructure-engineering.rancher.rancher-agents-cluster-agent-and-system-agent
name: rancher-agents-cluster-agent-and-system-agent
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [cattle-cluster-agent, rancher-system-agent, agents, tolerations, resource-requests, downstream]
level: advanced
status: docs-checked
description: "cattle-cluster-agent and rancher-system-agent on downstream clusters, missing default CPU/memory requests, scheduling and tolerations."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/launch-kubernetes-with-rancher/about-rancher-agents
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two agent resources run on Rancher-managed clusters.

**cattle-cluster-agent** connects Rancher to the Kubernetes API of Rancher-launched clusters. It runs as a Deployment.

**rancher-system-agent** is a daemon that manages nodes in Rancher-provisioned RKE2 or K3s clusters during lifecycle operations such as upgrading Kubernetes or creating and restoring etcd snapshots. It applies "plans" to the node system and supports local and remote plans.

**Requests.** The `cattle-cluster-agent` pod defines no default CPU or memory requests. As a baseline the page recommends CPU `50m` and memory `100Mi`, adjusted to your use case. In the UI, create or edit the cluster, open **Cluster Configuration > Cluster Agent** and set **CPU Reservation** and **Memory Reservation**. In YAML:

```yaml
spec:
  clusterAgentDeploymentCustomization:
    overrideResourceRequirements:
      requests:
        cpu: 50m
        memory: 100Mi
```

**Scheduling.** The agent uses either a fixed set of tolerations or tolerations added dynamically from taints on control plane nodes, so taint-based evictions work properly. If control plane nodes exist, the default tolerations are replaced with ones matching their taints. It also has preferred scheduling rules (`preferredDuringSchedulingIgnoredDuringExecution`) favouring nodes with the control plane label (weight 100) and nodes labelled `cattle.io/cluster-agent=true` (weight 1). When no control plane nodes are visible, usually the case on hosted clusters, add the label `cattle.io/cluster-agent=true` to a node to prefer it.

The default node affinity excludes Windows nodes (`beta.kubernetes.io/os:NotIn:windows`). The UI request fields are documented for RKE2/K3s clusters.

## Checked

2026-11-09. Read the cited Rancher Agents page in full and checked every claim against it (agent roles, 50m/100Mi baseline, UI path, YAML snippet, tolerations, preferred scheduling table). Removed the claim that the preference targets etcd nodes; the page lists only control plane labels and the cluster-agent label.

Method: documentation only; no commands were run.
