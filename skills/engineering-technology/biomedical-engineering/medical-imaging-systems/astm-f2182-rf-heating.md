---
id: engineering-technology.biomedical-engineering.medical-imaging-systems.astm-f2182-rf-heating
name: astm-f2182-rf-heating
category: engineering-technology
field: biomedical-engineering
product: medical-imaging-systems
tags: [astm-f2182, mri-safety, mr-conditional-testing, rf-heating, gel-phantom, specific-absorption-rate, passive-implant, mr-conditional]
level: advanced
status: gated
description: "Plan ASTM F2182 RF-induced heating tests for passive implants in MRI: gel phantom, probes, worst-case position, SAR normalisation and how results feed MR Conditional labelling."
sources: ["ASTM F2182 Standard Test Method for Measurement of Radio Frequency Induced Heating on or Near Passive Implants During Magnetic Resonance Imaging (confirm current edition)", "ASTM F2503 Standard Practice for Marking Medical Devices and Other Items for Safety in the Magnetic Resonance Environment", "ISO/TS 10974 Assessment of the safety of MRI for patients with an active implantable medical device (confirm edition)", "FDA, Testing and Labeling Medical Devices for Safety in the Magnetic Resonance (MR) Environment, https://www.fda.gov/media/74201/download"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# ASTM F2182 RF heating test

**Goal:** show the temperature rise at or near a passive implant during MRI RF exposure, to support MR Conditional labelling.

This describes the test approach; a qualified MR safety scientist and an accredited laboratory run and interpret the test, and the regulator decides what labelling is acceptable.

## Setup
1. **Phantom:** a box phantom filled with a gelled saline medium (polyacrylic acid and sodium chloride) with specified electrical properties (conductivity of roughly 0.5 S/m and relative permittivity near 80 are the usual target (gated: unconfirmed, source is paywalled or blocked); use the values in the standard) and thermal properties that limit convection.
2. **Probes:** fibre-optic or other MR-compatible temperature sensors at the hot spots on the implant and at reference locations; check probe placement accuracy and calibration.
3. **Position:** the implant in the position that gives worst-case heating (often near the edge of the phantom where E-field is highest); test more than one orientation and length where needed (heating depends strongly on implant length versus RF wavelength).
4. **RF exposure:** run the highest-SAR sequence available on the scanner for the declared field strengths (for example 1.5 T and 3 T) for about 15 minutes (gated: unconfirmed, source is paywalled or blocked); the whole-body average SAR is measured by calorimetry in the phantom (about 2 W/kg (gated: unconfirmed, source is paywalled or blocked); FDA's MR guidance uses 2 W/kg as the Normal Operating Mode whole-body SAR, which IEC 60601-2-33 allows to be exceeded for short intervals).
5. **Reference run:** the same exposure without the implant to subtract background heating.

## Analysis
- Temperature rise attributable to the implant: delta T from the implant location minus reference.
- Normalise to a whole-body SAR of 2 W/kg (FDA: scale results in C per W/kg or per V/m to build MR Conditional labelling) and assess the in vivo temperature using computer simulation and thermal modelling (a regulator often accepts this in the labelling justification).
- Report heating at each field strength; label with scan conditions (field strength, SAR limit, scan duration).

## Gotchas
- Lead and wire-like implants and active implants need different methods (ISO/TS 10974).
- Small changes in length or loop geometry change resonance; test worst cases.
- Probe self-heating and artefacts due to RF coupling.

## Verify
- [ ] Phantom properties measured and documented.
- [ ] Repeated run reproducibility.
- [ ] Report supports the exact labelling claim, reviewed by MR safety expert.
