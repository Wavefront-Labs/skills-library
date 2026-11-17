---
id: computing-software.ai-ml-engineering.ml-platform-engineering.karpenter-gpu-node-autoscaling
name: karpenter-gpu-node-autoscaling
category: computing-software
field: ai-ml-engineering
product: ml-platform-engineering
tags: [ml-platform-engineering, karpenter-gpu, cluster-autoscaler, gpu-nodes, kubernetes, eks, cost-optimization]
level: practitioner
status: draft
description: "Autoscale GPU nodes on Kubernetes with Karpenter: GPU NodePools, taints, spot vs on-demand, consolidation and disruption protection for training jobs."
sources:
  - https://karpenter.sh/docs/concepts/nodepools/
  - https://karpenter.sh/docs/concepts/disruption/
  - https://docs.aws.amazon.com/eks/latest/best-practices/aiml-compute.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# GPU node autoscaling with Karpenter

## GPU NodePool
```yaml
apiVersion: karpenter.sh/v1
kind: NodePool
metadata: {name: gpu}
spec:
  template:
    spec:
      nodeClassRef: {group: karpenter.k8s.aws, kind: EC2NodeClass, name: gpu}
      requirements:
        - {key: karpenter.k8s.aws/instance-family, operator: In, values: [g6e, p5, p4d]}
        - {key: karpenter.sh/capacity-type, operator: In, values: [on-demand, spot]}
      taints:
        - {key: nvidia.com/gpu, value: "true", effect: NoSchedule}
  limits: {nvidia.com/gpu: 64}             # cap total GPUs this pool can create
  disruption:
    consolidationPolicy: WhenEmpty         # don't evict running GPU jobs to repack
    consolidateAfter: 10m
    budgets: [{nodes: "10%"}]
```
EC2NodeClass uses a GPU-ready AMI (EKS optimized accelerated AMI / Bottlerocket NVIDIA) with enough root volume for large images.

## Workloads
- Pods request `nvidia.com/gpu: N` and tolerate the taint; non-GPU pods stay off expensive nodes.
- NVIDIA device plugin (or GPU Operator) must run on new nodes before pods schedule; account for that start-up time.
- Training pods: add `karpenter.sh/do-not-disrupt: "true"` annotation so consolidation and drift do not kill long jobs.
- Spot for fault-tolerant work (checkpointing training, batch inference); on-demand or reservations for latency-critical serving. Separate NodePools with weights express preference.

## Cold-start costs
GPU node provisioning plus multi-GB image pulls can take 5-15 minutes. Mitigations: pre-pulled images in AMIs/snapshots, image streaming (SOCI), a small warm pool, or low-priority placeholder pods.

## Cluster Autoscaler alternative
Node groups per GPU type with min/max sizes; simpler but less flexible instance selection. On GKE use node auto-provisioning or Autopilot GPU classes.

## Verify
- [ ] Submitting a GPU job provisions a node within the expected time; idle GPU nodes are removed after the consolidation window; a running job is never evicted by consolidation.
