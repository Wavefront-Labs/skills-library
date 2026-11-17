---
id: computing-software.cybersecurity-defensive.security-architecture.power-resilience
name: power-resilience
category: computing-software
field: cybersecurity-defensive
product: security-architecture
tags: [power-resilience, ups, generator, pdu, data-centre-power, runtime-calculation, graceful-shutdown]
level: practitioner
status: draft
description: "Design power resilience for server rooms and sites: UPS sizing and runtime, generator transfer, dual-corded A/B feeds, graceful shutdown automation and maintenance testing."
sources: ["https://csrc.nist.gov/pubs/sp/800/34/r1/upd1/final", "https://uptimeinstitute.com/tiers", "https://networkupstools.org/docs/user-manual.chunked/index.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Power resilience (UPS and generators)

## Chain
Utility -> automatic transfer switch (ATS) -> generator backup -> UPS (bridges the 10-60 s before
generator takes load, and conditions power) -> A and B PDUs -> dual-corded equipment.

## Sizing
- Measure real load (PDU readings) in watts; size UPS for load x 1.25 growth, keeping it under ~80% capacity.
- Runtime: at least the generator start/transfer time plus margin (minimum 10-15 minutes), or enough to shut down gracefully if there is no generator.
- Batteries degrade: plan replacement every 3-5 years (VRLA) and run calibration tests.

## A/B feeds
- Each PDU on a different UPS/circuit; load each side under 50% so one side can carry everything.
- Single-corded devices behind an automatic transfer switch, or accept them as single points of failure.

## Graceful shutdown
Network UPS Tools (NUT) or vendor agents (APC PowerChute, Eaton IPM) trigger ordered shutdown:
```
# /etc/nut/upsmon.conf on each host
MONITOR ups1@nut-server 1 monuser <secret> secondary
SHUTDOWNCMD "/sbin/shutdown -h +0"
```
Order: application servers, then databases, then storage, hypervisors last; set power-on order in BIOS/iLO.

## Testing
- Monthly generator run under load; annual full transfer test (pull utility).
- UPS self-test monthly; alarm (SNMP traps) to the NOC.

## Gotchas
- Batteries pass a self-test yet fail under full load; do load-bank tests.
- Fuel: contract for refuelling and test fuel quality; diesel degrades.
- The network gear needed to send the shutdown signal must itself be on UPS.

## Verify
- [ ] Last generator transfer test passed under load.
- [ ] Shutdown automation tested in a maintenance window.
- [ ] Each PDU side below 50% load.
