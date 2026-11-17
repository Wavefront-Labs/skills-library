---
id: engineering-technology.aerospace-engineering.spacecraft-systems-design.separation-and-release-shock
name: separation-and-release-shock
category: engineering-technology
field: aerospace-engineering
product: spacecraft-systems-design
tags: [separation-shock, pyroshock, shock-response-spectrum, srs, clamp-band, shock-testing]
level: practitioner
status: draft
description: "Define and verify separation and release shock environments with shock response spectra, attenuation with distance and test or analysis for sensitive units."
sources:
  - "NASA-STD-7003A (pyroshock test criteria)"
  - "NASA GSFC-STD-7000 (GEVS)"
  - "launch vehicle user's guides"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Separation shock

**Goal:** show units survive the shock from separation systems, release devices and stage events.

## Environment
- The launch vehicle user's guide gives a shock response spectrum (SRS) at the payload interface for the separation system (clamp band, separation nut or bolt cutter). Use it as the source of the interface level.
- SRS: peak response of a single-degree-of-freedom oscillator bank (Q commonly 10) versus natural frequency, plotted log-log in g.
- Levels are highest near the source and fall with distance and with each joint crossed.

## Procedure
1. Collect SRS inputs: launcher separation, your own deployables (see deployable-mechanisms), pyro events.
2. Attenuate through the structure: use a published attenuation rule or measured data for the structure type (the attenuation depends on the number of joints and distance; confirm with tests).
3. Identify sensitive items: relays, quartz and crystal oscillators, ceramic parts, cracked solder joints, optics and MEMS.
4. Verify by test (shaker-driven SRS, resonant plate, or pyrotechnic source) or by similarity and analysis. Test tolerances are given in the standard (SRS typically within a band such as plus and minus 6 dB; see NASA-STD-7003A).
5. Mitigate: isolate, move sensitive units away from the source, shock mounts, or redesign the release.

## Gotchas
- Shock at frequencies above 10 kHz is rarely measurable without special instrumentation; use appropriate accelerometers and filtering.
- Qualify-by-vibration alone does not cover shock.

## Verify
- [ ] The units' tested SRS envelope the predicted environment plus margin at all frequencies in the band of concern.
