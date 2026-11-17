---
id: computing-software.cloud-infrastructure-engineering.kubernetes.upgrading-cluster-addons-coredns-kube-proxy-cni
name: upgrading-cluster-addons-coredns-kube-proxy-cni
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, addon-upgrade, coredns-upgrade, cni-upgrade, kube-proxy-upgrade, coredns, kube-proxy, cilium, calico, kubeadm, cluster-upgrade, corefile-migration]
level: practitioner
status: docs-checked
description: "Upgrade CoreDNS, kube-proxy and the CNI alongside a cluster upgrade: what kubeadm automates, Corefile migration, CNI rollout order, avoiding DNS/datapath outages."
sources: ["https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://kubernetes.io/docs/tasks/administer-cluster/coredns/", "https://kubernetes.io/releases/version-skew-policy/", "https://github.com/coredns/deployment/blob/master/kubernetes/Upgrading_CoreDNS.md", "https://docs.cilium.io/en/stable/operations/upgrade/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading cluster addons: CoreDNS, kube-proxy, CNI

**Goal:** the three addons every pod depends on get upgraded deliberately, in the right order,
without a window where DNS or the datapath is gone.

## What kubeadm handles
`kubeadm upgrade apply` applies the new **CoreDNS** and **kube-proxy** manifests (and RBAC). It does not
upgrade the CNI: the kubeadm docs say to upgrade your CNI provider manually and follow its own
instructions. The Kubernetes DNS docs say kubeadm can retain the existing Corefile automatically.
Since v1.28 kubeadm waits to upgrade the addons until the last control plane instance is upgraded, so
upgrade control plane nodes sequentially; before v1.28 it upgraded them during the first `apply`.
Back up the Corefile before upgrading:
```bash
kubectl -n kube-system get cm coredns -o yaml > corefile.bak
```
`kubeadm upgrade diff` shows the changes to static pod manifests (not the Corefile). The CoreDNS version
for each Kubernetes release is listed in the CoreDNS deployment repo's `CoreDNS-k8s_version.md`.
kubeadm has an `addon` upgrade phase; see `kubeadm upgrade apply phase addon --help` to skip one.

## CoreDNS by hand (managed clusters or Helm-managed)
```bash
# Managed clusters: use the provider's addon mechanism first
# Helm (coredns/coredns chart)
helm upgrade coredns coredns/coredns -n kube-system -f values.yaml --version <chart>
```
Follow the CoreDNS project's Upgrading_CoreDNS guide (linked from the Kubernetes DNS docs) and read the
CoreDNS release notes for plugin syntax changes. After the roll, check the CoreDNS logs for errors.

## kube-proxy
kubeadm: applied during `kubeadm upgrade apply`. Managed: provider addon mechanism. Self-managed
DaemonSet: per the version skew policy kube-proxy must not be newer than kube-apiserver and may be up to
three minor versions older (two for kube-proxy before 1.25), so bump it *after* the control plane upgrade. Not running
kube-proxy (Cilium kubeProxyReplacement)? Then make sure the DaemonSet is actually absent, not
just scaled, or an upgrade may resurrect it.

## CNI
Each CNI has its own upgrade instructions and Kubernetes support matrix; check your provider's
docs (the kubeadm docs point to the Kubernetes addons page).
- **Cilium** (from its upgrade guide): upgrade to the latest patch release of your current minor first,
  then to the next minor. Run the pre-flight check (`preflight.enabled=true`, `cilium-preflight.yaml`)
  before upgrading. Set `upgradeCompatibility` to the version you originally installed to minimise datapath
  disruption. With `helm upgrade` between minors do **not** use `--reuse-values`; save the old values to a
  file, check for renamed values and pass it with `-f`. Upgrade the operator only as the guide describes.
- Calico, Flannel and other CNIs: follow the provider's own guide; their docs were not checked here.

## Order for a full upgrade
1. Check your CNI's support matrix for the current and target Kubernetes minor and upgrade it first if needed.
2. Control plane upgrade (kubeadm applies CoreDNS + kube-proxy after the last control plane instance).
3. Node roll.
4. Upgrade the CNI further if it had to stay back.
5. Verify DNS and connectivity (below).

## Gotchas
- A Corefile with a plugin or syntax the new CoreDNS does not accept can break DNS; keep `corefile.bak`
  so you can restore the ConfigMap.
- kube-proxy newer than the apiserver is unsupported skew.

## Verify
- [ ] `kubectl -n kube-system rollout status deploy/coredns` succeeds, and a throwaway pod running `nslookup kubernetes.default` resolves (use an image that contains nslookup).
- [ ] The kube-proxy image is not newer than the control plane and within the skew policy.
- [ ] The CNI's own status command is green and a cross-node pod-to-pod connection works.

## Checked

2026-10-26, against Kubernetes website docs (kubeadm-upgrade, coredns, version-skew-policy, kubeadm reference), Cilium upgrade guide (cilium/cilium Documentation/operations/upgrade.rst). Confirmed: kubeadm applies CoreDNS and kube-proxy but leaves the CNI to you, v1.28 addon-upgrade ordering change, kubeadm retains the Corefile, kube-proxy skew rules, `kubeadm upgrade diff` scope, Cilium preflight, `upgradeCompatibility` and the --reuse-values prohibition. Wrong: `kubeadm upgrade diff` was described as showing a CoreDNS/Corefile diff (it shows static pod manifest changes), and the Cilium helm command used `--reuse-values`, which the Cilium guide forbids. Removed unconfirmed EKS version strings, CoreDNS plugin-history claims, replica/PDB advice, Calico and Flannel steps and the kubeadm replica-reset claim.

Method: documentation only; no commands were run.
