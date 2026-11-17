---
id: computing-software.cloud-infrastructure-engineering.kubernetes.k3s-and-microk8s-ha-clusters
name: k3s-and-microk8s-ha-clusters
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, k3s, k3s-install, k3s-ha, embedded-etcd, microk8s, microk8s-addons, edge, lightweight-kubernetes, k3s-config]
level: practitioner
status: gated
description: "Stand up lightweight HA clusters: k3s with embedded etcd (server tokens, fixed registration address, disabling bundled components) and MicroK8s with addons and dqlite HA."
sources: ["https://docs.k3s.io/datastore/ha-embedded", "https://docs.k3s.io/installation/configuration", "https://docs.k3s.io/installation/packaged-components", "https://canonical.com/microk8s/docs/high-availability", "https://canonical.com/microk8s/docs/addons"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# k3s and MicroK8s HA clusters

## k3s with embedded etcd (3 servers)
```bash
# server 1
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=<version> K3S_TOKEN=<shared-secret> sh -s - server \
  --cluster-init --tls-san k3s.example.internal \
  --disable traefik --disable servicelb          # if bringing your own ingress / MetalLB
# servers 2 and 3
curl -sfL https://get.k3s.io | INSTALL_K3S_VERSION=<version> K3S_TOKEN=<shared-secret> sh -s - server \
  --server https://k3s.example.internal:6443 --tls-san k3s.example.internal
# agents
curl -sfL https://get.k3s.io | K3S_TOKEN=<shared-secret> sh -s - agent --server https://k3s.example.internal:6443
```
- Use an **odd number** of servers (3/5) for etcd quorum; `k3s.example.internal` is the optional
  "fixed registration address" (needs `--tls-san`).
- Persist config in `/etc/rancher/k3s/config.yaml` (drop-ins in `config.yaml.d/*.yaml`) instead of flags (same keys).
- Kubeconfig: `/etc/rancher/k3s/k3s.yaml` (replace server address).
- Snapshots: `k3s etcd-snapshot save`; scheduled by default at 00:00 and 12:00 system time, 5 kept per
  server node, in `/var/lib/rancher/k3s/server/db/snapshots` (S3 with `--etcd-s3`).
- Upgrades: system-upgrade-controller `Plan` CRs or rerun install with the new version, servers
  first one at a time.
- Bundled: containerd, Flannel, CoreDNS, Traefik, ServiceLB, kube-router network policy,
  local-path-provisioner, metrics-server, Spegel registry mirror; AddOns (`coredns`, `traefik`,
  `local-storage`, `metrics-server`, `servicelb`) can be removed with `--disable`.

## MicroK8s (snap) HA
```bash
snap install microk8s --classic --channel=<track>/stable   # (gated: unconfirmed, source is paywalled or blocked). Snap channel names were not checked against current docs.
microk8s status --wait-ready
microk8s add-node                     # prints a join command
microk8s join 10.0.0.11:25000/<token> # on nodes 2,3 → dqlite HA automatically at 3+ voters
microk8s kubectl get nodes
microk8s enable dns ingress metrics-server hostpath-storage rbac
microk8s enable metallb:10.0.0.200-10.0.0.220   # (gated: unconfirmed, source is paywalled or blocked). The addons page describes metallb without showing the range syntax.
microk8s disable <addon>
```
The datastore is dqlite and HA needs at least three nodes. Snap auto-refresh can upgrade clusters
unexpectedly; pin the channel and hold refreshes (`snap refresh --hold`) (gated: unconfirmed, source is paywalled or blocked). Snap documentation was not checked.

## Choosing
k3s: single binary with batteries included (see the k3s introduction). MicroK8s: snap-based with
addons. Both: you still own datastore backups and upgrades.

## Verify
- [ ] Killing one server keeps the API available; `k3s etcd-snapshot ls` shows recent snapshots.

## Checked

2026-10-26, against k3s-io/docs and rancher/rke2-docs on main (latest commits 2026-10-23/24; docs mention RKE2 v1.37 and containerd 2.0 era releases), and canonical.com/microk8s docs (high-availability and addons pages). Confirmed: k3s HA commands (`--cluster-init`, `--server`, `K3S_TOKEN`, `--tls-san`), odd server count, config file locations, bundled components and `--disable`, default snapshot schedule and retention, kubeconfig path; MicroK8s join command form with port 25000, three-node HA minimum, dqlite, addon names (`dns`, `ingress`, `metrics-server`, `hostpath-storage`, `rbac`, `metallb`). Not confirmed and marked gated: snap channel, metallb range syntax, snap refresh hold. Removed pinned k3s version, CNCF-certified and edge/ARM claims, `microk8s addons repo list`, and the one-time token wording.

Method: documentation only; no commands were run.
