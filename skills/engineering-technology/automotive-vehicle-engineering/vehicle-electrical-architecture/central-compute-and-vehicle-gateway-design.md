---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.central-compute-and-vehicle-gateway-design
name: central-compute-and-vehicle-gateway-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [vehicle-gateway, central-compute, gateway, high-performance-computer, hpc, pdu-router, firewall, doip-routing, time-sync, gptp, hypervisor, zonal-architecture]
level: practitioner
status: gated
description: "Design the central compute and vehicle gateway: routing across CAN, LIN and Ethernet, diagnostic and OTA roles, firewalling, time sync, and safety partitioning."
sources:
  - "AUTOSAR Layered Software Architecture, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_EXP_LayeredSoftwareArchitecture.pdf)"
  - "ISO 13400 (DoIP); IEEE 802.1AS (time synchronisation); confirm current editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Central compute and vehicle gateway design

## 1. Roles
- **Routing:** forward signals or PDUs between CAN, CAN FD, LIN and Ethernet domains (signal gateway: re-pack signals; frame or PDU gateway: forward frames; AUTOSAR PduR does this in Classic).
- **Diagnostics:** route UDS requests from the OBD or Ethernet port to target ECUs (DoIP routing activation, then forwarding to CAN/LIN; ISO 13400 details (gated: unconfirmed, source is paywalled or blocked)).
- **Network management and wake:** coordinate sleep and wake across domains (see power moding).
- **Security enforcement:** firewall and intrusion detection between external-facing domains (telematics, infotainment, diagnostics port) and safety-critical networks; authentication of messages across zones.
- **Update master:** distribute software updates in OTA flows (see OTA update architecture).
- **Time distribution:** time master for gPTP (IEEE 802.1AS) on the Ethernet backbone (gated: unconfirmed, source is paywalled or blocked).

## 2. Central compute (vehicle computer)
High-performance SoC(s) running Linux, QNX or similar, often with a hypervisor hosting several guests (for example Adaptive AUTOSAR, infotainment, ADAS functions). Provide: network switch, multicore compute, hardware security module, storage, and reliable power with fallback. Choose between one central computer and a few domain computers based on safety, supplier and compute needs.

## 3. Design steps
1. List domains and their buses, signal and PDU counts, rates, latency limits (from the communication matrix).
2. Define routing tables: source, destination, rate adaptation, filtering, priority; identify signals that need gateway-introduced latency budgets (for example, add one cycle plus processing time).
3. Define queues, buffer sizes and what happens on overload (drop non-critical, keep critical).
4. Partition by criticality: safety-relevant routing in an ASIL-capable partition or dedicated safety MCU; non-safety traffic on a separate partition; ensure freedom from interference (see ECU consolidation).
5. Security: default deny, whitelists per route, rate limits, SecOC passing or re-authentication, logging.
6. Failure behaviour: gateway failure must not stop safety-critical local loops (keep ASIL D control loops within one domain or zone controller).

## 4. Verification
Latency measurement per route under full load, overload and fault tests, security penetration tests, diagnostic routing tests, sleep and wake tests, long-run stability.

## Verify
- [ ] Routing table with latency budgets signed by owners of both ends.
- [ ] Overload and failure behaviour specified and tested.
- [ ] Safety and security partitioning documented.
- [ ] Time sync accuracy measured where used.
