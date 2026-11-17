---
id: engineering-technology.chemical-engineering.separation-processes.particle-size-distribution-analysis
name: particle-size-distribution-analysis
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-solid-liquid-and-gas-solid, particle-size-distribution-analysis, particle-size-distribution, d50, rosin-rammler, sieve-analysis]
level: practitioner
status: draft
description: "Analyse a particle size distribution: cumulative curves, d10 d50 d90, mean diameters and the Rosin-Rammler or log-normal fit."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook, Kister Distillation Design, Treybal Mass-Transfer Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Particle size distribution analysis

**Goal:** Analyse a particle size distribution: cumulative curves, d10 d50 d90, mean diameters and the Rosin-Rammler or log-normal fit.

## Steps
1. Get the data by sieve analysis, laser diffraction or sedimentation, and note that the methods measure different diameters.
2. Plot the cumulative mass fraction versus size; read d10, d50 (median) and d90, and the span (d90 - d10)/d50.
3. The Sauter mean diameter d32 = sum(n d^3) / sum(n d^2) is the one used for surface area per volume in mass transfer and filtration.
4. Rosin-Rammler: cumulative retained R = exp(-(d/d_e)^n); fit by plotting ln(ln(1/R)) versus ln d.
5. Report the method, the basis (mass, number or volume) and the sample preparation.

## Gotchas
- Number and mass based averages differ greatly; state the basis.
- Aggregates give a different result from dispersed particles.

## Verify
- [ ] Cumulative curve is monotonic and ends at 100 percent.
- [ ] Fit is checked against d10 and d90.
