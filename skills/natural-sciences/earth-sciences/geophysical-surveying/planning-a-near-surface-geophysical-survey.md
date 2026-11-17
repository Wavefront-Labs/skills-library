---
id: natural-sciences.earth-sciences.geophysical-surveying.planning-a-near-surface-geophysical-survey
name: planning-a-near-surface-geophysical-survey
category: natural-sciences
field: earth-sciences
product: geophysical-surveying
tags: [geophysical-surveying, near-surface-geophysics, magnetometry, magnetic-survey, gradiometer, diurnal-correction, resistivity, ert, electrical-resistivity-tomography, wenner, dipole-dipole, gpr, ground-penetrating-radar, gravity, bouguer-correction, seismic-refraction, seismic-reflection, survey-design, line-spacing, nyquist, inversion, res2dinv, pygimli, archaeogeophysics]
level: practitioner
status: gated
description: "Pick the right near-surface method (magnetics, ERT, GPR, gravity, seismic) for a target, design line/station spacing, run QC in the field and avoid over-reading inversions."
sources: ["Reynolds, An Introduction to Applied and Environmental Geophysics (Wiley)", "Milsom & Eriksen, Field Geophysics (Wiley)", "pyGIMLi documentation"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Planning a near-surface geophysical survey

**Goal:** a survey that can actually see the target — right physical property, right
spacing, right depth — and field data good enough that the interpretation is not wishful.

## 1. Match the method to the contrast
A target is only detectable if it differs from its surroundings in some physical property.

| Method | Property | Good for | Struggles with |
|---|---|---|---|
| Magnetometry | magnetic susceptibility/remanence | buried metal, fired features, dykes, UXO screening | cultural noise (fences, cars), deep targets |
| Resistivity (ERT) | electrical resistivity | groundwater, clay vs sand, voids, landfill extent | very dry/frozen ground (contact resistance) |
| GPR | dielectric contrast | shallow layers, pipes, rebar, ice | clay-rich or saline ground (signal dies in <1 m) |
| Gravity | density | voids, basins, buried valleys | slow; needs precise elevations |
| Seismic refraction/reflection | elastic velocity/impedance | bedrock depth, layer stratigraphy | velocity inversions (refraction), noise |

Do a **forward model** or back-of-envelope estimate first: will a 2 m void at 10 m depth
produce a gravity anomaly larger than your noise? (Often it won't: with a density contrast of -2000 kg/m³ a 2 m diameter void at 10 m depth gives a peak of about 0.008 mGal as a long horizontal cylinder and about 0.0006 mGal as a sphere, both computed; field gravity noise is typically ~0.01 mGal or worse (gated: unconfirmed, source is paywalled or blocked)).

## 2. Survey geometry
- **Spacing:** the smallest target you want to resolve needs at least 2 samples across it,
  ideally 3–4. A 1 m wide wall needs ≤0.5 m line spacing for magnetics/GPR.
- **Depth vs array:** ERT investigation depth is roughly 15–20% of the total array
  length for Wenner (more for dipole-dipole, *depends on array and model*) (gated: unconfirmed, source is paywalled or blocked). Want 20 m
  depth → spread of ~100+ m.
- Lines **perpendicular** to the expected target strike.
- Extend lines well beyond the target so you capture background.

## 3. Field QC by method
- **Magnetics:** set up a base station or revisit a reference point every 30–60 min for
  diurnal drift; check heading error by walking a line both ways; remove magnetic items
  from the operator (phone, keys, steel-toed boots).
- **ERT:** check contact resistances before acquisition (water the electrodes with brine
  if high); run reciprocal or repeat measurements to estimate error; flag outliers.
- **GPR:** calibrate velocity from a hyperbola or a known depth; set time window to
  ~1.5× target two-way time; note antenna frequency (higher = shallower, sharper).
- **Gravity:** loop back to a base every 1–2 h for drift; survey elevations to a few cm
  (1 cm ≈ 0.003 mGal free-air effect; computed from 2GM/R³ = 0.308 mGal/m); apply latitude, free-air, Bouguer and terrain
  corrections, stating the reduction density.
- **Seismic:** stack several shots per location; record noise records; reverse shots for
  dipping layers.

## 4. Processing and inversion
- Keep raw data; process copies. Document every filter.
- Inversions (Res2DInv, pyGIMLi, BERT) produce *one* model that fits the data, not the
  truth. Report the RMS/chi² misfit, try a few regularisation settings, and look at the
  sensitivity or depth of investigation (DOI) index — don't interpret below it.
- Integrate with boreholes or trial pits wherever possible; one ground-truth point
  calibrates the whole section.

## Gotchas
- Choosing GPR on clay — the radar sees nothing beyond a few tens of cm.
- Line spacing chosen for convenience, not target size.
- Reading features at the edges and bottoms of inversion sections (artifacts are common).
- Positioning errors: use RTK GNSS or a total station for sub-metre work.
- Permits: utility clearances and landowner permissions before any electrode goes in.

## Verify
- [ ] The target's physical-property contrast and expected anomaly size are estimated.
- [ ] Spacing gives ≥2 samples across the smallest target; lines cross its strike.
- [ ] Drift/repeat/reciprocal checks recorded in the field.
- [ ] Inversion misfit and depth of investigation reported with the section.
- [ ] Interpretation tied to at least one independent ground-truth point if available.
