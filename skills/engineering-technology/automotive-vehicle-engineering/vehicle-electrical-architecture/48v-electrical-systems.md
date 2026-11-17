---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.48v-electrical-systems
name: 48v-electrical-systems
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [48v-system, 48-volt, mild-hybrid, bsg, belt-starter-generator, 48v-battery, dcdc-48-12, iso-21780, lv-148, voltage-class-a, arcing, power-distribution]
level: practitioner
status: gated
description: "Design a 48 V mild-hybrid electrical subsystem: architecture, belt starter generator, 48 V battery and DC-DC, loads that benefit, voltage class rules and arc safety."
sources:
  - "ISO 21780 (48 V supply voltage electrical requirements and tests) and OEM specs such as LV 148 (a joint Audi/BMW/Daimler/Porsche/VW 48 V component test standard per secondary sources (gated: unconfirmed, source is paywalled or blocked)); confirm editions"
  - "Navet and Simonot-Lion, Automotive Embedded Systems Handbook (chapter list)"
  - "Ehsani et al., Modern Electric Hybrid Electric and Fuel Cell Vehicles (chapter list)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# 48 V electrical systems

## 1. What and why
A 48 V (nominal) subsystem alongside the 12 V net supports mild hybrid functions (belt or crank-mounted starter generator for torque assist, recuperation, engine start-stop and coasting) and high-power loads, with lower current than 12 V for the same power and without the full high-voltage safety regime. Typical components: starter generator (power commonly in the order of 10-20 kW (gated: unconfirmed, source is paywalled or blocked)), 48 V lithium-ion battery (a few hundred watt-hours to about 1 kWh (gated: unconfirmed, source is paywalled or blocked)), 48-to-12 V DC-DC converter, and 48 V loads.

## 2. Voltage ranges and class
The 48 V net operates over a window around the nominal (confirm in ISO 21780 and the OEM specification: normal operation window and transient limits). Systems at or below 60 V DC are generally treated as low voltage class (touch-safe) under road-vehicle electrical safety standards (for example ISO 6469-3 and UN R100 voltage class definitions (gated: unconfirmed, source is paywalled or blocked)); confirm how your market classifies it and whether any shock protection requirements still apply.

## 3. Architecture choices
P0 (belt starter generator on the engine front), P1, P2 (between engine and transmission), P4 (rear axle) with 48 V; with or without 12 V battery; electric turbocharger or supercharger, electric heated catalyst, active roll stabilisation, electric air conditioning compressors, and high-power steering as 48 V loads. The 12 V net remains for legacy loads via DC-DC (bidirectional or unidirectional).

## 4. Design points
- **Protection:** DC fuses and switches rated for 48 V; DC arcs are sustained more readily at 48 V than at 12 V, so use connectors, relays and fuses rated for the voltage and have breaking capability (use DC arc-rated devices).
- **Battery management:** cell monitoring, balancing, temperature control, current limits (see BMS topics); high power cycling (recuperation) needs power-oriented cells.
- **Wiring:** colour coding and labelling per OEM practice; wire gauge per current at 48 V; EMC from switching converters and machines.
- **Isolation:** keep the 48 V net isolated from chassis (isolated or monitored) as per specification; consider isolation monitoring even if not mandated.
- **Failure behaviour:** sudden loss of 48 V assist must be handled by the powertrain controller without hazards.

## 5. Verification
Net simulation (loads, regeneration, battery SoC), electrical transient tests (load dump equivalents, short circuits, voltage dips) per ISO 21780 style, thermal and EMC tests, safety analysis.

## Verify
- [ ] Voltage window and class confirmed against current standards and the market.
- [ ] DC arc-rated protection and connectors specified.
- [ ] Battery and DC-DC sized to the recuperation and assist profile.
- [ ] Transient and failure cases tested.
