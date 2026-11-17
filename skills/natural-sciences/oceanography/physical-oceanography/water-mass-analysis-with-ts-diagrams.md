---
id: natural-sciences.oceanography.physical-oceanography.water-mass-analysis-with-ts-diagrams
name: water-mass-analysis-with-ts-diagrams
category: natural-sciences
field: oceanography
product: physical-oceanography
tags: [physical-oceanography, water-masses, ts-diagram, theta-s, teos-10, gsw, absolute-salinity, conservative-temperature, potential-temperature, practical-salinity, potential-density, sigma-theta, neutral-density, isopycnals, mixing-triangle, omp-analysis, optimum-multiparameter, ctd, argo, nadw, aaiw, aabw, mediterranean-outflow]
level: practitioner
status: verified
description: "Identify and quantify water masses from CTD/Argo profiles: TEOS-10 conversions, theta-S diagrams with isopycnals, source water types, mixing triangles and OMP analysis."
sources: ["Talley et al., Descriptive Physical Oceanography (6th ed.)", "IOC/SCOR/IAPSO TEOS-10 manual and GSW toolbox documentation", "Tomczak & Large 1989, OMP analysis"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Water-mass analysis with T–S diagrams

**Goal:** from temperature/salinity profiles, say which water masses are present, where
they mix, and in what proportions — with the thermodynamics done the modern (TEOS-10) way.

## 1. Convert with TEOS-10 (GSW)
Raw CTD gives in-situ temperature (t), practical salinity (SP, unitless PSS-78) and
pressure (p, dbar). Convert:
```python
import gsw
SA = gsw.SA_from_SP(SP, p, lon, lat)   # Absolute Salinity, g/kg (location-dependent)
CT = gsw.CT_from_t(SA, t, p)           # Conservative Temperature, °C
sigma0 = gsw.sigma0(SA, CT)            # potential density anomaly ref. 0 dbar, kg/m³
```
- Use **CT and SA** for analysis (TEOS-10 recommends them); still archive and report
  **SP** as the measured variable in data submissions.
- Older literature uses potential temperature θ and SP; when comparing, convert
  consistently and label axes properly.
- Density reference (checked with gsw: a cold deep parcel at SA 34.7, CT 0.5 has lower σ0 than a warmer one at SA 34.9, CT 2.0 but higher σ4): σ0 is fine for upper ocean; for deep water use σ2 or σ4 (or neutral
  density γⁿ) — σ0 can invert with depth in the abyss due to thermobaricity.

## 2. Plot the T–S diagram
- CT on y, SA on x, **isopycnals** contoured underneath (compute σ on a grid with gsw).
- Colour points by depth or by station; one line per profile.
- Water masses appear as **extrema** (salinity minimum = intermediate water like AAIW;
  salinity maximum = Mediterranean Outflow/subtropical underwater) or as points/lines
  where profiles converge.
- Straight segments between two water types indicate two-component mixing; curved
  envelopes indicate three or more.

## 3. Define source water types
Use literature definitions (Talley et al. tables, regional papers) or the water's
formation region values, e.g. characteristic CT, SA (and ideally oxygen, nutrients,
silicate, CFCs). Write them down with references — results depend heavily on these choices.

## 4. Mixing fractions
- **Mixing triangle** (three end-members, two conservative tracers + mass conservation):
  solve
  ```
  x1 + x2 + x3 = 1
  x1·CT1 + x2·CT2 + x3·CT3 = CT
  x1·SA1 + x2·SA2 + x3·SA3 = SA
  ```
- **OMP analysis** (Optimum Multiparameter): over-determined least squares with more
  tracers (O2, NO3, PO4, SiO4 — non-conservative ones corrected via Redfield ratios in
  extended OMP), weighted by tracer reliability, with non-negativity constraints.
  Toolboxes exist in MATLAB and Python (*check maintenance status before relying on one*).
- Negative or >1 fractions mean a missing end-member or bad definitions.

## 5. Interpret
Track a water mass core (e.g. the salinity minimum) along a section to show spreading
paths; combine with oxygen (age-proxy: decreasing O2 along path) and transient tracers.

## Gotchas
- Using in-situ temperature and density at depth — compressibility makes deep waters
  look warmer and denser than they are.
- Treating oxygen and nutrients as conservative without correction.
- Surface mixed-layer points scatter wildly (air–sea exchange); exclude them from deep
  water-mass analysis.
- Spiky salinity from CTD sensor lag at sharp gradients — use processed (aligned,
  lag-corrected) data.

## Verify
- [ ] All variables converted to SA/CT with gsw; units on every axis.
- [ ] Appropriate density reference for the depth range plotted.
- [ ] Source water type definitions cited.
- [ ] Mixing fractions all in [0, 1] and sum to 1; residuals reported.
- [ ] Water-mass cores traced consistently across stations.
