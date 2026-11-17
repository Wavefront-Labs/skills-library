---
id: computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-rp-filter
name: troubleshoot-rp-filter
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, rp-filter, asymmetric-routing, reverse-path-filtering, static-routes, source-based-routing, frr-k8s]
level: advanced
status: docs-checked
description: "Fix MetalLB services dropped by Linux reverse path filtering when packets arrive on a non-default-gateway interface: static routes, FRR-K8s route learning, source routing."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/troubleshooting/_index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Asymmetric return path and rp_filter

Reverse path filtering (`rp_filter`) drops packets arriving on an interface when the node has no route back to the source through that interface. It is common with BGP (less so with L2) because MetalLB advertises routes to the service but the nodes do not learn how to reach the clients.

Typical pattern:
- A client in a different subnet reaches the MetalLB-exposed service.
- Packets reach the node on an interface other than the default gateway one.
- The node has no route to the client via that interface, so, depending on the interface's `rp_filter` value, packets are dropped.

Fixes from the docs:
1. Add static routes to your nodes.
2. Use the FRR-K8s variant so your fabric sends those routes to the nodes (`computing-software.cloud-infrastructure-engineering.metallb.frr-k8s-configuration-merge` shows receiving prefixes).
3. Use source-based routing to steer replies out the right interface. The metallb-node-route-agent project does this (not affiliated with MetalLB).

Related symptoms: `computing-software.cloud-infrastructure-engineering.metallb.troubleshoot-intermittent-traffic`.

## Checked
2026-11-04. Confirmed against the MetalLB Troubleshooting page, "MetalLB and asymmetric return path": definition, BGP versus L2 commonness, the three-step pattern and the three fixes. Removed an invented sysctl check and a remark about disabling rp_filter that the page does not make.
Method: documentation only; no commands were run.
