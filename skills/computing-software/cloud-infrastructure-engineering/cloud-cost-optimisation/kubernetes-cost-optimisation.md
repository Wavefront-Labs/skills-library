---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.kubernetes-cost-optimisation
name: kubernetes-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-aware-architecture, kubernetes-cost-optimisation, cluster-efficiency, bin-packing, idle-capacity, karpenter, cluster-autoscaler, spot-node-pools, requests-rightsizing, opencost]
level: practitioner
status: docs-checked
description: "Raise Kubernetes cluster cost efficiency: measure requested vs used vs allocatable, rightsize requests, consolidate nodes, spot pools, autoscaler tuning, idle cleanup."
sources: ["https://www.opencost.io/docs/", "https://karpenter.sh/docs/concepts/disruption/", "https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/", "https://www.finops.org/framework/capabilities/architecting-for-cloud/", "https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/FAQ.md", "https://kubernetes.io/docs/concepts/workloads/autoscaling/vertical-pod-autoscale/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kubernetes cluster cost efficiency

## Measure three layers
- **Allocatable** (node capacity you pay for) → **requested** (what pods reserve) → **used**.
- Idle = allocatable − requested (scheduler/packing waste). Slack = requested − used (overrequest waste).
- Track the ratios per cluster with a cost tool such as OpenCost, or from your own metrics, and note the trend.

## Actions in order of payoff
1. **Rightsize requests** from observed usage: run the VPA in recommendation mode or use a cost tool; the scheduler
   packs pods by requests (see the container-rightsizing skill).
2. **Consolidate nodes**: Karpenter `consolidationPolicy: WhenEmptyOrUnderutilized` (with `consolidateAfter`); or
   Cluster Autoscaler `--scale-down-utilization-threshold` (default 0.5, compared with the node's summed requests
   over allocatable) and its scale-down delay flags. Check PodDisruptionBudgets and `safe-to-evict`
   annotations are not blocking scale-down.
3. **Instance choice and spot**: for stateless, fault-tolerant workloads, use diversified node pools and PDBs.
4. **Scale workloads**: scale down non-prod clusters or namespaces outside working hours.
5. **Clean up** abandoned namespaces, volumes and LoadBalancer services.
6. **Fewer, larger clusters** where isolation allows: each cluster carries its own control plane and system add-ons.

## Verify
- [ ] Requested/allocatable and used/requested ratios tracked per cluster monthly.
- [ ] Top workloads by request have rightsized requests.

## Checked
2026-11-01. Confirmed in the Cluster Autoscaler FAQ (flag and 0.5 default, safe-to-evict), the Karpenter disruption
page (consolidationPolicy, consolidateAfter), the Kubernetes resource management and VPA pages, and OpenCost docs home.
Removed: the "typical untuned" utilisation figures, PromQL query, percentile targets, Goldilocks/KRR, ARM, KEDA,
Released-PV billing claim and per-cluster fee claim as stated figures.
Method: documentation only; no commands were run.
