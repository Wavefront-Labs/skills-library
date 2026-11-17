---
id: computing-software.systems-network-administration.network-design.network-packet-brokers
name: network-packet-brokers
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, monitoring, packet-broker, network-tap, span, visibility-fabric]
level: practitioner
status: draft
description: "Design a visibility layer with TAPs and network packet brokers: TAP vs SPAN, aggregation, filtering, deduplication, slicing, load balancing to tools and decryption."
sources:
  - https://www.keysight.com/us/en/products/network-visibility/network-packet-brokers.html
  - https://www.cisco.com/c/en/us/products/collateral/switches/nexus-3000-series-switches/white-paper-c11-737398.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network packet brokers

## TAP vs SPAN
| | TAP | SPAN / mirror port |
|---|---|---|
| Fidelity | every frame incl. errors, no drops | drops under oversubscription, may reorder, no L1 errors |
| Impact | passive optical TAPs need no power; inline | consumes switch resources, limited sessions |
| Cost | hardware per link | free |
Use TAPs on critical links (internet edge, DC core); SPAN for ad-hoc.

## What an NPB does
Sits between TAP/SPAN sources and tools (IDS, NDR, APM, packet recorders):
- **Aggregation** of many links into a tool port (watch oversubscription).
- **Filtering** by VLAN, IP, port so each tool gets only what it needs.
- **Load balancing** across tool instances with flow-aware hashing (keep both directions of a
  session on the same tool).
- **Deduplication** when the same packet is seen on several taps.
- **Packet slicing** (keep headers only) for metadata tools, saving bandwidth/storage.
- **Header stripping** (VXLAN, MPLS, VN-tags) for tools that cannot parse them.
- **TLS decryption** (some models) and timestamping.

## Design
- Size tool ports for peak aggregate, not average; full-duplex 10G link = up to 20G of tap output.
- Inline bypass for inline tools (IPS) with heartbeat fail-open/closed policy.
- Budget-conscious alternative: switch-based visibility fabric (Nexus Data Broker, Arista
  DANZ) using merchant silicon.

## Verify
- [ ] Each tool receives only its intended traffic with no drops at peak (NPB port counters), and both directions of sessions arrive at the same tool instance.
