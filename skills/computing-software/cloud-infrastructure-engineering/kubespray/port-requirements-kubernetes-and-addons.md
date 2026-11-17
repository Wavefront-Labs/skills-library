---
id: computing-software.cloud-infrastructure-engineering.kubespray.port-requirements-kubernetes-and-addons
name: port-requirements-kubernetes-and-addons
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [ports, firewall, etcd, kubelet, nodeport, metallb]
level: intro
status: docs-checked
description: "Open the right ports between hosts: SSH, etcd 2379/2380, apiserver 6443, kubelet 10250, NodePort range, plus node exporter and MetalLB ports."
sources:
  - https://kubespray.io/docs/operations/port-requirements.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Firewalls must allow infrastructure components to talk to each other. Ports from the Kubespray page:

**Control plane**: TCP 22 (ssh for ansible), 2379 (etcd client), 2380 (etcd peer), 6443 (kubernetes api), 10250 (kubelet api), 10257 (kube-scheduler), 10259 (kube-controller-manager).

**Worker nodes**: TCP 22, 10250 (kubelet api), 30000-32767 (kube nodePort range).

The page refers to the upstream Kubernetes ports-and-protocols documentation for these.

**Addons**:

| Protocol | Port | Purpose |
|---|---|---|
| TCP | 9100 | node exporter |
| TCP/UDP | 7472 | metallb metrics |
| TCP/UDP | 7946 | metallb L2 operating mode |

Some ports are optional depending on configuration. CNI-specific ports are in the companion skill on Calico and Cilium ports.

## Checked

2026-11-04. Port tables were confirmed on the Port Requirements page.

Method: documentation only; no commands were run.
