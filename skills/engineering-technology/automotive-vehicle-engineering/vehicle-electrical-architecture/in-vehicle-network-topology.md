---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.in-vehicle-network-topology
name: in-vehicle-network-topology
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [e-e-architecture, ee-architecture, in-vehicle-network, network-topology, can, can-fd, can-xl, lin, flexray, automotive-ethernet, 100base-t1, 1000base-t1, 10base-t1s, tsn, someip, zonal-architecture, domain-architecture, central-compute, gateway, ecu-partitioning, bus-load, worst-case-response-time, dbc, arxml, ldf, autosar, partial-networking, iso-11898, uds, iso-14229, doip, iso-13400, secoc, iso-21434, unece-r155, unece-r156, canoe, preevision, vehicle-networks, automotive-cybersecurity, lin-bus, dbc-files, domain-controller]
level: practitioner
status: gated
description: "Design a vehicle network: assign ECUs to CAN/CAN FD/LIN/Ethernet domains or zones, budget bus load and latency, and plan gateways, wake-up and diagnostics."
sources:
  - "CiA, CAN XL (https://www.can-cia.org/can-knowledge/can-xl) and CAN FD basic idea (https://www.can-cia.org/can-knowledge/can-fd-the-basic-idea)"
  - "Zephyr LIN documentation (https://docs.zephyrproject.org/latest/hardware/peripherals/lin.html)"
  - "ISO 11898-2:2016 (https://www.iso.org/standard/67244.html)"
  - "ISO 14229-1 UDS (https://www.iso.org/standard/72439.html); ISO 15765-4 (https://www.iso.org/standard/78384.html)"
licence: Apache-2.0
version: 5
updated: 2026-11-17
aliases: []
---

# In-vehicle network topology

**Goal:** a network where every signal arrives within its deadline with headroom for
growth, ECUs sleep and wake correctly, diagnostics and software updates reach everything,
and safety/security domains are separated — at the lowest harness cost.

## 1. Inventory the communication matrix first
List every signal: producer, consumers, size, period or event, deadline, ASIL, and
security need. Tools: Vector PREEvision or a spreadsheet exported to DBC (CAN), LDF (LIN)
or AUTOSAR ARXML. Topology decisions made before this matrix exists are guesses.

## 2. Pick the physical layer per traffic class
| Bus | Practical rate | Use |
|---|---|---|
| LIN | up to 20 kbit/s (19.2 kbit/s is a common rate), single commander/master | switches, mirrors, seat motors, sensors |
| CAN (classical) | 500 kbit/s typical (1 Mbit/s max) | body, chassis, powertrain control; OBD |
| CAN FD | arbitration up to 1 Mbit/s; data-phase rate limited by transceiver and topology (2 Mbit/s common, 5 Mbit/s with good topology (gated: unconfirmed, source is paywalled or blocked)) | most new control traffic, up to 64 data bytes |
| CAN XL | data phase 20 Mbit/s and higher (needs XL-capable transceivers), up to 2048 data bytes | emerging; check ECU/transceiver availability |
| 10BASE-T1S | 10 Mbit/s multidrop (gated: unconfirmed, source is paywalled or blocked) | CAN-replacement edge networks |
| 100BASE-T1 / 1000BASE-T1 | 100 Mbit/s / 1 Gbit/s point-to-point | backbone, cameras, ADAS, infotainment |
FlexRay remains in legacy chassis platforms but is rarely chosen for new designs.

## 3. Domain vs zonal
- **Domain:** ECUs grouped by function (powertrain, chassis, body, infotainment), each
  domain bus joined by a central gateway. Simple to reason about; harness follows function,
  so wires cross the car.
- **Zonal:** zone controllers at physical locations (front-left, rear, etc.) aggregate
  local I/O and LIN/CAN, connected by an Ethernet backbone to central compute. Cuts harness
  length and mass and simplifies power distribution, but needs time-sensitive Ethernet
  (TSN) or careful scheduling for control loops, and SOME/IP or similar service middleware.
Partition by: latency/determinism, ASIL (keep ASIL D loops short and redundant), bandwidth,
physical location, and who updates the software.

## 4. Bus load budget
```
load = Σ (frame_bits_i / period_i) / bitrate
```
A classical CAN 11-bit-ID frame with 8 data bytes is ~111 bits before stuffing, up to ~135
worst case (bit counts (gated: unconfirmed, source is paywalled or blocked)). Example on 500 kbit/s, assuming 125 bits per frame (between those two): 30 frames at 10 ms + 40 frames at 100 ms ≈
30·125/0.01 + 40·125/0.1 = 375 + 50 = 425 kbit/s → **85%** (computed; 111 bits per frame gives 377 kbit/s, 75%) — too high. Move the fast
traffic to CAN FD (or split the bus). Common practice: ≤ ~50% at start of production on
CAN to leave growth margin; check your OEM's rule. Then run **worst-case response-time
analysis** on the lowest-priority frames (the revised Davis et al. method, not the original
Tindell version) to prove deadlines — average load says nothing about the last frame.

## 5. Physical topology rules (CAN/CAN FD)
Linear bus with short stubs, 120 Ω termination at both ends (≈60 Ω measured between
CAN-H and CAN-L with power off). At 2 Mbit/s+ data phase, stubs and star points cause
ringing: keep stubs short, consider ringing-suppression transceivers, and simulate or
measure eye diagrams. Sample-point settings must match across all nodes.

## 6. Gateways, wake-up, diagnostics, security
- Gateway routing tables and latency per hop go in the timing budget.
- Wake-up and sleep: define wake sources, network management (AUTOSAR NM), and partial
  networking (selective wake-up is part of ISO 11898-2:2016) so unused ECUs stay asleep; budget key-off
  quiescent current per ECU against the 12 V battery's parked-life target.
- Diagnostics: UDS (ISO 14229) everywhere; DoIP (ISO 13400) for fast flashing; legislated
  OBD on CAN per ISO 15765-4 where required. Make sure OTA updates can reach every ECU.
- Security: separate safety-critical networks from externally connected ones behind
  firewalling gateways; authenticate critical messages (AUTOSAR SecOC); the process
  must satisfy ISO/SAE 21434 and UN R155/R156 where they apply.

## Verify
- [ ] Communication matrix complete with periods, deadlines, ASIL and security level.
- [ ] Each bus below its load limit at SOP with documented growth margin.
- [ ] Worst-case response times computed for the lowest-priority frames on every bus.
- [ ] Termination, stub lengths and CAN FD bit timing verified by measurement.
- [ ] Sleep/wake behaviour and key-off current tested over a full parked-life scenario.
- [ ] Every ECU reachable for diagnostics and flashing; security zones and gateway
      filters reviewed.
