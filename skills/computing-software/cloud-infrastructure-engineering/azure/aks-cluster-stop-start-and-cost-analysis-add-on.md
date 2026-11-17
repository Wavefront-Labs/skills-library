---
id: computing-software.cloud-infrastructure-engineering.azure.aks-cluster-stop-start-and-cost-analysis-add-on
name: aks-cluster-stop-start-and-cost-analysis-add-on
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, aks, aks-stop-start, aks-cost-analysis, cost-optimisation, node-pool-stop, namespace-cost]
level: practitioner
status: docs-checked
description: "Cut AKS cost: stop/start whole clusters or user node pools, scale pools to zero, and see per-namespace cost with the AKS cost analysis add-on."
sources: ["https://learn.microsoft.com/azure/aks/start-stop-cluster", "https://learn.microsoft.com/azure/aks/start-stop-nodepools", "https://learn.microsoft.com/azure/aks/cost-analysis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AKS stop/start and cost analysis

**Goal:** non-production clusters don't burn money overnight, and teams see what their namespaces cost.

## Stop/start a cluster
```bash
az aks stop -g rg -n aks-dev
az aks show -g rg -n aks-dev --query powerState.code      # Stopped
az aks start -g rg -n aks-dev
```
- Stops the control plane and agent nodes; all objects except standalone pods are kept and restored from etcd on start.
- The API server IP address may change; with cluster autoscaler the node count after start may be outside your min/max.
- Cluster state is preserved for up to 12 months while stopped; only start or delete operations are allowed on a stopped cluster.
- Clusters using node auto-provisioning cannot be stopped; in capacity-constrained regions a start can fail, so avoid stopping mission-critical clusters.
- Automate with a scheduled pipeline or runbook calling `az aks stop` and `az aks start`.

## Stop or zero a node pool
```bash
az aks nodepool stop -g rg --cluster-name aks01 -n batch
az aks nodepool start -g rg --cluster-name aks01 -n batch
```
System pools can't be stopped; spot pools can, and stopped pools can be upgraded. The cluster and pool must be running and the pool's `provisioningState` must be `Succeeded`. Stopping a pool also stops its cluster autoscaler until the pool is started, and node pools of node auto-provisioning clusters can't be stopped.

## Cost analysis add-on
```bash
az aks update -g rg -n aks01 --enable-cost-analysis       # needs the Standard or Premium tier, not Free
```
- The add-on is built on OpenCost and shows cost by Kubernetes construct (clusters, namespaces) and by Azure compute, network and storage resources, including idle charges (capacity no workload uses). Allow up to 24 hours for data.
- Limits: about 7,000 containers per cluster (4 GB memory limit); once enabled you must disable it before downgrading the cluster to the Free tier.

## Other levers
Spot node pools for interruptible work, right-sized VM SKUs, node autoprovisioning, reservations/savings plans for
the steady baseline, and requests/limits so bin-packing works.

## Gotchas
- Standalone pods (not managed by a Deployment, StatefulSet, DaemonSet or Job) are deleted when the cluster stops.
- Webhook configurations that match cluster-scoped resources AKS manages during stop/start (nodes, leases, clusterroles) can cause the stop to be rejected.
- Anything polling the API (GitOps, monitoring) will alarm while the cluster is stopped; suppress alerts.

## Verify
- [ ] Dev cluster shows Stopped outside hours in the schedule's runs; namespace cost view populated within about 24 hours.

## Checked
Date: 2026-10-24. Checked against MicrosoftDocs/azure-aks-docs (start-stop-cluster, start-stop-nodepools, cost-analysis; main branch).
- Confirmed: `az aks stop/start`, `powerState.code`; objects restored except standalone pods; 12-month state retention; NAP clusters cannot be stopped; `az aks nodepool stop/start --cluster-name --nodepool-name`; system pools cannot be stopped, spot pools and upgrades are supported; Standard or Premium tier required for `--enable-cost-analysis`; OpenCost basis, idle charges, 24-hour data delay, 7,000-container limit.
- Removed as unconfirmed: scale-to-zero via `--node-count 0` and autoscaler `--min-count 0`, the VMSS-only remark, node name changes, and the 24-48 hour figure.
Method: documentation only; no commands were run.
