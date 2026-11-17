---
id: computing-software.cloud-infrastructure-engineering.cilium.lb-ipam-ip-pools
name: lb-ipam-ip-pools
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, lb-ipam, ciliumloadbalancerippool, ip-pool, serviceselector, allowfirstlastips]
level: practitioner
status: docs-checked
description: "Create CiliumLoadBalancerIPPool blocks with CIDR or start/stop ranges, service selectors, reserved first/last IPs, conflict handling and disabling."
sources:
  - https://docs.cilium.io/en/stable/network/lb-ipam/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LB IPAM IP pools

LB IPAM allocates IPs for `type: LoadBalancer` Services; it is always enabled but dormant until the first pool exists. It only assigns IPs. Advertise them with BGP Control Plane or L2 announcements.

## Pool
`CiliumLoadBalancerIPPool` with `spec.blocks`, each either `cidr` (IPv4 or IPv6) or a `start`/`stop` pair. Caution: start and stop belong to ONE list item. Check with `kubectl get ippools` (columns DISABLED, CONFLICTING, IPS AVAILABLE).

- `spec.allowFirstLastIPs: No` reserves the first and last IP of CIDR blocks. Ignored for /32 /31 IPv4 and /128 /127 IPv6, and for start/stop blocks. Default uses all IPs.
- `spec.serviceSelector`: label selector limiting which services get IPs (`matchLabels` or `matchExpressions`). None means any service. Special keys `io.kubernetes.service.namespace` and `io.kubernetes.service.name` match metadata namespace and name.
- `spec.disabled: true` stops new allocations but keeps existing ones, to drain a pool.

## Conflicts
Overlapping CIDRs between pools: the LAST added pool is marked Conflicting and allocates nothing. Read why with `kubectl get ippools/red-pool -o jsonpath='{.status.conditions[?(@.type=="cilium.io/PoolConflict")].message}'`. Always check pool status after changes.

## Status
Conditions `cilium.io/IPsTotal`, `cilium.io/IPsAvailable`, `cilium.io/IPsUsed` hold counts in `message`.

## Warning
Updating a pool can reassign IPs so service IPs may change (GitHub issue 40358).

## Checked

2026-11-08. Read in full against the Cilium docs source (rst) of the LB IPAM page: https://docs.cilium.io/en/stable/network/lb-ipam/. Confirmed the pool blocks, allowFirstLastIPs, serviceSelector, conflict, disabled and status condition details stated above. Nothing was removed.

Method: documentation only; no commands were run.
