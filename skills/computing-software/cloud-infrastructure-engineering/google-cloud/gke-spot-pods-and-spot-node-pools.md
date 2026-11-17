---
id: computing-software.cloud-infrastructure-engineering.google-cloud.gke-spot-pods-and-spot-node-pools
name: gke-spot-pods-and-spot-node-pools
category: computing-software
field: cloud-infrastructure-engineering
product: google-cloud
tags: [google-cloud, gcp, gke, spot-vms, spot-pods, spot-node-pool, node-taints, autopilot, cost-optimisation]
level: practitioner
status: docs-checked
description: "Run fault-tolerant GKE workloads on Spot: Standard Spot node pools with taints, Autopilot Spot Pods via nodeSelector, graceful termination limits and on-demand fallback."
sources: ["https://docs.cloud.google.com/kubernetes-engine/docs/concepts/spot-vms", "https://docs.cloud.google.com/kubernetes-engine/docs/how-to/spot-vms"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# GKE Spot Pods and Spot node pools

## 1. Standard: Spot node pool
```bash
gcloud container node-pools create spot-pool --cluster=<C> --region=<R> \
  --spot --machine-type=n2-standard-8 \
  --node-taints=cloud.google.com/gke-spot="true":NoSchedule
```
GKE labels Spot nodes `cloud.google.com/gke-spot=true`. Node auto-provisioning adds the `cloud.google.com/gke-spot=true:NoSchedule` taint to Spot pools it creates; for your own pools add a taint yourself so critical workloads stay off Spot VMs.

## 2. Workload spec
```yaml
spec:
  terminationGracePeriodSeconds: 25          # GKE's default graceful termination period for Spot is 30 s; keep below it
  nodeSelector:
    cloud.google.com/gke-spot: "true"
  tolerations:
  - key: cloud.google.com/gke-spot
    operator: Equal
    value: "true"
    effect: NoSchedule
```
**Autopilot**: requesting Spot Pods with the same `nodeSelector` makes Autopilot automatically provision Spot VMs and add taints and tolerations. No node pool to create.

The cluster autoscaler can be configured to prefer Spot VMs when adding nodes; keep a non-Spot pool for system workloads.

## 3. Survive preemption
- Reclaiming Spot VMs is involuntary and is not covered by PodDisruptionBudget guarantees; spread replicas across nodes and zones.
- Compute Engine sends a preemption notice to GKE; the default graceful termination period is 30 seconds, so handle SIGTERM quickly. Extending it to 120 seconds needs recent control plane versions (see the Spot VMs page).
- Spot VMs have no expiration time.

## Gotchas
- Create clusters with at least one node pool without Spot VMs for system workloads such as DNS.
- The default autoscaler location policy is `ANY`.

## Verify
- [ ] `kubectl get nodes -l cloud.google.com/gke-spot=true` lists Spot nodes; tolerant pods land there, others don't.
- [ ] Draining a Spot node leaves the service available.

## Checked

2026-10-24, GKE Spot VMs concept and how-to pages on docs.cloud.google.com. Confirmed: `--spot`, label and taint keys, nodeSelector and toleration, `terminationGracePeriodSeconds: 25` example, 30-second default termination period, PodDisruptionBudget limitation, Autopilot Spot Pods behaviour, advice to keep a non-Spot pool, default location policy ANY. Removed unconfirmed claims: autoscaling flags, node affinity and compute-class fallback guidance, `podFailurePolicy` advice, StatefulSet zonal PV statement.

Method: documentation only; no commands were run.
