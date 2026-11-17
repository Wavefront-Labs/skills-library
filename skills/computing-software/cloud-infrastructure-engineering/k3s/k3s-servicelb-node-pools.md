---
id: computing-software.cloud-infrastructure-engineering.k3s.k3s-servicelb-node-pools
name: k3s-servicelb-node-pools
category: computing-software
field: cloud-infrastructure-engineering
product: k3s
tags: [k3s, enablelb, lbpool, metallb]
level: advanced
status: docs-checked
description: "Restrict ServiceLB to labeled nodes or node pools, or disable ServiceLB to use another load balancer such as MetalLB."
sources:
  - https://docs.k3s.io/networking/networking-services
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Allow-list mode: add the label `svccontroller.k3s.cattle.io/enablelb=true` to one or more nodes. ServiceLB then runs only on labeled nodes; unlabeled nodes are excluded. By default no nodes are labeled, and while all remain unlabeled every node with a free port is used.

Pools: combine enablelb with matching `svccontroller.k3s.cattle.io/lbpool` values on nodes and Services. Example:

- Nodes A and B: lbpool=pool1 and enablelb=true
- Nodes C and D: lbpool=pool2 and enablelb=true
- A LoadBalancer Service on port 443 labeled lbpool=pool1 gets a DaemonSet only on A and B
- Another Service on port 443 labeled lbpool=pool2 gets pods only on C and D

The same label trick can confine the packaged Traefik Service to a pool, via the Traefik HelmChartConfig.

Disable ServiceLB with `--disable=servicelb` on every server. This is required to run a different LB such as MetalLB. While ServiceLB is disabled, LoadBalancer Services, including Traefik's, stay pending until another load balancer is installed, although their NodePorts are still allocated on every node. If you expose Traefik some other way, set its Service type to ClusterIP.

Do not confuse with external load balancers placed in front of the servers for the API; those are covered in the cluster load balancer pages.

## Checked

2026-11-08. Read the full K3s Networking Services page (docs/networking/networking-services.md in the k3s-io/docs repo). Confirmed: enablelb allow-list mode and default unlabeled behaviour, the lbpool example with pool1 and pool2, confining Traefik to a pool through matching labels in its HelmChartConfig, --disable=servicelb for MetalLB, pending Services with NodePorts still allocated, and the ClusterIP advice for Traefik. Nothing removed.

Method: documentation only; no commands were run.
