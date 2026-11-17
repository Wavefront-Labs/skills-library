---
id: computing-software.cloud-infrastructure-engineering.kubernetes.offline-os-package-mirrors-for-kubernetes-nodes
name: offline-os-package-mirrors-for-kubernetes-nodes
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, air-gapped, package-mirror, offline-packages, pkgs-k8s-io, apt, dnf, kubeadm, containerd]
level: practitioner
status: docs-checked
description: "Mirror pkgs.k8s.io kubeadm/kubelet/kubectl repos and containerd/runc packages for offline nodes, pin versions per minor, and install/upgrade from the local mirror."
sources: ["https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/", "https://kubernetes.io/blog/2023/08/31/legacy-package-repository-deprecation/", "https://kubernetes.io/docs/tasks/administer-cluster/kubeadm/kubeadm-upgrade/", "https://github.com/containerd/containerd/blob/main/RELEASES.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline OS package mirrors for kubelet/kubeadm/containerd

## Repos to mirror
- `pkgs.k8s.io` has a dedicated package repository **per Kubernetes minor version**, for example
  `https://pkgs.k8s.io/core:/stable:/v<major>.<minor>/deb/` and `/rpm/`. The legacy
  `apt.kubernetes.io` and `yum.kubernetes.io` repositories were deprecated and frozen on
  13 September 2023 and cannot supply later releases. Mirror every minor you run and the next
  one (for upgrades). One signing key is used for all the repositories.
- containerd and runc: distro packages, a vendor repository, or static release archives; see the
  containerd and runc release pages. Check the containerd RELEASES.md table for support status
  before choosing a line.
- The packages' own dependencies: resolve them with your package manager when building the
  mirror. The Kubernetes RPM repository definition excludes `kubelet kubeadm kubectl cri-tools
  kubernetes-cni`, which gives the set of packages that repository supplies.

## Debian/Ubuntu
Mirror the repository with any apt mirroring tool (consult its documentation), snapshot it, and
publish it internally. On nodes, point apt at the internal mirror using the same `signed-by`
pattern the install guide uses, then hold the packages:
```bash
echo 'deb [signed-by=/etc/apt/keyrings/<internal-key>.gpg] https://mirror.internal/k8s-<minor>/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update && sudo apt-get install -y kubelet=<version> kubeadm=<version> kubectl=<version>
sudo apt-mark hold kubelet kubeadm kubectl
```
Use `apt-cache madison kubeadm` on a connected host to see the exact version strings.

## RHEL family
The install guide's repository file uses `gpgcheck=1`, a `gpgkey` URL and
`exclude=kubelet kubeadm kubectl cri-tools kubernetes-cni`; copy that pattern with your internal
`baseurl`/`gpgkey`, then install with the exclusion lifted for this repo only:
```bash
sudo dnf install -y kubelet kubeadm kubectl --disableexcludes=kubernetes
```
The `exclude` line keeps routine `dnf update` from upgrading those packages.

## Version discipline
- Snapshot mirrors (dated directories or snapshots) so a node built in 6 months gets the same
  packages; pin exact versions in your node build (Ansible, Packer).
- Upgrade order: add the next-minor repository, upgrade `kubeadm` first (control plane), then
  kubelet and kubectl per node, lifting the holds only for the upgrade (`apt-mark unhold`
  then `hold`).

## Verify
- [ ] A node build from scratch succeeds with no internet route.
- [ ] `apt-mark showhold` (or your DNF equivalent) shows the Kubernetes packages held.
- [ ] The mirror's GPG key is trusted; do not use `trusted=yes` or `gpgcheck=0`.

## Checked

Checked 2026-10-27 against Kubernetes documentation (kubernetes/website main tree, v1.38 development; latest release v1.37.1) and kubeadm/kubectl source: install-kubeadm page (per-minor pkgs.k8s.io repositories, same signing key for all, deb signed-by line, apt-mark hold, RPM repo fields gpgcheck/gpgkey/exclude and --disableexcludes=kubernetes, legacy repositories deprecated and frozen on 13 September 2023 via the site's legacy-repos notice), kubeadm-upgrade page (unhold/hold sequence) and containerd RELEASES.md. Removed unconfirmed aptly and reposync commands, dependency package list and the claim that the legacy repos were removed in 2024.

Method: documentation only; no commands were run.
