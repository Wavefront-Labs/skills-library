---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.fuse-relay-and-power-distribution-unit-design
name: fuse-relay-and-power-distribution-unit-design
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [fuse-box, pdu, power-distribution-unit, fuse, relay, efuse, smart-fuse, high-side-switch, junction-box, power-distribution, iso-8820, battery-junction-box]
level: practitioner
status: gated
description: "Design low-voltage power distribution: fuse and relay boxes, electronic fuses, protection philosophy, fuse sizing, ground distribution, voltage drop and thermals."
sources:
  - "ISO 8820-3:2015 Road vehicles - Fuse-links - Part 3: Fuse-links with tabs (blade type) Type C (medium), Type E (high current) and Type F (miniature) (https://www.iso.org/standard/58088.html); a 2026 edition is listed at https://www.iso.org/standard/85282.html"
  - "Fuse and relay manufacturers' datasheets for time-current curves"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Fuse, relay and PDU design

## 1. Architecture
Battery positive goes first to a battery junction box or main fuse unit near the battery with large fuses or fusible links for main feeds; secondary distribution boxes (engine bay, cabin, rear) feed branch circuits. Ground distribution via grounding points on body with low resistance.

## 2. Protection philosophy
Fuses protect the wire (and the supply) from overcurrent faults (see wire sizing). Place the protection device at the supply end, as close to the power source as possible. Critical loads (steering, brakes, safety systems) should not share a fuse with comfort loads; redundant supply paths for safety-critical functions (dual feeds or dual batteries) per the safety concept. Document fuse and wire sizes in a circuit table.

## 3. Devices
- **Blade fuses** (ISO 8820-3: Type F miniature, Type C medium, Type E high current; the trade names mini, standard and maxi correspond roughly to these classes, confirm the mapping (gated: unconfirmed, source is paywalled or blocked)) and **cartridge or bolt-on high-current fuses** for larger feeds. Use time-current curves; slow-blow types for inrush loads (motors, lamps).
- **Relays** (mini relay standards (gated: unconfirmed, source is paywalled or blocked)) switch higher currents; consider contact ratings for inductive and lamp loads, coil suppression, and lifetime.
- **Smart power distribution (electronic fuses, eFuses; smart high-side switches):** MOSFET switches with current sensing, programmable trip curves (I2t emulation), diagnostics (open load, short, overtemperature), inrush control, remote reset and software configurable ratings; enable load shedding and power management. Use for body and zonal controllers, with hardware-limited short-circuit protection and a fallback.
- **Active/passive discharge and precharge** belong to HV systems (see precharge).

## 4. Sizing rules
Continuous load below a stated fraction of fuse rating (typically about 75-80% at room temperature (gated: unconfirmed, source is paywalled or blocked), less in hot boxes); fuse rating below the wire's thermal capability; check voltage drop across fuse and contacts (millivolts to tens of millivolts at rated current); account for cold crank current and inrush; coordinate upstream and downstream fuses so the one closest to the fault clears first.

## 5. Thermal and packaging
Heat dissipation in the box (fuses and relays warm up); keep margin to plastic and ambient limits; locate away from water and provide drainage; serviceability and fuse puller access; labelling.

## 6. Verification
Fault tests (short circuit at various points), thermal rise at maximum load, load profile with inrush, electronic fuse trip curve checks, EMC of switching, durability (vibration, humidity), service fuse replacement test.

## Verify
- [ ] Fuse table lists load, wire gauge, fuse rating and derating.
- [ ] Safety-critical loads have independent protection and supply per concept.
- [ ] Thermal rise and voltage drop within limits at worst case.
- [ ] Short-circuit tests prove the first device in line clears.
