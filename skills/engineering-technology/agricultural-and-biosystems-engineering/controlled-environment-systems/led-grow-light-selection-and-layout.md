---
id: engineering-technology.agricultural-and-biosystems-engineering.controlled-environment-systems.led-grow-light-selection-and-layout
name: led-grow-light-selection-and-layout
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: controlled-environment-systems
tags: [agricultural-and-biosystems-engineering, controlled-environment-systems, led-grow-lights, horticultural-lighting, grow-lighting, photon-efficacy, ppfd-uniformity, light-layout, spectrum]
level: practitioner
status: draft
description: "Select LED grow lights by photon efficacy, spectrum and PPFD uniformity, plan mounting height and layout, and account for heat load, controls and independent test data."
sources:
  - "Michigan State University Extension, LED fixture efficacy (https://www.canr.msu.edu/floriculture/uploads/files/LED efficacy.pdf)"
  - "DesignLights Consortium horticultural lighting requirements (https://www.designlights.org)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# LED grow light selection and layout

**Goal:** the required PPFD or DLI at the canopy at the lowest cost over the life of the fixtures.

## Key metrics
- **PPF** (photosynthetic photon flux, micromoles per second) of the fixture and **photon efficacy** in micromoles per joule (PPF divided by input power). The best double-ended HPS fixtures with electronic ballasts are about 1.7 umol/J (Michigan State Extension); the original DLC horticultural minimum was 1.9 umol/J and later versions raised it (v3.0 by 21 percent, v4.0 by a further 8.7 percent), which suggests about 2.5 umol/J for current listings (arithmetic, not a quoted figure; check the current DLC Horticultural Technical Requirements). Use independent test reports (for example from a test laboratory or a certification listing such as DLC) rather than claims.
- **PPFD** (umol per square metre per second) at the canopy and its uniformity (minimum to average).
- **Spectrum**: red and blue plus white; far-red affects shade avoidance, flowering and leaf expansion; choose by the crop and research advice.

## Layout
1. Required DLI and photoperiod give the target PPFD (see the DLI skill).
2. Use a lighting design programme or manufacturer layout with the fixture photometric file (IES file) to compute the PPFD map for mounting height and spacing; the edge fixtures need overhang or reflective walls.
3. Mounting height and beam angle affect uniformity and canopy spacing; account for crop growth.
4. **Heat**: electrical power not converted to light becomes heat (roughly half or more of the input for LEDs); LEDs reduce radiant heat on the canopy but all power is in the room: include it in the cooling load (see the grow room HVAC skill).
5. **Controls**: dimmable drivers, schedules and sunlight integration for supplemental lighting.
6. Electrical: circuit sizing, ingress protection in wet environments, and maintenance.

## Verify
- [ ] Measure PPFD on a grid with a calibrated quantum sensor and compare average and uniformity with the design.
