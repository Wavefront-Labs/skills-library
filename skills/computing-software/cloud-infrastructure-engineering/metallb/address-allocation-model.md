---
id: computing-software.cloud-infrastructure-engineering.metallb.address-allocation-model
name: address-allocation-model
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, address-allocation, ip-pool, rfc1918, loadbalancer, bare-metal, kubernetes]
level: intro
status: docs-checked
description: "How MetalLB allocates LoadBalancer IPs from operator-supplied pools, where pool addresses come from, and what happens to assigned IPs when a pool is edited or removed."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Address allocation model

MetalLB lets Kubernetes Services of `type: LoadBalancer` work off-cloud. It has two jobs that work together: address allocation and external announcement (see `computing-software.cloud-infrastructure-engineering.metallb.choosing-l2-or-bgp`).

- MetalLB cannot create IPs. You must give it pools, and it only hands out IPs from configured pools.
- Where pools come from:
  - Colocation: lease a block (the docs' example is a /26, 64 addresses).
  - Private cluster serving a LAN: pick RFC1918 ranges. They are free and work as long as services are only for your LAN.
  - Both at once: define as many pools as you like; MetalLB does not care what kind of address it gets.
- Once IPs are assigned to a Service, MetalLB tries to keep them assigned to it.
- If those IPs leave the pools (the `IPAddressPool` they came from is deleted or edited), MetalLB assigns another set to the service when one is available. Note the stale-config behaviour in `computing-software.cloud-infrastructure-engineering.metallb.stale-config-changing-service-ip`.

## Checked

2026-11-04. Confirmed against the MetalLB Concepts page (address allocation section): pools required, /26 = 64 addresses example, RFC1918 option, any number of pools, reassignment on pool deletion or edit. Removed the generic Verify and Gotcha lines, which the page does not state.

Method: documentation only; no commands were run.
