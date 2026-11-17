---
id: computing-software.networking-hardware-and-wireless.arista-eos.qos
name: qos
category: computing-software
field: networking-hardware-and-wireless
product: arista-eos
tags: [arista-eos, qos, traffic-class, policy-map, dscp-trust]
level: practitioner
status: draft
description: "Configure EOS QoS trust, DSCP-to-traffic-class mapping, policy-maps and queue shaping."
sources: ["https://www.arista.com/en/support/product-documentation", "https://www.arista.com/en/um-eos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QoS and traffic classes
Goal: protect priority traffic.

```
qos rewrite dscp
interface Ethernet1
   qos trust dscp
class-map type qos match-any VOICE
   match dscp ef
policy-map type quality-of-service PM-IN
   class VOICE
      set traffic-class 5
interface Ethernet2
   service-policy type qos input PM-IN
   tx-queue 5
      priority strict
```

```
show qos interfaces Ethernet1
show qos maps
show interfaces Ethernet1 counters queue
```

- Platform differences are significant (7050, 7280, 7500, 720): confirm syntax in the matching QoS guide.
- DSCP to traffic-class maps are global (`qos map dscp ... to traffic-class ...`).

Gotcha: untrusted ports reset DSCP to default. Use `qos trust dscp` only on ports where you trust the marking.

Operational tip: validate QoS with traffic generation and read per-queue drop counters. Document trust boundaries, and avoid enabling features whose hardware resources you have not checked on the platform. Capture a baseline of queue counters before the change so you can show improvement and spot a queue that is unexpectedly starved afterwards.

## Verify
- `show interfaces counters queue` shows packets in the expected tx-queue under load.
