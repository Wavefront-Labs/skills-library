---
id: computing-software.systems-network-administration.network-design.qos-class-models
name: qos-class-models
category: computing-software
field: systems-network-administration
product: network-design
tags: [qos-design, qos-class-model, dscp-plan, rfc4594, bandwidth-allocation, queuing-design]
level: practitioner
status: draft
description: "Choose a 4, 8 or 12-class QoS model, map RFC 4594 classes to DSCP and queues, collapse classes for WAN and wireless, and allocate bandwidth per queue."
sources:
  - https://www.rfc-editor.org/rfc/rfc4594
  - https://www.cisco.com/c/en/us/td/docs/solutions/Enterprise/Video/qosmrn.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# QoS class models

Marking can be rich (12 classes) at the edge while queues are few (4-8). The model maps one to the
other consistently everywhere.

## 12-class (RFC 4594) marking at the edge
| Class | DSCP |
|---|---|
| Network control | CS6 |
| VoIP telephony | EF |
| Broadcast video | CS5 |
| Real-time interactive | CS4 |
| Multimedia conferencing | AF41/42/43 |
| Multimedia streaming | AF31/32/33 |
| Signalling | CS3 |
| Ops/admin/management (OAM) | CS2 |
| Transactional data | AF21/22/23 |
| Bulk data | AF11/12/13 |
| Best effort | DF (0) |
| Scavenger | CS1 (or LE, DSCP 1, RFC 8622) |

## Collapsing into fewer queues
| 8-class queue | Members | Typical allocation |
|---|---|---|
| Priority (LLQ) | EF (+ CS5, CS4 if no separate video PQ) | <= 33 % of link |
| Interactive video | AF4x, CS4 | 15-20 % |
| Streaming | AF3x, CS5 | 10 % |
| Network control | CS6, CS7 | 5 % |
| Signalling/OAM | CS3, CS2 | 2-5 % |
| Transactional | AF2x | 10 % |
| Bulk | AF1x | 5 % |
| Scavenger | CS1 | 1 % |
| Default | DF | 25 % (remainder) |

4-class WAN model: Realtime (EF, CS4/AF4x), Critical data (CS6, CS3, AF2x, AF3x), Best effort (DF),
Scavenger (CS1). Use when the provider sells 4-6 classes.

## Rules of thumb
- Keep total priority (strict) traffic at or below ~33 % so data is never starved.
- Best effort keeps at least 25 % (most traffic is there).
- Scavenger gets a floor, not zero, so it still drains.
- Map consistently: wired access, distribution, WAN edge, wireless (WMM) and provider classes all
  derive from the same table; document it once.

## Verify
- [ ] Each device's queuing policy implements the same table, and `show policy-map interface`
  counters during peak show realtime queues with zero drops.
