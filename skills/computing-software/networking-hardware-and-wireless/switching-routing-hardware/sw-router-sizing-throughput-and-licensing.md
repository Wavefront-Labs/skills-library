---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-router-sizing-throughput-and-licensing
name: sw-router-sizing-throughput-and-licensing
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [router-throughput-sizing, branch-gateway-sizing, feature-licensing, sw-routing-platforms]
level: practitioner
status: draft
description: "Size WAN edge routers/gateways using throughput with IPsec, NAT, firewall and QoS enabled, and account for licences and tunnel counts."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Router sizing

- Datasheet throughput is usually unencrypted large-packet UDP; real numbers with IPsec, firewall/IPS, NAT, QoS and small packets are far lower. Use the vendor's "with services" figures, or test.
- Sum all traffic sources: user peak, backups, voice, cloud sync; plan 30-50 percent headroom (a common rule, tune by growth).
- Check limits beyond bandwidth: session count, tunnel count, routes, ACL size, and CPU for control plane at scale.
- Licences can gate throughput tiers and features; record the licence terms and renewal.
- Include power (PoE budget for APs on integrated switch ports), form factor and SFP/LTE modules.

## Verify
- [ ] A load test with the production feature set achieves target throughput while CPU stays under the headroom limit.
