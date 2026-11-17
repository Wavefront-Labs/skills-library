---
id: computing-software.cloud-infrastructure-engineering.kubernetes.managed-cluster-upgrades-eks-gke-aks
name: managed-cluster-upgrades-eks-gke-aks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, managed-cluster-upgrade, node-pool-upgrade, surge-upgrade, eks, gke, aks, blue-green-node-pool, release-channel, auto-upgrade-channel, cluster-upgrade, maintenance-window]
level: practitioner
status: gated
description: "Upgrade EKS/GKE/AKS in the right order (control plane, then node pools via surge or blue/green), with provider commands, maintenance windows and skew traps."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html", "https://docs.aws.amazon.com/eks/latest/userguide/kubernetes-versions.html", "https://karpenter.sh/docs/concepts/nodeclasses/", "https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/docs/concepts/workloads/pods/disruptions/", "https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane", "https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-node-pools-rolling", "https://learn.microsoft.com/en-us/azure/aks/auto-upgrade-cluster", "https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions", "https://cloud.google.com/kubernetes-engine/docs/concepts/node-pool-upgrade-strategies"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Managed cluster upgrades (EKS, GKE, AKS)

**Goal:** one minor version at a time, control plane first, then node pools, without
violating PDBs or the kubelet skew rule (kubelet may be up to 3 minors older than the
apiserver, never newer). Managed upgrades are easy to start and easy to leave half-done: a
control plane several minors ahead of its node pools is the normal failure.

## Common pre-flight (all providers)
```bash
kubectl version                                       # server vs node versions
kubectl get nodes -o custom-columns=NAME:.metadata.name,VER:.status.nodeInfo.kubeletVersion
kubectl get pdb -A -o custom-columns=NS:.metadata.namespace,NAME:.metadata.name,ALLOWED:.status.disruptionsAllowed | awk '$3==0'
```
Scan for APIs removed in the target version (EKS upgrade insights do this for EKS). Any PDB
with `disruptionsAllowed: 0` blocks node drains, so a node-pool upgrade stalls on it; fix it
before starting. Check addon/CNI/CSI compatibility for the target minor.

## EKS
```bash
aws eks update-cluster-version --name prod --kubernetes-version <next-minor>   # control plane; API stays available
aws eks describe-update --name prod --update-id <id>
# managed node group, rolling update
aws eks update-nodegroup-version --cluster-name prod --nodegroup-name ng-1 --kubernetes-version <next-minor>
# then EKS add-ons
aws eks describe-addon-versions --kubernetes-version <next-minor> --addon-name vpc-cni
aws eks update-addon --cluster-name prod --addon-name vpc-cni --addon-version <version>
```
EKS upgrades one minor at a time, cannot be paused once started, needs up to five free IPs in
the cluster subnets, and can be rolled back to the previous minor within 7 days. Its documented
order is control plane, then nodes, then cluster applications (for example Cluster Autoscaler),
then the EKS add-ons (VPC CNI, CoreDNS, kube-proxy), then clients such as kubectl. Kubelet
1.28+ may be three minors behind; AWS recommends matching node and control plane versions
before each upgrade.
Karpenter nodes: select AMIs with an `amiSelectorTerms` alias (`al2023@latest` or a pinned
`al2023@vYYYYMMDD`) and let drift replace nodes when the AMI changes.

## GKE
```bash
gcloud container clusters upgrade prod --region europe-west2 --master --cluster-version <next-minor>   # control plane
gcloud container clusters upgrade prod --region europe-west2 --node-pool default-pool --cluster-version <next-minor>
gcloud container node-pools update default-pool --cluster prod --region europe-west2 \
  --max-surge-upgrade 1 --max-unavailable-upgrade 0
gcloud container node-pools update default-pool ... --enable-blue-green-upgrade --node-pool-soak-duration 1h
```
The gcloud flags above are (gated: unconfirmed, source is paywalled or blocked). GKE
documentation is not in a readable source repository for this review, so confirm them in the
GKE node pool upgrade strategy docs.
Release channels auto-upgrade both control plane and nodes, and maintenance windows plus
exclusions control when (gated: unconfirmed, source is paywalled or blocked). Zonal clusters
lose the API during the control-plane step while regional clusters do not
(gated: unconfirmed, source is paywalled or blocked).

## AKS
```bash
az aks get-upgrades -g rg -n prod -o table
az aks upgrade -g rg -n prod --kubernetes-version <next-version> --control-plane-only
az aks nodepool upgrade -g rg --cluster-name prod -n sys --kubernetes-version <next-version> --max-surge 33%
az aks nodepool upgrade ... --node-image-only          # OS image only, same Kubernetes version
az aks update -g rg -n prod --auto-upgrade-channel stable   # none | patch | stable | rapid
```
Non-LTS AKS clusters cannot skip minor versions. The default max surge is one node; surge nodes
need compute and IP quota, and AKS falls back to a surge of one and then to an in-place upgrade
using `--max-unavailable` when quota is short. A PDB that never allows eviction fails the drain
(error code `PodDrainFailure`); `--undrainable-node-behavior Cordon` (default `Schedule`)
changes how undrainable nodes are handled, or fix the PDB. The `node-image` cluster channel is
legacy; use `--node-os-upgrade-channel NodeImage` instead. The `patch` channel never moves to a
new minor, and clusters left on an unsupported version get a platform-initiated upgrade after a
60-day grace period, even outside the maintenance window.

## Ordering and skew
1. Control plane (+1 minor).
2. Nodes and core add-ons in the provider's documented order (EKS: nodes, then add-ons).
3. Node pools: system pools before user pools.
4. Cluster-scoped operators that pin a client-go (cert-manager, ingress, service mesh).
Repeat per minor; never skip a minor on the control plane.

## Gotchas
- Surge upgrades create extra nodes, so quota or IP exhaustion fails the upgrade half-way;
  check subnet free IPs and vCPU quota first.
- Node pool upgrades re-create nodes: local emptyDir/hostPath data is gone, and node labels set
  by hand (not in the pool template) vanish.
- Auto-upgrade channels can upgrade you into a version your CNI doesn't support yet; pin
  maintenance windows and keep an exclusion while you validate.

## Verify
- [ ] `kubectl get nodes` shows every node at the target minor.
- [ ] Add-on versions match the provider's recommendation for that minor (`aws eks describe-addon`, AKS/GKE add-on status).
- [ ] App SLOs held through the node roll (no PDB stalls in provider upgrade logs).

## Checked
Checked 2026-10-27 against the Amazon EKS User Guide source (updating a cluster: one minor at
a time, no pause, five IPs, 7-day rollback, upgrade order, kubelet three-minor skew; Kubernetes
versions page), Karpenter docs (`amiSelectorTerms` alias, drift), kubernetes/website version
skew policy and Disruptions, and MicrosoftDocs/azure-aks-docs (control plane upgrade and no
minor skipping, rolling node pool upgrades with max surge, max unavailable, quota fallback and
the `PodDrainFailure` troubleshooting link, auto-upgrade channels with `node-image` legacy and
platform-initiated upgrades) plus the Azure CLI `acs` help source (`--control-plane-only`,
`--node-image-only`, `--undrainable-node-behavior`). Corrected the claim that EKS refuses an
upgrade when nodes are more than two minors behind (EKS allows three-minor kubelet skew) and the
EKS order (nodes before add-ons). Removed the upgrade duration figure and the kube-proxy
ordering claim. GKE claims are gated because GKE docs were not readable.

Method: documentation only; no commands were run.
