---
id: computing-software.cloud-infrastructure-engineering.talos-linux.talos-troubleshoot-api-etcd-kubelet
name: talos-troubleshoot-api-etcd-kubelet
category: computing-software
field: cloud-infrastructure-engineering
product: talos-linux
tags: [troubleshooting, talosctl, etcd, kubelet, discovery, control-plane, static-pods, certsans]
level: practitioner
status: docs-checked
description: "Talos failure triage with talosctl: API reachability, discovery membership, etcd stuck in Pre, kubelet and node registration, and control plane static pods."
sources:
  - https://github.com/siderolabs/docs/blob/main/public/talos/v1.15/troubleshooting/troubleshooting.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Work top-down; the guide assumes Discovery Service and KubePrism are enabled.

**Talos API (port 50000).** Control plane nodes always serve it; workers need control plane access to get TLS certificates. Check the firewall allows 50000/50001. Common client mistake: `talosctl gen config` writes `talosconfig` to the current directory while `talosctl` reads the talosconfig in its default `.talos` config directory; pass `--talosconfig`. If `talosctl` says certificate IPs are empty, the host subnet overlaps the default pod/service CIDRs `10.244.0.0/16` and `10.96.0.0/12`; change the machine configuration. Endpoints must be control plane addresses, never workers and never the VIP. With a TCP load balancer, add its address to `.machine.certSANs`.

**Health and logs.** `talosctl health` uses discovery for membership (override with `--control-plane-nodes` and `--worker-nodes`); `talosctl support` gathers logs offline.

**Discovery.** `talosctl -n <IP> get members` should agree on every node. Missing members: check connectivity to `discovery.talos.dev:443`. Duplicates: never reuse the same secrets across clusters. Removed nodes linger up to the 30 minute TTL unless reset.

**etcd.**

```
talosctl -n IP service etcd
talosctl -n IP etcd members
talosctl -n IP logs etcd
talosctl -n IP etcd alarm list
```

All members stuck in `Pre`: confirm one member was bootstrapped and images pull (`talosctl dmesg`, `retrying:`). Some stuck: port 2380 blocked or quorum lost (see disaster recovery). Crash loops: bad `extraArgs` or a non-empty disk with an old `/var/lib/etcd`.

**kubelet.** Check `talosctl image ls --namespace system` and `talosctl -n IP logs kubelet`. Wrong internal IP: set `nodeIP` in `KubeNodeConfig`. Stale nodes need `kubectl delete node`. A node is `Ready` only once the CNI is up.

**Control plane.** `talosctl -n <IP> get staticpods`, `talosctl -n <IP> dmesg | grep 'rendered new'`, `talosctl -n <IP> containers --namespace=cri`, and `talosctl -n <IP> get manifests` for bootstrap manifests. Start with `kube-apiserver`, which needs etcd.

## Checked

Each symptom and command above confirmed on the Troubleshooting page.

Method: docs-checked 2026-11-09 against the raw Troubleshooting page (v1.15 folder), read in full.
