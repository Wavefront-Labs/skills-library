---
id: engineering-technology.chemical-engineering.piping-instrumentation.colebrook-friction-factor
name: colebrook-friction-factor
category: engineering-technology
field: chemical-engineering
product: piping-instrumentation
tags: [chemical-engineering, piping-instrumentation, pi-line-sizing, colebrook-friction-factor, darcy-friction-factor, colebrook-equation, haaland, moody-chart, pipe-roughness, reynolds-number, friction-loss, darcy-weisbach]
level: practitioner
status: gated
description: "Compute the Darcy friction factor with the Colebrook equation or the explicit Haaland approximation, with pipe roughness data and laminar and transition handling."
sources:
  - "Crane Technical Paper 410, Perry Handbook fluid transport section, ASME B31.3 Process Piping, ISA-5.1, ISO 10628, ISA-75.01.01 / IEC 60534-2-1, Darby Chemical Engineering Fluid Mechanics, Karassik Pump Handbook"
  - "https://www.aiche.org"
  - "Haaland 1983, J Fluids Eng 105:89-90, doi:10.1115/1.3240948 (Crossref)"
  - "Colebrook 1939, J Inst Civil Eng 11:133-156, doi:10.1680/ijoti.1939.13150 (Crossref)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Darcy friction factor and the Colebrook equation

**Goal:** a reliable friction factor in code or a spreadsheet.

## Equations
- Laminar (Re below about 2,300): f = 64/Re (Darcy).
- Turbulent (Colebrook-White, implicit): 1/sqrt(f) = -2 log10( (eps/D)/3.7 + 2.51/(Re sqrt(f)) ).
- Haaland (explicit, within a couple of percent of Colebrook): 1/sqrt(f) = -1.8 log10[ ((eps/D)/3.7)^1.11 + 6.9/Re ].
- Pressure drop: dP = f (L/D) rho v^2/2 (f is the Darcy factor, four times the Fanning factor).

## Roughness (absolute, typical)
Commercial steel about 0.045 mm; drawn tubing about 0.0015 mm; cast iron about 0.26 mm; plastic and glass about smooth (gated: unconfirmed, source is paywalled or blocked). Aged pipe is rougher; use a margin for old lines.

## Solving Colebrook
Iterate: start with the Haaland value, then substitute into the right side two to four times; or use the Lambert W form. In a spreadsheet use an iterative cell or Haaland.

## Transition
Between about Re 2,300 and 4,000 the factor is uncertain; avoid designing in this range or use the higher of the laminar and turbulent estimates.

## Worked check
Water in 77.9 mm pipe with eps = 0.045 mm (eps/D = 0.000578) and Re = 1.8e5: Haaland: ((eps/D)/3.7)^1.11 = (1.56e-4)^1.11 = 5.95e-5 and 6.9/Re = 3.83e-5, so 1/sqrt(f) = -1.8 log10(9.78e-5) = 7.21 and f = 0.0192. Colebrook (iterated, brentq) gives f = 0.0194, about 1% apart.

## Gotchas
- Mixing Darcy and Fanning factors (a factor of 4).
- Using diameter in the wrong units in the roughness ratio.

## Verify
- [ ] Code reproduces known Moody chart points (for example Re = 1e5, eps/D = 0.001, f about 0.022).
- [ ] Laminar and turbulent branches meet sensibly.
