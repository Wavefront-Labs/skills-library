---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-cost-allocation-and-cost-optimisation
name: gke-cost-allocation-and-cost-optimisation
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, gke-cost-allocation, gke-usage-metering, gke-cost-optimization, gke-cost, vpa, bin-packing, finops]
level: advanced
status: docs-checked
description: "Attribute GKE cost to namespaces and labels with cost allocation in the billing export, then cut it: right-size requests with VPA, autoscale, Spot."
sources: ["https://cloud.google.com/kubernetes-engine/docs/how-to/cost-allocations", "https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-usage-metering", "https://cloud.google.com/architecture/best-practices-for-running-cost-effective-kubernetes-applications-on-gke"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE cost allocation and optimisation

## 1. See cost per namespace / label
Enable cost allocation on an existing cluster (also available on `clusters create`):
```bash
gcloud container clusters update CLUSTER_NAME --enable-cost-allocation
```
(`--no-enable-cost-allocation` turns it off.) Prerequisite: export detailed usage cost data to BigQuery.
- Allocation data appears **only** in the Cloud Billing detailed usage cost export, not the standard export. It can take
  up to three days to appear after enabling.
- It is based on resource **requests**, not consumption.
- Labels on the billing rows include `goog-k8s-cluster-name` and `k8s-namespace`; join on `labels.key` in the detailed
  export to group cost by namespace for a cluster.
- Special namespaces: `kube:system-overhead` (node capacity not available to Pods: capacity minus allocatable),
  `kube:unallocated` (neither requested by workloads nor system overhead), `goog-k8s-unknown` (SKU not processed, for
  example during node startup and autoscaling) and `goog-k8s-unsupported-sku`.
- Limits: if a Pod has more than 50 Kubernetes labels none of its labels are available in billing; native sidecar
  containers (init containers with `restartPolicy: Always`) are reported in `kube:unallocated`; with CUD discount sharing
  some covered instances may land in `goog-k8s-unsupported-sku`; labels applied directly to PersistentVolumeClaims do
  not appear.
- Usage metering (separate feature) tracks requests and actual usage for CPU, GPU, TPU, memory, storage and optionally
  network egress, by namespace or label, to find workloads whose requests differ from consumption. Egress metering is
  not supported for Windows Server nodes, Shared VPC or VPC Network Peering, or clusters over 150 nodes.

## 2. Reduce it
Per Google's cost-effective GKE best practices:
1. **Right-size requests** with Vertical Pod Autoscaler. Start in `Off` (recommendation) mode, which applies no change;
   let it run at least 24 hours, ideally a week or more, before reading recommendations, then consider `Initial` or
   `Auto`. Take care when mixing HPA and VPA.
2. **Node auto-provisioning** creates node pools that fit scheduled workloads and reduces waste, at slightly higher
   autoscale latency when new pools are needed.
3. **Spot VMs** for workloads that tolerate node loss. Spot has no guaranteed availability and Pod Disruption Budgets
   might not be respected; keep a backup node pool without Spot VMs.

## Gotchas
- Pods without requests carry no allocation, so shared cost lands in the unallocated bucket; set requests.
- Standard and detailed billing exports are different tables; cost allocation needs the detailed one.

## Verify
- [ ] Monthly report: cost per namespace with `kube:unallocated` trending down.

## Checked
2026-11-09: confirmed against the GKE cost allocation page, usage metering page (limits and scope) and the cost-effective
GKE best-practices page (VPA Off mode, 24 hours/one week, node auto-provisioning, Spot caveats). Removed unread claims:
autoscaling-profile flag, Autopilot vs Standard guidance, CUD pairings, scale-to-zero, the `__unallocated__` name (the
page says `kube:unallocated`), `k8s-label` key forms, the SQL, the 70% ratio, and the dead view-cost-optimization source.
Method: documentation only; no commands were run.
