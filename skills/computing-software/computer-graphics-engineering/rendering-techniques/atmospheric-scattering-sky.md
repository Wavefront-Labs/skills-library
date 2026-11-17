---
id: computing-software.computer-graphics-engineering.rendering-techniques.atmospheric-scattering-sky
name: atmospheric-scattering-sky
category: computing-software
field: computer-graphics-engineering
product: rendering-techniques
tags: [computer-graphics-engineering, rendering-techniques, volumetric-rendering, atmospheric-scattering, sky-rendering, rayleigh-scattering, mie-scattering, transmittance-lut, aerial-perspective, hillaire-sky]
level: advanced
status: docs-checked
description: "Render a physically based sky and aerial perspective: Rayleigh/Mie/ozone parameters, transmittance and multiple-scattering LUTs, sky-view LUT."
sources: ["https://sebh.github.io/publications/egsr2020.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Atmospheric scattering sky

**Goal:** a sky and distant haze that respond correctly to time of day, altitude and planet
parameters, using the LUT set from Hillaire's "A Scalable and Production Ready Sky and
Atmosphere Rendering Technique" (EGSR 2020). It needs no high-dimensional LUTs, so the
atmosphere can change dynamically without heavy LUT updates.

## 1. Physical parameters (Earth-like, per km, from the paper)
| component | scattering | absorption | density profile |
|---|---|---|---|
| Rayleigh (air) | (5.802, 13.558, 33.1) e-3 | 0 | exp(-h / 8 km) |
| Mie (aerosols) | 3.996e-3 | 4.40e-3 | exp(-h / 1.2 km); Cornette-Shanks phase, default g = 0.8 |
| Ozone | 0 | (0.650, 1.881, 0.085) e-3 | tent function, 30 km wide, centred at 25 km altitude |
Ground radius 6360 km, atmosphere top 6460 km. The paper notes the simpler Henyey-Greenstein
phase function is also appropriate. Ozone matters for the sky colour when the sun is near the
horizon.

## 2. LUTs
1. **Transmittance LUT** (256x64): the atmosphere transmittance toward the sun, stored with the
   same representation as Bruneton and Neyret 2008 so it is not ray marched per sample.
2. **Multiple-scattering LUT** (32x32): a small 2D texture, u = 0.5 + 0.5 cos(sun zenith),
   v = altitude normalised between ground and top radius. It assumes multiple scattering is
   isotropic and varies only with altitude, and sums the infinite orders as a geometric series
   F_ms = 1 / (1 - f_ms) applied to the second-order contribution. This replaces the per-order
   iteration used by older LUT models.
3. **Sky-View LUT** (200x100): the distant sky rendered into a latitude/longitude texture oriented
   to the local up vector, so the horizon is a horizontal line. A non-linear latitude
   mapping (a simple quadratic curve in the paper) concentrates texels at the horizon. The
   sun disk is not in this texture; it is composited after the LUT is applied.
4. **Aerial perspective volume** (32x32 over the screen with 32 depth slices, over 32 km by
   default): in-scattering in RGB and the mean of the RGB transmittance in alpha. Applied to
   opaque objects as a post process; for transparents in a forward pipeline apply it per vertex.

## 3. Integration
The paper integrates scattered luminance along the path with transmittance T, shadow factor S
(planet shadow and, optionally, volumetric shadows) and in-scattering. The multiple-scattering
LUT contribution is added at each sample. The paper's reported step counts are about 20-40 per
LUT on a PC; treat them as starting points.

## Gotchas
- With volumetric shadows enabled the Sky-View LUT shortcut cannot be used for the sky, since
  per-pixel ray marching is needed.
- The Sky-View LUT needs the non-linear latitude mapping to avoid visible horizon artefacts.
- Keep units consistent: the table above is per kilometre.

## Verify
- [ ] Noon sky, sunset reddening and twilight look plausible across a day cycle.
- [ ] Aerial perspective tints distant geometry consistently with the sky at the horizon.
- [ ] Per-frame LUT cost measured on target hardware (the paper reports sub-millisecond on PC).

## Checked

Method: docs-checked 2026-11-09 against the EGSR 2020 paper (Hillaire), downloaded as PDF and read as text: section 4 and 5 parameters, LUT sections 5.2-5.5 and the performance table. Dropped the UE sample repo and Bruneton site sources (not read), the code sketch details, exposure range and cube-map remarks.
