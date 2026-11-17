---
id: natural-sciences.atmospheric-sciences.radar-satellite-meteorology.interpreting-reflectivity-velocity-and-dual-pol
name: interpreting-reflectivity-velocity-and-dual-pol
category: natural-sciences
field: atmospheric-sciences
product: radar-satellite-meteorology
tags: [radar-satellite-meteorology, weather-radar, doppler-radar, nexrad, wsr-88d, reflectivity, dbz, z-r-relationship, radial-velocity, velocity-aliasing, dealiasing, couplet, mesocyclone, dual-polarisation, dual-pol, zdr, rhohv, cc, correlation-coefficient, kdp, hail, melting-layer, bright-band, debris-signature, beam-blockage, ground-clutter, anomalous-propagation, pyart]
level: practitioner
status: docs-checked
description: "Interpret weather radar: reflectivity, radial velocity with aliasing and couplets, dual-pol ZDR/CC/KDP for hail, melting layer and debris, and non-weather artefacts."
sources: [https://www.weather.gov/jan/dualpolupgrade-applications, https://www.weather.gov/bmx/radar_dualpol]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Interpreting reflectivity, velocity and dual-pol radar

**Goal:** read a weather-radar volume correctly — what is precipitation and how
intense, how the air is moving, what kind of hydrometeor is there — and spot the
artefacts that look like weather but aren't.

## 1. Geometry first
- The radar scans at several **elevation angles**; the lowest is used for most
  displays. The beam rises with range (Earth curvature + elevation) and widens.
  Far from the radar you **overshoot** low-level features (shallow snow, drizzle, tornado
  circulations).
- Know where the radar is; many artefacts are range- or azimuth-dependent.

## 2. Reflectivity (Z, dBZ)
- Proportional to the sum of the sixth power of drop diameters — dominated by the largest
  particles. A few big drops or hail produce high Z.
- Hail: the NWS Jackson guidance says reflectivity is typically greater than 55 dBZ,
  possibly as low as 45 dBZ in rare cases.
- Rain rate comes from a **Z–R relationship**, which is uncertain: hail contamination,
  bright band and drop-size variation all bias it. Check which relationship your
  product uses.
- Structures: bow echoes (damaging winds), hook echoes (supercells), bounded weak echo
  regions (strong updrafts) — look at multiple tilts.

## 3. Radial velocity
- Doppler radar measures only the **component toward/away** from the radar. Check your
  viewer's colour table for which colours mean toward and away. The zero isodop is where
  the wind is perpendicular to the beam.
- **Aliasing:** speeds beyond the Nyquist velocity fold over (bright red next to bright green
  with no zero line between them). Dealiased products correct most, but check suspicious
  couplets for fold-over.
- **Rotation couplet:** inbound and outbound maxima side by side across the radial
  (azimuthal shear). **Convergence/divergence:** inbound/outbound along the same radial
  (e.g. outflow, downburst divergence near the surface).
- Use storm-relative velocity to see rotation in fast-moving storms.

## 4. Dual-polarisation
| Product | What it measures | Key uses |
|---|---|---|
| **ZDR** (dB) | Horizontal vs vertical reflectivity: particle shape | Hail is close to 0 dB; small melting hail can give significantly higher values; used to find a hail core |
| **CC / ρhv** | Correlation between H and V returns: particle diversity | Hail typically 0.7 to 0.95, below 0.85 often giant hail (> 2 in); freezing rain 0.95 or higher; used to locate the melting layer and updrafts |
| **KDP** (°/km) | Differential phase shift | Above 1.5 °/km for melting, water-coated hail, near 0 if dry; noisy in the melting layer |
- **Melting layer / bright band:** a ring around the radar; shows as a band of lower CC,
  noisy mainly positive ZDR and noisy KDP.
- **Tornado debris signature (TDS):** a localised area of low CC (typically below 0.8),
  ZDR usually near 0 dB, and high reflectivity almost co-located with tight rotation.
- **Winter guidelines (not hard rules):** dry snow reflectivity under 35 dBZ with CC
  0.97 to 1.01 and ZDR -0.3 to 1.5 dB; wet snow reflectivity 25 to 50 dBZ with CC 0.88
  to 0.985 and ZDR -0.5 to 3 dB.
- **Hail:** high Z with ZDR near 0 and reduced CC.

## 5. Non-weather echoes
- **Ground clutter** and **anomalous propagation** (beam bent to the ground by inversions):
  stationary or speckled near-zero velocity, low CC.
- **Biological echoes** (birds, insects): can appear as non-weather echoes, usually
  with low CC; confirm with the products and time of day.
- **Beam blockage** by terrain/buildings: wedges of reduced Z downstream of an obstacle.
- **Attenuation** (strong at C/X band): echoes behind intense cores look weaker.
- Chaff, smoke plumes, wind farms also appear.

## Tools
Check product units and colour tables in your viewer before comparing.

## Gotchas
- Compare with satellite, surface obs and soundings; radar alone can't tell you surface
  precipitation type reliably.
- Velocity products are relative to the radar; a "couplet" from a single gate is noise.

Thresholds are rules of thumb from NWS guidance for the WSR-88D; other radars differ in
attenuation and dual-pol values.

## Checked
2026-11-01. Confirmed in the NWS Jackson page "Dual-Pol Applications": hail reflectivity,
hail ZDR/CC/KDP, freezing rain CC, melting layer behaviour, TDS values, winter-precipitation
guidelines. The NWS Birmingham dual-pol page confirms ZDR, CC and KDP as the new base
products and melting-layer and debris detection as uses. Removed: beam height and width
figures, the rain dBZ scale, Marshall-Palmer constants and the factor-of-2 claim, ZDR
1-4 dB for rain, CC bands for rain and mixed hail, roost-ring and insect ZDR statements,
and the tool list. Velocity, aliasing and artefact descriptions are general radar practice
and carry no figures.
Method: documentation only; no commands were run.

## Verify
- [ ] Beam height at the feature's range considered.
- [ ] Velocity features checked for aliasing and against the radar-relative geometry.
- [ ] Dual-pol products used together (Z + ZDR + CC), not one in isolation.
- [ ] Clutter, biological echoes, blockage and bright band ruled out before interpreting.
