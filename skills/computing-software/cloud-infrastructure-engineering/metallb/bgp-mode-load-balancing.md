---
id: computing-software.cloud-infrastructure-engineering.metallb.bgp-mode-load-balancing
name: bgp-mode-load-balancing
category: computing-software
field: cloud-infrastructure-engineering
product: metallb
tags: [metallb, bgp, ecmp, packet-hash, multipath, 3-tuple, 5-tuple, kube-proxy]
level: practitioner
status: docs-checked
description: "How MetalLB BGP mode spreads traffic: equal-cost routes, per-connection packet hashing, 3-tuple vs 5-tuple, and why more hash entropy is better."
sources:
  - https://raw.githubusercontent.com/metallb/metallb/main/website/content/concepts/bgp.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# BGP mode load balancing

Every node peers with your routers and advertises the service IPs. If routers support multipath, the routes are equal except for next hop, so routers use all next hops. After arrival, `kube-proxy` forwards to one pod.

Behaviour depends on router model/config, but commonly:
- Balancing is per connection, by packet hash. All packets of one TCP/UDP session go to one node; spreading happens only between connections.
- This is deliberate: splitting one connection across paths reorders packets, and Kubernetes on-node routing is not guaranteed consistent across nodes (two nodes might pick different pods for the same connection).

Hash options:
- 3-tuple: `(protocol, source-ip, dest-ip)`. All traffic between two IPs goes to one backend.
- 5-tuple: adds source and destination ports, so different connections from one client can spread out.
- Prefer more fields (more entropy) to approach even load and avoid hotspots.

Caveat: backend-set changes break connections; see `computing-software.cloud-infrastructure-engineering.metallb.bgp-connection-reset-mitigation`.

## Checked
2026-11-04. Confirmed against the MetalLB "MetalLB in BGP mode" page: multipath assumption, per-connection hashing, reasons, 3-tuple and 5-tuple definitions, entropy advice. Removed a router setup and verify line the page does not contain.
Method: documentation only; no commands were run.
