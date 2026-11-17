---
id: computing-software.systems-network-administration.network-design.wan-circuit-sla-and-handoff
name: wan-circuit-sla-and-handoff
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, wan, circuit-sla, handoff, demarcation, mtu, availability, service-credits]
level: practitioner
status: draft
description: "Specify and accept a WAN or internet circuit: SLA terms (availability, latency, MTTR), handoff type and MTU, demarcation, diversity proof, and acceptance testing."
sources:
  - https://www.mef.net/service-standards/
  - https://www.rfc-editor.org/rfc/rfc2544
  - https://www.itu.int/rec/T-REC-Y.1564
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# WAN circuit SLAs and handoffs

## What to put in the order
- **Bandwidth** committed (CIR) vs burst, symmetric or not.
- **Handoff:** media (1000BASE-LX, 10GBASE-LR, copper), connector, VLAN tagged or untagged,
  autonegotiation or fixed speed, **MTU** (1500 vs jumbo; needed for MPLS/VXLAN over it), IPv4
  and IPv6 addressing, routing (static or BGP with ASN/communities).
- **Demarcation:** where the provider's responsibility ends (NTE, patch panel position) and
  who supplies the NTE power.
- **Diversity:** separate building entries, ducts and exchange/PoP, documented with route
  maps, if you are buying it for resilience. Without proof, assume shared fate.

## SLA terms that matter
| Term | Typical | Watch out |
|---|---|---|
| Availability | 99.9-99.99% monthly | excludes planned maintenance; how is it measured |
| Latency / jitter / loss | per class, PoP to PoP | measured on provider core, not your path |
| MTTR / time to restore | 4-8 h | business hours only? |
| Service credits | % of monthly fee | the only remedy, usually tiny: design for redundancy, not credits |

99.9% monthly allows ~43 min outage; 99.99% ~4.3 min.

## Acceptance test before cut-over
- Throughput at CIR both directions (iperf3/RFC 2544 or Y.1564 test from the provider).
- MTU: `ping -M do -s 1472` (Linux) / `ping -f -l 1472` (Windows) across the circuit, and the
  jumbo size if ordered.
- Latency/jitter baseline recorded; BGP session and failover test.
- Interface error counters clean for 24 h.
Record the provider circuit ID, NOC contact and escalation path in documentation.

## Verify
- [ ] Order spec matches what was delivered (handoff, MTU, addressing); acceptance results archived; SLA monitoring in place.
