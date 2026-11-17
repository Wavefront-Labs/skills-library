---
id: engineering-technology.automotive-vehicle-engineering.vehicle-electrical-architecture.esd-and-electrical-transient-immunity
name: esd-and-electrical-transient-immunity
category: engineering-technology
field: automotive-vehicle-engineering
product: vehicle-electrical-architecture
tags: [transient-immunity, esd, iso-10605, iso-7637-2, iso-16750-2, load-dump, reverse-battery, jump-start, tvs-diode, surge-protection, functional-status-classes]
level: practitioner
status: gated
description: "Protect automotive electronics from ESD and supply transients: ISO 10605, ISO 7637-2 and ISO 16750-2 pulses, load dump, reverse battery, and protection circuit design."
sources:
  - "ISO 7637-2:2011 (https://www.iso.org/standard/50925.html)"
  - "ISO 16750-2:2023 (https://www.iso.org/standard/76119.html)"
  - "ISO 10605:2023 (https://www.iso.org/standard/79094.html)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# ESD and electrical transient immunity

## 1. Threats
- **ESD** from occupants and service (contact and air discharge) to switches, connectors and exposed electronics.
- **Supply-line transients:** inductive load switching spikes, relay and motor bounce, **load dump** (battery disconnection with the alternator running), starter dips, ignition noise.
- **Over/under-voltage and polarity:** jump start (typically up to 24 V for a defined time for 12 V nets (gated: unconfirmed, source is paywalled or blocked)), reverse battery connection, superimposed ripple, ground shifts.
- **Coupled transients** onto signal lines.

## 2. Test standards (confirm editions and levels)
- **ISO 10605** for ESD (contact and air discharge with specified network values, powered and unpowered tests, packaging and handling; 2023 edition 3); levels (kV) come from OEM specs.
- **ISO 7637-2** pulses for supply-line transients on 12 V and 24 V systems, and **ISO 16750-2** ("Road vehicles - Environmental conditions and testing for electrical and electronic equipment - Part 2: Electrical loads", 2023 edition) for the electrical loads on equipment, including load dump, starting profiles, superimposed alternating voltage, reverse polarity and slow voltage ramps (list of load cases (gated: unconfirmed, source is paywalled or blocked)). OEM specifications commonly add or modify levels. Use the functional performance status classes from the standard to state required behaviour (for example normal function, self-recovery, or no damage).

## 3. Protection design
- **Reverse battery:** series diode (voltage drop and loss), P-channel or ideal-diode MOSFET controllers (lower loss).
- **Load dump and spikes:** TVS diodes sized for the standard's pulse energy (check peak pulse power and clamp voltage against the downstream device's maximum rating), varistors, input pi-filters; regulators with wide input range (rated for the clamp voltage).
- **Cranking dips:** supply must keep microcontrollers alive during voltage sags: bulk capacitance, boost stage or supervisor, brown-out reset behaviour.
- **ESD:** TVS arrays at connector pins, series resistors, ferrite beads, creepage and grounded shields; PCB layout with short paths to chassis ground.
- **Inductive loads:** flyback diode or active clamp near the load.
- **Ground and signal:** ratings of I/O pins to transients, series current limiting.

## 4. Test plan
Test all supply, ground and signal ports per the spec in each defined ECU mode (sleep, run, active outputs). Record behaviour class; run repeated pulses; check functional recovery and any latent damage (parameter drift) afterwards. Combine with thermal extremes.

## Verify
- [ ] Applicable pulses and ESD levels listed per port from the OEM spec.
- [ ] Protection components rated for pulse energy with margin.
- [ ] Brown-out and cranking behaviour verified on the bench.
- [ ] Functional status class documented and met for every test.
