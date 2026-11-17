---
id: computing-software.networking-hardware-and-wireless.switching-routing-hardware.sw-qos-trust-boundary-and-queueing
name: sw-qos-trust-boundary-and-queueing
category: computing-software
field: networking-hardware-and-wireless
product: switching-routing-hardware
tags: [qos-trust-boundary, switch-queueing, qos-policing-shaping]
level: advanced
status: draft
description: "Set the QoS trust boundary, map DSCP/CoS to queues, apply policing at the edge and verify drops per queue."
sources:
  - https://www.rfc-editor.org/rfc/rfc4594
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Switch QoS

- Trust DSCP/CoS only from devices you control (e.g. IP phones); re-mark or zero out marks from untrusted endpoints.
- Map classes to queues: priority queue for voice (with a policer so it cannot starve others), assured forwarding queues for business apps, default and scavenger.
- Policing drops or re-marks excess traffic; shaping buffers it. Apply policing at the edge, shaping at WAN handoffs.
- QoS matters only where there is congestion: check uplink utilisation first.
- DSCP values per RFC 4594 guidance (e.g. EF for voice, AF41 for interactive video), adapt to your policy.

## Verify
- [ ] Per-queue counters show voice in the priority queue with no drops under load.
