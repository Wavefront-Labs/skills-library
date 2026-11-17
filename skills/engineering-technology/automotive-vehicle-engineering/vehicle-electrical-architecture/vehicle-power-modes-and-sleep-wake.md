---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.vehicle-power-modes-and-sleep-wake
name: vehicle-power-modes-and-sleep-wake
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [power-modes, power-moding, sleep-wake, network-management, partial-networking, wake-up, bus-sleep, autosar-nm, ghost-wake, vehicle-mode-manager, power-distribution]
level: practitioner
status: verified
description: "Define vehicle power modes and the sleep and wake logic: states, wake sources, network management and partial networking, ownership, and tests for ghost wake-ups."
sources:
  - "AUTOSAR Specification of CAN Network Management, R22-11 (https://www.autosar.org/fileadmin/standards/R22-11/CP/AUTOSAR_SWS_CANNetworkManagement.pdf)"
  - "ISO 11898-2:2016 (https://www.iso.org/standard/67244.html); ISO 11898-6:2013 (https://www.iso.org/standard/59165.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Vehicle power modes and sleep/wake

## 1. State model
Define a small set of vehicle power states and the transitions between them, owned by one entity (for example a body or vehicle mode manager) and distributed to all ECUs:
- **Parked / sleep:** most ECUs off or in lowest-current sleep.
- **Standby / convenience:** door unlock, interior lights, remote functions.
- **Accessory / ignition on:** loads partially or fully powered.
- **Ready / drive:** propulsion enabled (EVs: HV contactors closed).
- **Charging:** on-board charger and thermal management active.
- **Remote or scheduled activity:** pre-conditioning, OTA, telematics wake.
Each ECU has a mode matrix: in which vehicle states it runs, what it must do before sleeping, and its maximum wake time.

## 2. Wake sources
Hardwired wake lines (door contact, ignition, brake switch), CAN or LIN bus wake-up patterns, key fob or phone-as-key receivers, telematics, charger plug-in, real-time clock, and sensors. Document every source per ECU with debounce time and what is allowed to wake the whole network versus only a node.

## 3. Network management
AUTOSAR network management (NM) (and OEM variants) coordinates bus sleep: each node keeps the network awake while it needs communication; when all release, the network goes through ready-sleep and prepare-bus-sleep to bus-sleep after timeouts. Set timeouts to allow late messages and diagnostics without wasting current. **Partial networking** (selective wake-up, selective wake-up is specified in ISO 11898-2:2016, formerly ISO 11898-6) lets groups of ECUs sleep while others communicate; define cluster membership and wake-up frames.

## 4. Design rules
- A single owner per wake request and defined handshake for sleep.
- Avoid periodic wake-ups unless necessary, with a bounded duty cycle.
- Define behaviour on faults: stuck wake line, NM bus-off, a node that refuses to sleep (watchdog on network awake time).
- Include diagnostics: log reason of last wake.

## 5. Verification
State transition tests with a bus recorder: each wake source, sleep timing, time to sleep, currents during each step, and **ghost wake** hunts (unexplained awake periods) over several days on a parked vehicle; temperature extremes; low battery behaviour (reduce activity).

## Verify
- [ ] Power mode state machine and ECU mode matrix documented and agreed.
- [ ] Every wake source listed with owner and debounce.
- [ ] NM timeouts set and tested; partial network clusters defined if used.
- [ ] Parked tests show no unexplained wake-ups.
