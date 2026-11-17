---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.ecu-consolidation-trade-offs
name: ecu-consolidation-trade-offs
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [ecu-consolidation, ecu-count, function-allocation, mixed-criticality, freedom-from-interference, supplier-integration, single-point-of-failure, domain-controller, zonal-architecture, centralisation]
level: practitioner
status: gated
description: "Decide which functions to consolidate onto fewer ECUs: cost and harness benefits versus single points of failure, mixed-criticality interference, supplier and update trade-offs."
sources:
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
  - "ISO 26262 parts 1-12 (confirm edition)"
  - "AUTOSAR specifications overview (https://www.autosar.org); confirm release and documents there"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ECU consolidation trade-offs

## 1. Why consolidate
Fewer boxes means fewer housings, connectors and harness, simpler production, shared compute and memory, easier software updates, and lower weight. Many OEMs move toward domain, zonal and central computers (see network topology and zonal architecture skills).

## 2. Costs and risks
- **Single point of failure:** one failed unit takes several functions with it; define fail-operational needs for safety functions.
- **Mixed criticality:** combining ASIL-rated and QM software requires freedom from interference (memory protection, timing protection, safe communications) as in ISO 26262 guidance on freedom from interference (part and annex numbers (gated: unconfirmed, source is paywalled or blocked)); otherwise everything inherits the highest ASIL, raising cost.
- **Thermal and power:** concentrated heat and current; package space and cooling.
- **Supplier and IP:** the integrator now owns integration of third-party software; define interfaces and responsibilities.
- **Variants and lifecycle:** high-end and low-end vehicles may need different compute levels; software variants multiply.
- **Development independence:** schedule coupling: a delay in one function holds up the rest; branching and release strategy become critical.
- **Testing:** more integration effort.

## 3. Decision method
For each function or cluster, score: criticality (ASIL), real-time constraint, physical location and I/O, compute need, update frequency, supplier source. Keep together functions that share signals, I/O location, or lifecycle; keep apart those with different ASIL, cycle time or supplier unless an isolation mechanism is available. Quantify: cost per unit with and without consolidation (hardware, harness, assembly), weight, software effort.

## 4. Typical patterns
Zone controllers consolidating I/O and local body functions; domain controllers consolidating chassis or ADAS; centralised vehicle computer for non-safety services and orchestration; safety MCU kept separate for ASIL D chassis functions.

## Verify
- [ ] Functions allocated with ASIL and timing recorded per allocation.
- [ ] Isolation mechanism (hypervisor, MPU, safe scheduler) named for each mixed-criticality ECU.
- [ ] Failure of each consolidated unit analysed for system effect.
- [ ] Cost, weight and effort trade-off documented.
