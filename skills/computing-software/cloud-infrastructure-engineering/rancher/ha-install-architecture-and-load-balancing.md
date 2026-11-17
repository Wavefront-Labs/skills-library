---
id: computing-software.cloud-infrastructure-engineering.rancher.ha-install-architecture-and-load-balancing
name: ha-install-architecture-and-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: rancher
tags: [high-availability, etcd, layer-4, load-balancer, ingress, architecture]
level: intro
status: docs-checked
description: "Rancher HA install shape: Helm on three nodes, etcd odd node count, a layer 4 load balancer on 80/443, and where TLS terminates."
sources:
  - https://ranchermanager.docs.rancher.com/how-to-guides/new-user-guides/kubernetes-cluster-setup/high-availability-installs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Rancher recommends installing with Helm on a **dedicated Kubernetes cluster**. This is called a high-availability install because Rancher runs as a replica on each of three nodes. The nodes are typically hosted at a provider such as Amazon EC2 or Google Compute Engine, with Kubernetes installed first and Helm placing Rancher on top.

Rancher server data lives in etcd, which also runs on all three nodes. etcd needs an **odd number of nodes** so it can always elect a leader with a majority. If it cannot elect a leader it can fail, and the cluster then has to be restored from backup.

The recommended traffic path on the page:

- DNS for Rancher resolves to a **layer 4 load balancer**.
- The load balancer forwards TCP/80 and TCP/443 to all three cluster nodes.
- The ingress controller redirects HTTP to HTTPS and terminates TLS on TCP/443.
- The ingress controller then forwards to TCP/80 on the Rancher pod.

So with the recommended design TLS terminates at the ingress controllers inside the cluster, not at the load balancer (the page's figure caption). How Rancher works is the same regardless of install method; the page points to the architecture section for that.

## Checked

2026-11-09. Read the cited About High-availability Installations page in full and checked every claim against it (Helm on a dedicated cluster, three nodes, etcd odd count, layer 4 load balancer, ports, ingress TLS termination). Removed the inference about two nodes and the layer 7 termination remark, which the page does not state.

Method: documentation only; no commands were run.
