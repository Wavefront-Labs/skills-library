---
id: computing-software.cloud-infrastructure-engineering.kubernetes.cis-file-permission-and-ownership-checks
name: cis-file-permission-and-ownership-checks
category: computing-software
field: cloud-infrastructure-engineering
product: kubernetes
tags: [kubernetes, k8s, cis-benchmark, cis-file-permissions, node-hardening, pki, kube-bench]
level: practitioner
status: docs-checked
description: "Check and fix CIS benchmark file permission and ownership items for control-plane manifests, kubeconfigs, PKI, etcd data and kubelet files."
sources: ["https://www.cisecurity.org/benchmark/kubernetes", "https://github.com/aquasecurity/kube-bench/tree/main/cfg", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/master.yaml", "https://github.com/aquasecurity/kube-bench/blob/main/cfg/cis-1.9/node.yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CIS file permission and ownership checks

Sections 1.1 (control plane) and 4.1 (worker) of the benchmark. Values and ids below follow kube-bench's
`cis-1.9`; check the version kube-bench selects for your cluster.

| Path | Mode (or stricter) | Owner | Check |
|---|---|---|---|
| `/etc/kubernetes/manifests/*.yaml` (apiserver, controller manager, scheduler, etcd pod specs) | 600 | root:root | 1.1.1-1.1.8 |
| `/etc/kubernetes/admin.conf`, and `super-admin.conf` if present (Kubernetes 1.29+) | 600 | root:root | 1.1.13-1.1.14 |
| `scheduler.conf`, `controller-manager.conf` | 600 | root:root | 1.1.15-1.1.18 |
| `/etc/kubernetes/pki/` | ownership root:root; certificates 600; keys 600 | root:root | 1.1.19-1.1.21 |
| etcd data dir `/var/lib/etcd` | 700 | etcd:etcd | 1.1.11-1.1.12 |
| CNI config files (Manual) | 600 | root:root | 1.1.9-1.1.10 |
| `/etc/kubernetes/kubelet.conf` (the kubelet `--kubeconfig` file) | 600 | root:root | 4.1.5-4.1.6 |
| `/var/lib/kubelet/config.yaml` | 600 | root:root | 4.1.9-4.1.10 |
| kubelet systemd service file | 600 | root:root | 4.1.1-4.1.2 |
| client CA file used by kubelet (Manual) | 600 | root:root | 4.1.7-4.1.8 |

## Audit
```bash
stat -c '%a %U:%G %n' /etc/kubernetes/manifests/* /etc/kubernetes/*.conf /var/lib/kubelet/config.yaml
find /etc/kubernetes/pki -type f -exec stat -c '%a %U:%G %n' {} +
stat -c '%a %U:%G %n' /var/lib/etcd
```

## Fix
```bash
chmod 600 /etc/kubernetes/manifests/*.yaml /etc/kubernetes/*.conf /var/lib/kubelet/config.yaml
chown root:root /etc/kubernetes/manifests/*.yaml /etc/kubernetes/*.conf
find /etc/kubernetes/pki -type f -exec chmod 600 {} +
chmod 700 /var/lib/etcd
```
Bake these into the node image or config management so new nodes start compliant, and re-run the audit
after upgrades.

## Verify
```bash
kube-bench run --targets master,node 2>/dev/null | grep -E '\] (1\.1|4\.1)\.' | grep -v PASS
```
returns nothing (or only items accepted with a written exception).

## Checked
2026-10-28. Confirmed: every path, mode, owner and check id above against kube-bench `cfg/cis-1.9`
`master.yaml` and `node.yaml`, including `super-admin.conf` "on Kubernetes 1.29+, if present", `etcd:etcd`
and 600-or-more-restrictive wording for certificates and the client CA file; `--targets` against the
kube-bench docs. Removed: the claim that kubeadm runs etcd as root (not on the pages read). The CIS PDF is
not readable without registration, so ids come from kube-bench.
Method: documentation only; no commands were run.
