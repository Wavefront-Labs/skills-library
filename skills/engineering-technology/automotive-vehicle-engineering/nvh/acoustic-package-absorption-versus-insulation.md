---
id: engineering-technology.automotive-vehicle-engineering.nvh.acoustic-package-absorption-versus-insulation
name: acoustic-package-absorption-versus-insulation
category: engineering-technology
field: automotive-vehicle-engineering
product: nvh
tags: [acoustic-package, absorption, insulation, transmission-loss, mass-law, dash-insulator, headliner, carpet, decoupler, impedance-tube, body-acoustics]
level: practitioner
status: gated
description: "Design the vehicle acoustic package: insulation versus absorption, mass-law estimates, dash and floor mass-spring layers, leak sensitivity, and measurement methods."
sources:
  - "Harrison, Vehicle Refinement (chapter list)"
  - "ISO 10534-2 (impedance tube), ISO 354 (reverberation room absorption), ISO 10140 (laboratory sound insulation); designations not fetched (iso.org returned 403), confirm titles and editions"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Acoustic package: absorption versus insulation

## 1. Two jobs
- **Insulation (transmission loss, TL):** blocks airborne sound from entering through panels (dash, floor, doors, roof, glass).
- **Absorption:** removes acoustic energy inside the cabin and cavities, lowering reverberant level and reducing reflections.
They need different materials, and mass added for one does not give the other.

## 2. Insulation basics
- **Mass law:** for a single homogeneous limp panel, field-incidence TL rises by about 6 dB for each doubling of mass per area or frequency; a common approximation is TL = 20 log10(m x f) - 47 dB (m in kg/m2, f in Hz); this follows from normal-incidence TL = 20 log10(pi m f / (rho c)) = 20 log10(m f) - 42.4 dB with rho c = 415 rayl (computed) less the usual 5 dB field-incidence correction (the 5 dB is a textbook convention (gated: unconfirmed, source is paywalled or blocked)). Real panels deviate near critical (coincidence) frequency and low-frequency modes.
- **Mass-spring-mass (double wall):** a heavy layer on a decoupler foam on the steel panel gives much higher TL than the same mass bonded directly to the panel, above the double-wall resonance. Dash insulators are typically heavy layers (EPDM, EVA or filled polymer) over decoupling foam or fibre.
- **Leaks:** a small hole or poorly sealed grommet strongly reduces effective TL; seal cable and pipe pass-throughs.

## 3. Absorption basics
Porous materials (felts, shoddy cotton, melamine foam, non-woven fibres) absorb by viscous friction; effectiveness depends on flow resistivity, thickness, and mounting distance from a rigid wall (a quarter-wavelength rule; air gap increases low-frequency absorption). Use on carpet, headliner, parcel shelf, door trim, under-bonnet liner, wheel arch liner. Absorption coefficient (alpha) is measured in an impedance tube (small samples) or reverberation room (larger).

## 4. Where to put what
- **Front of dash and firewall:** high TL (engine noise) with sealed grommets.
- **Floor:** insulator for road and exhaust noise; absorb in the carpet and under seats.
- **Wheel arches and under-body:** absorbent liners to cut tyre noise before it reaches the body.
- **Roof and pillars:** absorption headliners and light insulation for wind and rain noise.
Weigh mass and cost against dB: rank by dB per kg; usually fix leaks and reduce sources first.

## 5. Measurement and process
Panel TL measured in a transmission suite with the real layup; cabin-level tests with and without treatments (subtractive tests: remove pieces to quantify). Use SEA or FE-SEA to predict (see SEA modelling) and correlate. Check fire, odour, fogging and recyclability requirements for materials.

## Verify
- [ ] Leaks identified and sealed first.
- [ ] Layup tested in transmission loss with real attachment.
- [ ] Absorption and insulation placed by location and frequency range.
- [ ] Mass cost of each treatment ranked by dB benefit.
