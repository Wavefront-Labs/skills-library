---
id: computing-software.networking-hardware-and-wireless.sd-wan.sdwan-qos-and-traffic-engineering
name: sdwan-qos-and-traffic-engineering
category: computing-software
field: networking-hardware-and-wireless
product: sd-wan
tags: [sdwan-qos, sdwan-shaping, per-flow-load-balancing]
level: advanced
status: draft
description: "Shape per-transport to circuit rate, classify and queue by DSCP, and load-balance flows across links without reordering."
sources:
  - https://www.cisco.com/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SD-WAN QoS

- Shape egress to the real circuit rate (a bit under it) so queueing happens on the edge you control, not in the carrier.
- Classify by DSCP/application into queues (priority for voice, assured for business apps, best effort); keep marks consistent with the LAN.
- Per-flow (5-tuple) hashing keeps TCP in order; per-packet spraying can raise throughput but risks reordering.
- Carrier MPLS often honours DSCP; internet does not, so QoS applies only up to your edge.
- Reserve bandwidth for control traffic.

## Verify
- [ ] Under a saturating test, voice flows keep low jitter while bulk flows are throttled.
