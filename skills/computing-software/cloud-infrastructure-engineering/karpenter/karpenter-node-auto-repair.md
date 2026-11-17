---
id: computing-software.cloud-infrastructure-engineering.karpenter.karpenter-node-auto-repair
name: karpenter-node-auto-repair
category: computing-software
field: cloud-infrastructure-engineering
product: karpenter
tags: [node-repair, noderepair, feature-gate, node-monitoring-agent, unhealthy-nodes, toleration-duration, alpha]
level: advanced
status: docs-checked
description: "Node Auto Repair (alpha, v1.1.0): NodeRepair feature gate, monitored conditions with toleration durations, the 20 percent unhealthy safety threshold, forced termination."
sources: ["https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.13/concepts/disruption.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Karpenter Node Auto Repair

Alpha since v1.1.0. Enable with feature gate `NodeRepair=true` and run a Node Monitoring Agent (or Node Problem Detector) that sets node conditions. After a condition outlasts its toleration, Karpenter forcefully terminates the node and NodeClaim, bypassing the normal drain and grace period.

Kubelet conditions:

| Type | Status | Toleration |
|---|---|---|
| Ready | False | 30 minutes |
| Ready | Unknown | 30 minutes |

Node Monitoring Agent conditions (all Status False):

| Type | Toleration |
|---|---|
| AcceleratedHardwareReady | 10 minutes |
| StorageReady | 30 minutes |
| NetworkingReady | 30 minutes |
| KernelReady | 30 minutes |
| ContainerRuntimeReady | 30 minutes |

Safety: repair is not performed if more than 20% of nodes in a NodePool are unhealthy; for standalone NodeClaims the 20% is measured across all cluster nodes. This avoids cascading failures during a wider outage.

Repair is forceful, so `karpenter.sh/do-not-disrupt` pod annotations do not prevent it, and budgets do not rate-limit it. Repair policies come from the cloud provider.

## Checked

Method: 2026-11-08, read the cited page(s) in full from the v1.13 markdown source and compared each claim. All claims matched the page; nothing changed.
