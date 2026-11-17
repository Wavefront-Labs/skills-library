---
id: computing-software.cloud-infrastructure-engineering.kubespray.cilium-ipam-and-pod-cidrs
name: cilium-ipam-and-pod-cidrs
category: computing-software
field: cloud-infrastructure-engineering
product: kubespray
tags: [cilium, ipam, pod-cidr, cluster-pool, load-balancer-ip-pools, ipv6]
level: practitioner
status: docs-checked
description: "Configure Cilium unprivileged mode, IPAM mode, pod CIDRs, per-node mask size and LB IPAM pools in Kubespray."
sources:
  - https://kubespray.io/docs/CNI/cilium.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Unprivileged agent.** Cilium is installed with `securityContext.privileged: false`, so set `kube_owner: root` in the inventory.

**IPAM mode.** The default is Cluster Scope. Choose another, for example:

```yml
cilium_ipam_mode: cluster-pool
```

**Cluster Pod CIDRs** default to `kube_pods_subnet`. If your node network is in the same range you will lose connectivity to other nodes.

```yml
cilium_pool_cidr: 10.233.64.0/18
cilium_pool_cidr_ipv6: fd85:ee78:d8a6:8607::1:0000/112
```

The IPv6 value is needed when `cilium_enable_ipv6` is used, and defaults to `kube_pods_subnet_ipv6`.

**Per-node size.** In Cluster Scope mode Cilium pre-allocates a segment to each node. `cilium_pool_mask_size` sets the size (default `kube_network_node_prefix`); `cilium_pool_mask_size_ipv6` the IPv6 size (default `kube_network_node_prefix_ipv6`):

```yml
cilium_pool_mask_size: "24"
cilium_pool_mask_size_ipv6: "120"
```

**Load balancer IP pools:**

```yml
cilium_loadbalancer_ip_pools:
  - name: "blue-pool"
    cidrs:
      - "10.0.10.0/24"
    ranges:
      - start: "20.0.20.100"
        stop: "20.0.20.200"
      - start: "1.2.3.4"
```

See the Cilium LB IPAM documentation for details.

## Checked

2026-11-08. Cited pages re-read in full. All variables and examples were confirmed on the Cilium page up to IP Load Balancer Pools.

Method: documentation only; no commands were run.
