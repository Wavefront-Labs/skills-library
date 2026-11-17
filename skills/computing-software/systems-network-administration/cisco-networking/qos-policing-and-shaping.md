---
id: computing-software.systems-network-administration.cisco-networking.qos-policing-and-shaping
name: qos-policing-and-shaping
category: computing-software
field: systems-network-administration
product: cisco-networking
tags: [cisco, cisco-ios, qos, quality-of-service, policing, shaping, shape-average, police, cir, bc, be, hierarchical-qos, hqos, sub-rate-circuit, token-bucket, conform-action, exceed-action, violate-action]
level: practitioner
status: draft
description: "Pick policing or shaping and configure both on IOS: token-bucket terms, police conform/exceed actions, shape average to a sub-rate circuit with a nested queuing policy (HQoS)."
sources:
  - https://www.cisco.com/c/en/us/support/docs/quality-of-service-qos/qos-policing/19645-policevsshape.html
  - https://www.cisco.com/c/en/us/td/docs/ios-xml/ios/qos_plcshp/configuration/xe-16/qos-plcshp-xe-16-book.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Policing vs shaping

| | Policing | Shaping |
|---|---|---|
| Excess traffic | dropped or re-marked immediately | buffered and sent later |
| Direction | ingress or egress | egress only |
| Effect on TCP | drops cause retransmits, sawtooth throughput | smooth, adds delay |
| Typical use | provider enforcing CIR, rate-limiting a class, scavenger caps | customer conforming to provider CIR |

Token bucket terms: **CIR** (committed rate, bits/s), **Bc** (committed burst, bits per Tc
interval), **Be** (excess burst). Tc = Bc / CIR. Leave Bc defaults unless you know why; too-small
bursts hurt TCP.

## Policing
```
policy-map POLICE-GUEST
 class class-default
  police cir 20000000 conform-action transmit exceed-action drop
interface Vlan90
 service-policy input POLICE-GUEST
```
Two-colour (conform/exceed) or three-colour (`police cir X pir Y conform-action transmit
exceed-action set-dscp-transmit af12 violate-action drop`) for marking down instead of dropping.

## Shaping to a sub-rate circuit (HQoS)
A 1 Gb/s Ethernet handoff with a 100 Mb/s contracted rate: shape to the CIR so congestion (and
queuing decisions) happen on your router, not in the provider's policer.
```
policy-map SHAPE-100M
 class class-default
  shape average 95000000          ! a bit under the CIR to absorb L2 overhead differences
  service-policy WAN-OUT          ! nested child queuing policy (LLQ/CBWFQ)
interface GigabitEthernet0/0/0
 service-policy output SHAPE-100M
```
Shaper rates on IOS count Layer 3 + Layer 2 header bytes depending on platform; the provider may
police on a different basis. 95% of CIR is a common safe margin; tune with testing.

## Read counters
```
show policy-map interface Gi0/0/0 output
! shaping: target/byte limit, queue depth, "shape (average) cir", child class drops
! policing: conformed/exceeded packets and bps
```

## Gotchas
- Shaping only on egress; to limit inbound downloads, shape egress on the far side or police
  ingress (TCP backs off on drops).
- Policers on voice are dangerous: one burst exceeding Bc drops RTP. Use LLQ instead.
- A shaper on a Port-channel or subinterface may not be supported on every platform.

## Verify
- [ ] iperf3 at above-CIR rate shows output limited to the shape rate with queuing (not drops) at the router.
- [ ] Provider-side drop counters (if visible) stop increasing.
- [ ] Policed class conform/exceed counters match the expected rate.
