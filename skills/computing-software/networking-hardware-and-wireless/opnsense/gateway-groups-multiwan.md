---
id: computing-software.networking-hardware-and-wireless.opnsense.gateway-groups-multiwan
name: gateway-groups-multiwan
category: computing-software
field: networking-hardware-and-wireless
product: opnsense
tags: [multiwan, gateway-groups, failover, load-balancing, trigger-level]
level: practitioner
status: docs-checked
description: "Gateway groups and Multi WAN on OPNsense: tiers, trigger levels, pool options, failover, load balancing and the dynamic-gateway limitation."
sources: ["https://docs.opnsense.org/manual/multiwan.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gateway groups and multi-WAN

Multi-WAN on OPNsense uses policy based (source) routing and depends on the firewall rules: a rule selects a gateway or gateway group, so traffic leaves via the chosen path. Limitation: gateways without an address (interfaces using Dynamic gateway policy) cannot be put in a group, because the firewall needs an address of the right family on the interface.

Group concepts:
- Gateway Priority (tier): numbered from 1, lower means more important. When no usable gateway remains in a tier, the next tier is used. OPNsense offers 5 tiers, each holding multiple gateways.
- Trigger Level: when a gateway in the tier counts as offline: fully down, packet loss, or increased latency.
- Pool Options: normally left at default; adjusts source stickiness per group.

Common designs:
- WAN failover: traffic uses the primary ISP, moves to the next available WAN when connectivity is lost or latency is bad, and returns to the primary when it fully recovers. Put primary and backup in different tiers.
- Load balancing: put two or more gateways in the same tier; each receives a portion of traffic, equal or weighted, adding bandwidth or lowering per-ISP load.
- Combined: several WANs in tier 1 for balancing and one or more in a lower tier for failover.

The step-by-step build, including firewall rules that use the group, is in the Multi WAN how-to.

## Checked

2026-11-03. Confirmed against the OPNsense Gateway groups / Multi WAN manual page: policy based routing, the dynamic gateway limitation, tiers, trigger level, pool options, failover and balancing roles, five tiers. Nothing removed.

Method: documentation only; no commands were run.
