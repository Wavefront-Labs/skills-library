---
id: computing-software.cloud-infrastructure-engineering.metallb.dual-stack-services
name: dual-stack-services
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, dual-stack, preferdualstack, ipfamilypolicy, ipv6, ipfamilies, loadbalancerips]
level: advanced
status: docs-checked
description: "IPv6 and dual-stack LoadBalancer Services in MetalLB: dual-stack pool requirement, metallb.io/loadBalancerIPs for two IPs, PreferDualStack fallback and pool-change behaviour."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/usage/_index.md
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/configuration/_advanced_ipaddresspool_configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dual stack services

Support: IPv6 and dual stack work in L2 mode; in BGP mode only with FRR-based modes (FRR-K8s or FRR), not native.

Rules:
- Dual-stack Services need at least one pool containing both IPv4 and IPv6 addresses.
- `spec.loadBalancerIP` cannot request multiple IPs; use the annotation `metallb.io/loadBalancerIPs` with a comma-separated list.

PreferDualStack Service:
```yaml
spec:
  type: LoadBalancer
  ports:
  - port: 80
  ipFamilyPolicy: PreferDualStack
  ipFamilies:
  - IPv6
  - IPv4
```
With an advertisement listing `ipv4-pool`, `ipv6-pool` and `dualstack-pool`, the Service gets one IPv4 and one IPv6 from `dualstack-pool`. Without `dualstack-pool` listed, it gets an IPv6 from `ipv6-pool` (first family in `ipFamilies`). Empty `ipFamilies` prefers IPv4.

Pool changes:
- Single-stack pool extended to dual: the original IP stays and an extra IP from the new stack is added.
- Dual-stack pool becoming single-stack: assigned IPs are considered malfunctioning, both are cleared, and MetalLB re-assigns.
- A Service on a single-stack pool keeps its pool when a dual-stack pool appears.

## Checked

2026-11-04. Confirmed against the MetalLB Usage page (IPv6 and dual stack section) and Advanced AddressPool configuration (PreferDualStack example, pool-change behaviour). Removed the unsupported "controller logs" debug line.

Method: documentation only; no commands were run.
