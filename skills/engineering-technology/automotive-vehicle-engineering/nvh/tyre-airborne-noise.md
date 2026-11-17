---
id: engineering-technology.automotive-vehicle-engineering.nvh.tyre-airborne-noise
name: tyre-airborne-noise
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [tyre-noise, tyre-road-noise, tread-pattern, pitch-sequence, air-pumping, un-r117, rolling-noise]
level: practitioner
status: gated
description: "Understand tyre airborne noise (500-2000 Hz): mechanisms, tread pitch sequencing, surface effect, regulation and label limits, and the tyre selection process."
sources:
  - "Sandberg and Ejsmont, Tyre/Road Noise Reference Book"
  - "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32020R0740"
  - "UN Regulation 117; confirm current limits"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Tyre airborne noise

1. Mechanisms: tread impact (block impact on road), air pumping from grooves, stick-slip and stick-snap at the contact patch, and vibration of the tyre structure radiating sound (below about 1 kHz structural, above 1 kHz air-related; textbook split (gated: unconfirmed, source is paywalled or blocked)).
2. Tread design: pitch sequencing varies the block lengths to spread tonal energy into broadband noise; lateral groove shapes and angle; block stiffness; wide tyres typically noisier.
3. Surface: road surface texture strongly affects levels (coarse chip seal or concrete is louder, porous asphalt quieter), so use a reference surface (ISO 10844 test surface for pass-by tests; the current edition is ISO 10844:2021 per the iso.org catalogue, page itself 403).
4. Regulation: UN R117 covers tyre rolling sound emission (Annex 3), wet grip (Annex 5) and rolling resistance (Annex 6) as cited by EU Regulation 2020/740, with limits by tyre class and width (limit values (gated: unconfirmed, source is paywalled or blocked)); the EU tyre label shows fuel efficiency, wet grip, external rolling noise in dB(A) with class (noise class set relative to the EU limit value: N <= LV-3, LV-3 < N <= LV, N > LV), and snow/ice pictograms; confirm current limit values and label scheme.
5. Process: trial tyres on the vehicle, measure interior noise at 60/80/100 km/h on standard surfaces, compare with benchmark; use A-weighted and loudness metrics.
6. Interaction: tyre choice sets low-frequency forces and high-frequency noise; trade with rolling resistance and grip.

**Gotchas:** tyre wear and temperature change tonal content.

## Verify
- [ ] Interior noise per tyre candidate recorded at constant speeds on the same surface.
- [ ] Tyre meets regulatory and label noise limits per the certificate.
