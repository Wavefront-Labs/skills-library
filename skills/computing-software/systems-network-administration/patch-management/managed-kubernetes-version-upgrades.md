---
id: computing-software.systems-network-administration.patch-management.managed-kubernetes-version-upgrades
name: managed-kubernetes-version-upgrades
category: computing-software
field: systems-network-administration
product: patch-management
tags: [kubernetes-version-upgrade, eks, aks, gke, control-plane-upgrade, container-image-patching]
level: practitioner
status: docs-checked
description: "Upgrade managed Kubernetes (EKS, AKS, GKE) one minor at a time: deprecated API checks, control plane then node pools, add-ons, surge settings and support windows."
sources:
  - https://kubernetes.io/releases/version-skew-policy/
  - https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html
  - https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-cluster
  - https://cloud.google.com/kubernetes-engine/docs/how-to/upgrading-a-cluster
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed Kubernetes version upgrades

Upstream Kubernetes gives each minor about one year of patch support plus a two-month maintenance period; EKS, AKS and GKE publish their own support windows, so check each provider's calendar. Falling behind forces rushed multi-hop upgrades.

## Rules
- Control plane upgrades **one minor at a time** (1.29 -> 1.30 -> 1.31).
- Version skew: kubelet may be up to three minors older than kube-apiserver (two minors for kubelet older than 1.25), never newer.
- Order: check APIs -> control plane -> add-ons -> node pools.

## 1. Deprecated API check
```sh
kubent                                      # kube-no-trouble
kubectl get --raw /metrics | grep apiserver_requested_deprecated_apis
```
EKS cluster insights (upgrade insights) also scan for deprecated API usage; check your provider's equivalent. Fix manifests and Helm charts first.

## 2. Control plane
Version numbers below are examples; use a version your provider currently offers.
```sh
aws eks update-cluster-version --name prod --kubernetes-version 1.31
az aks upgrade -g rg -n prod --kubernetes-version 1.31.2 --control-plane-only
gcloud container clusters upgrade prod --master --cluster-version 1.31
```

## 3. Add-ons
CNI (VPC CNI/Azure CNI/Cilium), CoreDNS, kube-proxy, CSI drivers, ingress controllers, cert-manager: upgrade to versions supporting the new minor (`aws eks describe-addon-versions --kubernetes-version 1.31`).

## 4. Node pools
```sh
aws eks update-nodegroup-version --cluster-name prod --nodegroup-name ng1   # or Karpenter drift
az aks nodepool upgrade -g rg --cluster-name prod -n np1 --kubernetes-version 1.31.2 --max-surge 33%
gcloud container clusters upgrade prod --node-pool np1
```
Surge settings control speed vs capacity; PodDisruptionBudgets control safety (too strict PDBs block drains forever).

## Gotchas
- GKE release channels and AKS auto-upgrade channels can upgrade for you; set maintenance windows and exclusions.
- Admission webhooks failing closed during upgrade block pod scheduling; check `failurePolicy`.
- Node image (OS) patching is separate from version upgrades: AKS node image upgrade, EKS AMI release, GKE auto node upgrades.

## Verify
`kubectl version` and `kubectl get nodes -o wide` show target versions; no deprecated API calls in metrics; workloads healthy and PDBs satisfied.

## Checked
Date: 2026-10-27. Documentation checked: Kubernetes version skew policy and patch release pages (kubelet skew: three minors from 1.25, two before; about one year of patch support plus two months maintenance), deprecation policy (`apiserver_requested_deprecated_apis` metric), kube-no-trouble README (`kubent`), EKS update-cluster page (one minor at a time, cluster insights) and `eks update-cluster-version` / `describe-addon-versions --kubernetes-version` references, AKS upgrade page (`az aks upgrade --control-plane-only`), GKE upgrade page (`--master`, `--cluster-version`, one minor at a time, `--node-pool`). Removed the `pluto` command (its flags were not confirmed) and the provider extended-support claim.

Method: documentation only; no commands were run.
