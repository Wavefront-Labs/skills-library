---
id: computing-software.cloud-infrastructure-engineering.kubernetes.bare-metal-vs-managed-cluster-lifecycle-differences
name: bare-metal-vs-managed-cluster-lifecycle-differences
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, eks, gke, aks, managed-kubernetes, bare-metal, kubeadm, control-plane-management, node-groups, managed-node-groups, cluster-upgrade, shared-responsibility]
level: advanced
status: gated
description: "What EKS/GKE/AKS manage for you versus what a kubeadm/bare-metal cluster leaves to the operator: control plane, etcd, certs, node pools, and upgrade mechanics compared."
sources: ["https://docs.aws.amazon.com/eks/latest/userguide/update-cluster.html", "https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html", "https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-control-plane", "https://learn.microsoft.com/en-us/azure/aks/upgrade-aks-node-pools-rolling", "https://learn.microsoft.com/en-us/azure/aks/supported-kubernetes-versions", "https://learn.microsoft.com/en-us/azure/aks/entra-id-authorization", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-certs/", "https://kubernetes.io/releases/version-skew-policy/", "https://cloud.google.com/kubernetes-engine/docs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bare-metal vs managed cluster lifecycle differences

**Goal:** know exactly which lifecycle skills in this catalogue a managed service makes
irrelevant, and which ones still apply — picking up a managed cluster and assuming
kubeadm-era habits (or vice versa) causes both wasted effort and missed operator
responsibility.

## 1. Control plane
- **Bare metal/kubeadm**: you build, upgrade, and troubleshoot the control plane
  yourself — `kubeadm-cluster-bootstrap`, `control-plane-ha-stacked-vs-external-etcd`,
  `static-pod-control-plane-management` all apply directly. API server downtime is your
  incident.
- **EKS/AKS (and GKE)**: the control plane is a managed service; you never manage
  `kube-apiserver`/`kube-scheduler`/`kube-controller-manager` processes, and there is no
  stacked-vs-external-etcd decision. "Upgrading the control plane" becomes a provider API call
  (`aws eks update-cluster-version`, `az aks upgrade --control-plane-only`). EKS, for example,
  replaces API server nodes in a rolling update, reverts automatically if its health checks
  fail, cannot be paused once started, and allows rollback to the previous minor within 7 days.

## 2. etcd
- **Bare metal/kubeadm**: fully your responsibility —
  `etcd-backup-and-restore`, `etcd-defragmentation-and-compaction`,
  `etcd-cluster-membership-and-recovery` all apply, and a mistake here is a cluster-wide
  outage you resolve yourself.
- **Managed**: etcd is not exposed: no access, no snapshots to manage, no membership to reason
  about. That removes a category of operator risk and also the lever: there is no "restore etcd
  from last night" option for you. EKS states that it backs up managed clusters, but plan your
  own DR as object-level backup of your workloads (for example Velero), not etcd snapshots.

## 3. Certificates
- **Bare metal/kubeadm**: `certificate-rotation-and-expiry-management` applies in
  full — you track leaf and CA expiry, and run `kubeadm certs renew` (kubeadm also renews
  certificates during control plane upgrades).
- **Managed**: the control-plane PKI is the provider's job. You still manage your own
  workload-facing certificates (Ingress TLS, service mesh mTLS, your admission webhooks) and any
  client credentials you issue.

## 4. Node lifecycle
- This is where the gap narrows the most. Even on managed services **you still**:
  - cordon/drain/taint for your own maintenance
    (`computing-software.cloud-infrastructure-engineering.kubernetes.node-maintenance-cordon-drain-taint`
    applies unchanged); provider-driven node upgrades do the cordon and drain for you (AKS
    rolling node pool upgrades; EKS Auto Mode, which updates nodes after a control plane
    upgrade and respects PDBs).
  - choose the upgrade strategy and schedule (AKS max surge, default one node, or max
    unavailable; EKS managed node group update settings).
  - size and configure the cluster autoscaler or provider equivalent (Karpenter, AKS cluster
    autoscaler).
- Version skew (`version-skew-policy`) still governs what's valid and managed services follow
  the same window rather than a stricter one: EKS allows kubelet up to three minors behind the
  API server (it recommends matching before each upgrade), and AKS requires the control plane
  and node pools to stay within N-3.

## 5. What's genuinely new on managed services
- IAM-to-RBAC mapping (EKS access entries or the legacy `aws-auth` ConfigMap, AKS Microsoft
  Entra ID with Azure RBAC) — a whole layer that doesn't exist on bare metal, where Kubernetes
  RBAC with your own authenticator is the model.
- Networking add-ons are often provider-supplied (AWS VPC CNI, Azure CNI) —
  CNI choice/tuning
  (`computing-software.cloud-infrastructure-engineering.kubernetes.cni-plugin-architecture-calico-cilium-flannel`)
  may be constrained by the provider's default, not a free choice like on bare metal.
- GKE equivalents (Autopilot node management, Workload Identity, node auto-provisioning,
  `gcloud container clusters upgrade --master`) are
  (gated: unconfirmed, source is paywalled or blocked). GKE documentation was not readable in a source repository for this review; confirm
  them in the GKE docs.

## Gotchas
- A failed managed control-plane upgrade is the provider's incident (EKS reverts it), but a
  node pool upgrade gone wrong (bad image, broken user data, PDBs that block drains) is yours.
- "It's managed, so there's no version-skew risk" is wrong — node pools drift behind the
  control plane if auto-upgrade is off or pools are pinned. AKS performs platform-initiated
  upgrades on clusters left on unsupported versions.
- Managed-service feature names and scope (EKS Auto Mode, AKS Automatic) change often; confirm
  current provider docs before relying on what is or isn't automated.

## Verify
- [ ] For any given cluster, there's an explicit written answer to "who owns control
      plane, etcd, cert, and node lifecycle here" — not an assumption carried over from
      a different platform.
- [ ] Node pool auto-upgrade settings are deliberately chosen, not left at whatever the
      provider defaults to.
- [ ] The DR story for a managed cluster has been reasoned through separately from
      "etcd snapshots" (which you don't have access to).
- [ ] IAM-to-RBAC mapping for the specific provider is documented, since it's the
      biggest genuinely-new surface versus bare metal.

## Checked
Checked 2026-10-27 against the Amazon EKS User Guide source (updating a cluster: rolling API
server replacement, automatic revert, no pause, 7-day rollback, regular backups, three-minor
kubelet skew, Auto Mode node updates respecting PDBs; access entries), MicrosoftDocs/azure-aks-docs
(control plane upgrade, rolling node pool upgrades with max surge and max unavailable, N-3 skew
and platform-initiated upgrades, Entra ID authorization) and kubernetes/website (kubeadm
certificate management, version skew policy). Corrected the claim that managed node tooling
enforces a stricter skew window than upstream; removed the unconfirmed EKS lifecycle hook and
GKE shielded/confidential node examples; replaced prose `sources:` titles with URLs. GKE claims
are gated because GKE docs were not readable.

Method: documentation only; no commands were run.
