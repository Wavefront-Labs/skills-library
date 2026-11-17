---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cloud-node-autoscaling-variants-and-spot-interruptions
name: cloud-node-autoscaling-variants-and-spot-interruptions
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, node-autoscaling, asg-tags, spot-interruption, node-termination-handler, cluster-autoscaler, eks]
level: advanced
status: docs-checked
description: "Configure Cluster Autoscaler ASG auto-discovery on AWS and handle spot interruptions with Node Termination Handler or Karpenter's interruption queue."
sources: ["https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://github.com/aws/aws-node-termination-handler", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/concepts/disruption.md", "https://github.com/aws/karpenter-provider-aws/blob/main/website/content/en/v1.15/faq.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Node autoscaling on AWS with spot interruptions

This skill covers Cluster Autoscaler with ASG auto-discovery on AWS and how interruption notices
reach Kubernetes (Node Termination Handler or Karpenter). For other clouds follow that provider's
own autoscaler documentation; the specifics are not repeated here.

## Cluster Autoscaler with ASG auto-discovery
```
--node-group-auto-discovery=asg:tag=k8s.io/cluster-autoscaler/enabled,k8s.io/cluster-autoscaler/<cluster-name>
--balance-similar-node-groups --expander=priority,least-waste
```
- Auto-discovery finds ASGs that carry at least all the listed tags. Without the tags Cluster
  Autoscaler cannot add instances to the ASG. When no value is given in the flag, the tag values are
  ignored and only the tag names matter; you can also require values
  (`...enabled=foo,...<cluster-name>=bar`).
- Cluster Autoscaler respects each ASG's min and max and only adjusts the desired capacity. Each ASG
  should contain instance types with approximately equal capacity (same vCPU and memory).
- Scale from zero: with no running node to inspect, add ASG tags so Cluster Autoscaler can build a
  node template: `k8s.io/cluster-autoscaler/node-template/label/<label-name>`,
  `k8s.io/cluster-autoscaler/node-template/taint/<taint-name>` (value `<value>:<effect>`, for example
  `true:NoSchedule`) and `k8s.io/cluster-autoscaler/node-template/resources/<resource-name>` (for
  example `ephemeral-storage`).
- Several expanders can be chained (`priority,least-waste`, supported from Cluster Autoscaler 1.23);
  the output of one feeds the next and ties are broken randomly. `least-waste` is the default.
- Use separate node groups per zone so Cluster Autoscaler knows which group creates nodes in the zone
  a zonal volume needs; `--balance-similar-node-groups` then keeps zones balanced for workloads
  without topology requirements.
- `--skip-nodes-with-system-pods` defaults to `true`; set it to `false` only if you accept
  scale-down of nodes that run kube-system pods.
- Spot with ASGs: use a mixed instances policy with several similar-sized instance types so spot
  capacity comes from many pools. The Cluster Autoscaler AWS README recommends the
  capacity-optimized allocation strategy.

## Spot interruption handling
- **EC2 spot notice** is 2 minutes (Karpenter docs).
- **AWS Node Termination Handler (NTH)** runs in two modes. IMDS mode runs as a DaemonSet that watches
  instance metadata (spot interruption, scheduled events, rebalance recommendations, ASG target
  lifecycle state). Queue Processor mode runs as a Deployment and needs an SQS queue plus
  EventBridge rules; it also handles ASG lifecycle hooks. In IMDS mode a rebalance recommendation
  only cordons unless `enableRebalanceDraining` is true. Enabling `enableSqsTerminationDraining`
  turns on Queue Processor mode and disables IMDS mode.
- **Karpenter** handles interruption natively when an SQS queue is configured (setting
  `INTERRUPTION_QUEUE` / `--interruption-queue`; interruption handling is off if it is not set). It
  watches spot interruption warnings, scheduled change events, instance terminating and stopping
  events and instance status check failures, then taints, drains and terminates the node while it
  launches a replacement in parallel. Karpenter does not drain on spot rebalance recommendations.
  The Karpenter FAQ recommends against running NTH alongside Karpenter because both react to the same
  events; the Karpenter disruption page notes NTH is the option if you need rebalance handling, at the
  cost of more node churn.
- Workload side: keep `terminationGracePeriodSeconds` shorter than the notice window, set PDBs that
  allow eviction, spread replicas across zones and instance types, and avoid singletons or local
  state on spot capacity.

## Verify
- [ ] A simulated interruption using your cloud's own tooling drains the node and pods reschedule
      without errors.
- [ ] A pending pod that needs a scale-from-zero node group triggers a new node, and the node-template
      tags give the same labels, taints and resources as a real node.

## Checked

Checked 2026-10-27. Documentation checked: Cluster Autoscaler AWS README and FAQ (autoscaler master branch), aws-node-termination-handler README (main), Karpenter docs v1.15 (disruption, settings, FAQ). Confirmed: `--node-group-auto-discovery` tag semantics and the node-template label, taint and resources tags; expander chaining from 1.23 and `least-waste` as default; `skip-nodes-with-system-pods` default true; NTH IMDS (DaemonSet) vs Queue Processor (Deployment) modes; Karpenter interruption queue setting, event list and 2 minute spot notice; Karpenter FAQ advice on NTH. Removed as unconfirmed because the provider documentation is not in a readable repository: GKE node auto-provisioning commands and selectors, GCP and Azure spot notice durations, GKE graceful shutdown timing, AKS spot settings, the claim that EKS managed node groups tag ASGs automatically, the `owned` tag value convention and the AWS FIS action name.

Method: documentation only; no commands were run.
