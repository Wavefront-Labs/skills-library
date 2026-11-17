---
id: engineering-technology.biomedical-engineering.biomedical-instrumentation.emc-emissions
name: emc-emissions
category: engineering-technology
field: biomedical-engineering
product: biomedical-instrumentation
tags: [emc-emissions, medical-emc, iec-60601-1-2, cispr-11, conducted-emissions, radiated-emissions, harmonics, flicker]
level: advanced
status: gated
description: "Plan EMC emission compliance for medical devices: CISPR 11 groups and classes, conducted and radiated limits, harmonics and flicker, and design measures that keep emissions down."
sources: ["IEC 60601-1-2 Medical electrical equipment - Electromagnetic disturbances (4th edition 2014 with amendment 1 2020; confirm edition)", "CISPR 11 Industrial scientific and medical equipment - Radio-frequency disturbance characteristics (confirm edition)", "IEC 61000-3-2 and IEC 61000-3-3 (harmonic current and flicker; confirm editions)"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# EMC emissions for medical devices

**Goal:** show the device does not emit electromagnetic disturbance above limits that would disturb other equipment.

Every dB figure below is (gated: unconfirmed, source is paywalled or blocked). Limits below are indicative from CISPR 11; confirm edition, measurement distance and the environment declared in the IEC 60601-1-2 edition you apply.

## Classification (CISPR 11)
- **Group 1:** RF energy generated only for internal functioning of the equipment. **Group 2:** RF energy intentionally generated or used for treatment or material processing (for example diathermy), with separate limits.
- **Class A:** suitable for non-domestic environments (including hospitals in the 4th edition of IEC 60601-1-2 for professional healthcare facilities, subject to the text); **Class B:** suitable for domestic establishments and connected to the public low-voltage network. Home healthcare equipment generally needs Class B.

## Typical limits for Group 1 (indicative)
- **Conducted emissions** (mains port, 150 kHz-30 MHz), quasi-peak: Class A about 79 dBuV (0.15-0.5 MHz) and 73 dBuV (0.5-30 MHz) (gated: unconfirmed, source is paywalled or blocked); Class B about 66 to 56 dBuV decreasing with log frequency (0.15-0.5 MHz), 56 dBuV (0.5-5 MHz), 60 dBuV (5-30 MHz).
- **Radiated emissions** at 10 m (30 MHz to 1 GHz): Class A about 40 dBuV/m (30-230 MHz) and 47 dBuV/m (230-1000 MHz); Class B about 30 and 37 dBuV/m respectively (gated: unconfirmed, source is paywalled or blocked). Higher-frequency ranges apply in newer editions for devices with fast clocks.
- **Harmonic current** (IEC 61000-3-2) and **voltage fluctuation and flicker** (IEC 61000-3-3) for mains-powered equipment up to 16 A per phase.

## Pre-compliance and design
1. Pre-scan in a near-field probe or a shielded chamber early.
2. Switch-mode supplies: input filter, common-mode choke, snubbers, spread-spectrum clocking.
3. Layout: continuous ground plane, short return loops, controlled-impedance clock lines, decoupling.
4. Cables: ferrites, shielded cables and shielding terminations at 360 degrees.
5. Enclosure seams and openings smaller than 1/20 of the shortest wavelength of concern.
6. Document the highest internal clock frequency (sets the upper frequency to measure).

## Verify
- [ ] Final test in an accredited lab with worst-case operating modes and accessories.
- [ ] Margin of at least 3-6 dB against limits to allow production variation.
- [ ] Re-test after hardware or firmware changes that affect clocks.
