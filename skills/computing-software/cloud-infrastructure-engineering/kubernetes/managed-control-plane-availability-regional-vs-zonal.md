---
id: computing-software.cloud-infrastructure-engineering.kubernetes.managed-control-plane-availability-regional-vs-zonal
name: managed-control-plane-availability-regional-vs-zonal
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, managed-kubernetes, regional-cluster, zonal-cluster, control-plane-sla, eks, gke, aks, uptime-sla, availability-zones, control-plane-ha, sla]
level: practitioner
status: draft
description: "What HA you actually get from EKS, GKE and AKS control planes: regional vs zonal, SLA tiers, what fails during a control-plane upgrade, and how to design workloads around it."
sources: ["https://cloud.google.com/kubernetes-engine/docs/concepts/regional-clusters", "https://docs.aws.amazon.com/eks/latest/userguide/disaster-recovery-resiliency.html", "https://learn.microsoft.com/en-us/azure/aks/free-standard-pricing-tiers"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Managed control-plane availability: regional vs zonal

**Goal:** pick the right control-plane tier and stop assuming "managed = HA by default".
Each provider's default is different, and the cheap tier is sometimes single-zone.

## Provider cheat sheet
| Provider | Default | HA option | SLA |
|---|---|---|---|
| **GKE** | Zonal (Standard, one zone, control plane is single-instance) | `--region` → regional cluster, 3 replicas across zones; Autopilot is always regional | Regional 99.95%, zonal 99.5% (financially backed only on Standard/Enterprise edition) |
| **EKS** | Always multi-AZ (≥2 AZs, AWS-managed) | n/a — control plane HA is built in; you pick subnets in ≥2 AZs at create | 99.95% |
| **AKS** | Free tier: no SLA, best effort | Standard tier (`--tier standard`) adds the uptime SLA; add `--zones 1 2 3` for zone-redundant | Standard 99.9%, 99.95% with AZs |

Key consequences:
- **GKE zonal**: the control plane is *unavailable during upgrades and zone outages*. Workloads
  keep running (kubelets are autonomous) but nothing can be scheduled, scaled or self-healed.
  Switching zonal → regional is not possible in place; it is a new cluster + migration.
- **EKS**: you never see control-plane instances; a bad subnet choice (one AZ) still gives
  you HA but your *nodes* and ENIs for the API endpoint live in that AZ.
- **AKS Free**: fine for dev; production must be Standard, and the tier can be flipped in place
  (`az aks update --tier standard`).

## Commands
```bash
# GKE
gcloud container clusters create prod --region europe-west2 --num-nodes 1 ...      # regional (1 node per zone)
gcloud container clusters describe prod --region europe-west2 --format='value(location,locations)'
# AKS
az aks create -g rg -n prod --tier standard --zones 1 2 3 --node-count 3 ...
az aks show -g rg -n prod --query 'sku'
# EKS — subnets decide the AZs
eksctl create cluster --name prod --region eu-west-2 --zones eu-west-2a,eu-west-2b,eu-west-2c
```

## What "control plane unavailable" breaks (and what it doesn't)
Keeps working: running pods, Services via kube-proxy rules already programmed, DNS (CoreDNS
pods are workloads), ingress controllers.
Stops: scheduling, HPA/VPA, autoscaler scale-up, cert rotation requests, `kubectl`, anything
that reconciles (operators, GitOps), new pod IP allocation on some CNIs, kubelet CSR renewals
if the window is long.
Design for it: readiness-based LBs, PDBs that tolerate node loss without rescheduling, no
in-request calls to the API server from app code.

## Gotchas
- SLA numbers are for the API endpoint, not for your workloads, and most require you to be on a
  supported Kubernetes version.
- GKE regional clusters bill for nodes in each zone — `--num-nodes 1` means 3 nodes total.
- Private clusters: the control plane is reachable only via the VPC peering/PSC endpoint; an
  outage of that path looks identical to a control-plane outage.
- Cluster autoscaler and node auto-repair are control-plane features — they pause during
  control-plane upgrades on every provider.

## Verify
- [ ] Provider console/CLI shows the expected tier and ≥3 zones for production clusters.
- [ ] During a planned control-plane upgrade, synthetic HTTP checks against the app stay green while `kubectl get nodes` may fail (zonal GKE) or stay up (regional/EKS/AKS Standard).
- [ ] Runbook includes "control plane down: what still works" so on-call does not restart healthy nodes.
