---
id: natural-sciences.atmospheric-sciences.atmospheric-observation.reading-a-skew-t-sounding
name: reading-a-skew-t-sounding
category: natural-sciences
field: atmospheric-sciences
product: atmospheric-observation
tags: [atmospheric-observation, radiosonde, upper-air, sounding, skew-t, skew-t-log-p, thermodynamic-diagram, dry-adiabat, moist-adiabat, mixing-ratio, lcl, lfc, el, cape, cin, mlcape, lifted-index, inversion, capping-inversion, lapse-rate, precipitable-water, hodograph, wind-shear, bulk-shear, freezing-level, metpy, sharppy, convective-forecasting]
level: practitioner
status: gated
description: "Read a radiosonde sounding on a Skew-T log-P: identify lines, inversions and moist layers, lift a parcel to find LCL, LFC, EL, CAPE and CIN, and read the hodograph for shear."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reading a Skew-T sounding

**Goal:** extract from a single upper-air sounding the stability, moisture and wind
structure of the atmosphere — enough to judge whether convection can start, how strong
it could be, and what form it might take.

## 1. Know the lines
On a Skew-T log-P diagram:
- **Isobars:** horizontal, logarithmically spaced (1000 hPa at bottom).
- **Isotherms:** straight lines skewed up to the right at 45°.
- **Dry adiabats:** curved lines sloping up-left — the path of unsaturated air (g/cp = 9.76 °C/km computed with cp = 1004.7 J/kg/K).
- **Moist (saturated) adiabats:** curved, steeper at low levels and becoming parallel to
  dry adiabats aloft — path of saturated air.
- **Mixing-ratio lines:** dashed, nearly straight, labelled in g/kg.
The sounding plots **temperature** (usually red, right) and **dewpoint** (green, left), with
wind barbs on the right.

## 2. First look
- **Moisture:** where T and Td are close (small dewpoint depression) the layer is near
  saturation — cloud layers. Wide gaps = dry layers.
- **Inversions:** temperature increasing with height (line bending right). A surface-based
  inversion is nocturnal cooling; an elevated warm, dry layer above moist air is a **cap**.
- **Lapse rates:** steeper than the moist adiabat (leaning left of it) in the mid-levels
  (700–500 hPa) means conditionally unstable "steep lapse rates", a key ingredient for
  severe convection. Approaching dry adiabatic = very unstable if lifted.
- **Freezing level:** height where the T line crosses 0 °C.

## 3. Lift a parcel
1. From the starting point (surface, mixed layer average of lowest ~100 hPa, or most unstable
   level), follow the **dry adiabat** up from T and the **mixing-ratio line** up from Td.
2. Where they meet is the **LCL** (lifted condensation level) ≈ cloud base for forced ascent.
3. From the LCL follow the **moist adiabat** upward.
4. Where the parcel line first crosses to the right of (warmer than) the environment is the
   **LFC**; where it crosses back is the **EL** (equilibrium level) ≈ storm top/anvil height.
5. **CAPE** = positive area between parcel and environment from LFC to EL (J/kg).
   **CIN** = negative area below the LFC — the energy that must be overcome.
Rough CAPE and CIN guides are forecaster rules of thumb and vary by region (gated: unconfirmed, source is paywalled or blocked): CAPE below 1000 J/kg marginal, 1000-2500 moderate, above 2500 large; CIN of tens of J/kg is easily overcome, much larger values usually suppress surface-based storms.

Specify the parcel: SBCAPE, MLCAPE (mixed-layer, common for forecasting) and MUCAPE can
differ greatly, especially with a nocturnal inversion. Virtual-temperature correction
changes small CAPE values noticeably.

## 4. Winds and hodograph
- Wind barbs with height: veering (turning clockwise) with height in the NH indicates warm
  advection; backing, cold advection.
- **Bulk shear** 0–6 km: vector difference between surface and 6 km winds. about 40 kt (~20 m/s) or more
  is the usual rule of thumb for organised storms/supercells (gated: unconfirmed, source is paywalled or blocked); weak shear favours short-lived pulse storms.
- A curved hodograph in the lowest 1–3 km (storm-relative helicity) supports rotating updrafts.

## 5. Tools
SHARPpy and MetPy (`metpy.calc.parcel_profile`, `cape_cin`, `lcl` and `metpy.plots.SkewT` all exist in the current release) compute
indices; check which parcel and virtual-temperature options they use before comparing
numbers. Sounding archives: University of Wyoming, NOAA/SPC (US), national services.

## Gotchas
- Radiosondes drift downwind during ascent (tens of km and 1.5-2 h to burst are typical figures (gated: unconfirmed, source is paywalled or blocked)); the upper part
  describes a different location and time than the launch.
- One sounding is a point sample; storms often form where conditions differ (boundaries,
  terrain). Use model soundings to see evolution.
- Indices are diagnostic aids, not forecasts; a high-CAPE, capped sounding may produce nothing.
- Wet-bulb zero and dry mid-levels matter for hail and downbursts; look beyond CAPE.

Uncertain here: thresholds are mid-latitude, US-style rules of thumb and vary by region and season.

## Verify
- [ ] Lines correctly identified; inversions and moist layers marked.
- [ ] Parcel type stated; LCL, LFC, EL located consistently on the diagram.
- [ ] CAPE and CIN sign and magnitude checked against software output.
- [ ] 0–6 km shear and hodograph shape noted.
- [ ] Sounding time/location vs storm environment considered.
