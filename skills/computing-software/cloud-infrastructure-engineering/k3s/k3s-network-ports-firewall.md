---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-network-ports-firewall
name: k3s-network-ports-firewall
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, inbound-ports, port-6443, port-8472]
level: practitioner
status: docs-checked
description: "Which TCP and UDP ports K3s nodes need open between each other, and which are loopback only."
sources:
  - https://docs.k3s.io/installation/requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: open exactly the ports K3s needs.

Inbound rules for K3s nodes:

- TCP 2379-2380, servers to servers: only for HA with embedded etcd
- TCP 6443, agents to servers: K3s supervisor and Kubernetes API server
- UDP 8472, all nodes: only for Flannel VXLAN
- TCP 10250, all nodes: kubelet metrics and API
- UDP 51820 (IPv4) and 51821 (IPv6), all nodes: only for Flannel WireGuard
- TCP 5001 and TCP 6443, all nodes: only for the embedded distributed registry (Spegel)

Outbound traffic is typically all allowed. Nodes make outbound connections to the server (reverse tunnel) and kubelet traffic runs through it; if you use your own CNI instead of Flannel, the Flannel ports are not needed.

Loopback-only local ports to avoid reusing: 2381 etcd metrics, 2382 etcd legacy HTTP API, 6444 kube-apiserver local access, 10010 containerd CRI streaming, 10248 kubelet health, 10249 and 10256 kube-proxy, 10257 controller-manager, 10258 cloud-controller-manager, 10259 scheduler.

Security warnings: do not expose the VXLAN port 8472 to the world; run nodes behind a firewall or security group that blocks it. Flannel uses the Bridge CNI plugin, so pods with NET_RAW can attempt ARP spoofing; set a restricted profile without NET_RAW on untrusted pods.

## Checked

2026-11-08. Read the full K3s Requirements page (docs/installation/requirements.md in the k3s-io/docs repo). Confirmed: the inbound rules table (2379-2380, 6443, 8472, 10250, 51820, 51821, 5001 and 6443 for Spegel), outbound typically all allowed, reverse tunnelling and no Flannel ports with a custom CNI, the loopback local ports list, the VXLAN exposure warning and the NET_RAW warning. Nothing removed.

Method: documentation only; no commands were run.
