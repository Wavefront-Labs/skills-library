---
id: computing-software.cloud-infrastructure-engineering.cilium.l3-policy-methods-overview
name: l3-policy-methods-overview
category: computing-software
field: cloud-infrastructure-engineering
product: cilium
tags: [cilium, layer3, endpoints-based, cidr-based, entities, toservices]
level: intro
status: docs-checked
description: "Choose between Cilium L3 policy methods: endpoints, services, entities, nodes, CIDR and DNS, and why to prefer label-based over hardcoded IPs."
sources:
  - https://docs.cilium.io/en/stable/security/policy/layer3/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Layer 3 policy methods

L3 policy sets which endpoints may talk. Methods, in rough order of preference:
1. Endpoints based: both sides managed by Cilium with labels; no IPs in policy.
2. Services based: refer to Kubernetes Services by name or label, so backend IPs are not hardcoded even if the destination is not Cilium-managed.
3. Entities based: categories of peers such as host or world.
4. Node based: extension of `remote-node` with per-node identity.
5. CIDR based: for external services when the peer is not an endpoint; needs stable IPs or subnets, so last resort.
6. DNS based: names converted to IPs via the DNS proxy, sharing CIDR limitations. DNS TTLs are respected.

## Checked

2026-11-03. Claims were read against: https://docs.cilium.io/en/stable/security/policy/layer3/. 

Method: documentation only; no commands were run.
