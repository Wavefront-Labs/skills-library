---
id: computing-software.cloud-infrastructure-engineering.kubernetes.version-skew-policy
name: version-skew-policy
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, version-skew, kube-apiserver, kubelet, kube-proxy, kubectl, minor-version, upgrade-order, compatibility, control-plane-upgrade, deprecation-policy, kubelet-skew]
level: advanced
status: docs-checked
description: "The exact minor-version skew Kubernetes allows between kube-apiserver, kubelet, kube-proxy, and kubectl, and the upgrade order it forces."
sources: ["https://kubernetes.io/releases/version-skew-policy/", "https://kubernetes.io/docs/reference/using-api/deprecation-guide/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Kubernetes version skew policy

**Goal:** know exactly how far each component can lag `kube-apiserver` so an upgrade
plan is derived from the rule, not guessed. This is the policy that
`computing-software.cloud-infrastructure-engineering.kubernetes.kubeadm-cluster-upgrade-sequencing`
executes against. Specific cluster deployment tools may add restrictions.

## 1. The skew table (current upstream policy)
- **kube-apiserver to kube-apiserver** (HA control plane): the newest and oldest
  `kube-apiserver` instances must be within **one minor version**.
- **kubelet to kube-apiserver**: kubelet must not be newer than `kube-apiserver` and may be up
  to **three minor versions older** (kubelet older than 1.25 may only be up to two minors
  older). If apiserver instances in an HA cluster differ, the allowed kubelet versions narrow,
  because kubelet must not be newer than any apiserver instance it talks to.
- **kube-proxy to kube-apiserver**: must not be newer; up to three minor versions older
  (two for kube-proxy older than 1.25). Relative to the kubelet on the same node, kube-proxy
  may be up to three minor versions older or newer (two for kube-proxy older than 1.25).
- **kubectl to kube-apiserver**: within **one minor version, older or newer**. With a mixed HA
  control plane, only the overlap is supported.
- **kube-controller-manager, kube-scheduler, cloud-controller-manager**: must not be newer
  than the `kube-apiserver` instances they communicate with. They are expected to match the
  apiserver minor but may be **up to one minor older** (to allow live upgrades). If they reach
  any apiserver through a load balancer in a mixed-version HA cluster, the allowed versions narrow.

## 2. The ordering this forces
1. Upgrade `kube-apiserver` instances first (in HA, all instances before the components below
   that can reach any of them). Prerequisites: controller-manager, scheduler and
   cloud-controller-manager at the previous minor; kubelets at the previous one or two minors;
   admission webhooks able to handle new API versions and fields.
2. Then `kube-controller-manager`, `kube-scheduler` and `cloud-controller-manager`, in any
   order or simultaneously.
3. Then `kubelet` and `kube-proxy`, optionally: they may stay at up to three minors behind.
   Drain a node before a minor kubelet upgrade; in-place minor kubelet upgrades are not
   supported.
4. kubectl can be changed any time within its one-minor window.
- `kube-apiserver` must not skip minor versions when upgrading, even in a single-instance
  cluster (API deprecation policy and API change guidelines).
- Before upgrading, the project recommends being on the latest patch of the current minor and
  upgrading to the latest patch of the target minor.

## 3. Why this matters beyond "it's the rule"
- Add-ons (CNI, CSI drivers, metrics-server, cluster-autoscaler) have their own compatibility
  matrices; this policy covers only the core components.
- Removed or graduated APIs, changed defaults and third-party webhooks can break across minors
  independently of skew. See the deprecation guide for removals by release.

## Gotchas
- Running kubelets or kube-proxies persistently three minors behind means they must be upgraded
  before the control plane can be upgraded again.
- The number is version dependent (two minors for kubelet before 1.25, three since); confirm
  the current page for the Kubernetes version in play.
- Managed services (EKS/GKE/AKS) can enforce stricter rules than upstream; see
  `computing-software.cloud-infrastructure-engineering.kubernetes.bare-metal-vs-managed-cluster-lifecycle-differences`.

## Verify
- [ ] `kubectl version` and `kubectl get nodes -o wide` (kubelet version column) show
      every component within its allowed skew of the current `kube-apiserver` version.
- [ ] The upgrade plan steps through each intervening minor version, with no multi-minor
      jumps on the control plane.
- [ ] Each cluster add-on's support matrix has been checked against the target minor.

## Checked
Date: 2026-10-27. Documentation: Kubernetes website "Version Skew Policy" (current docs; latest
release v1.37.1). Confirmed: all skew numbers above, the pre-1.25 exceptions, kube-proxy to
kubelet window, controller-manager/scheduler may be one minor older, upgrade order and
prerequisites, drain requirement and no-skip rule. The page allows kube-proxy up to three minors
either way from its node's kubelet and does not call a mixed pair unsupported.
Method: documentation only; no commands were run.
