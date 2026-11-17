---
id: engineering-technology.chemical-engineering.separation-processes.tray-efficiency-and-stage-count
name: tray-efficiency-and-stage-count
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-column-hydraulics, tray-efficiency-and-stage-count, tray-efficiency, murphree-efficiency, oconnell-correlation, overall-efficiency, actual-stages, stage-count, point-efficiency, distillation-trays]
level: practitioner
status: verified
description: "Convert theoretical stages to actual trays with O'Connell and Murphree efficiency estimates, understand typical ranges, and set stage counts with margin."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tray efficiency and actual stages

**Goal:** the number of real trays for a design and a defensible efficiency basis.

## Definitions
- **Overall efficiency** E_o = N_theoretical / N_actual.
- **Murphree vapour efficiency** E_MV = (y_n - y_{n+1}) / (y*_n - y_{n+1}), on a single tray.
- **Point efficiency** at one location on the tray; tray efficiency corrects for liquid mixing and entrainment.

## Estimates
1. **O'Connell correlation** (overall efficiency of fractionating columns as a function of the product alpha x mu_L, where alpha is the relative volatility of the keys and mu_L the liquid viscosity in mPa.s at average temperature). A commonly quoted fit: E_o (%) = 51 - 32.5 log10(alpha mu_L) (gated: unconfirmed, source is paywalled or blocked; the Drickamer and Bradford attribution is unconfirmed); other fits exist. Use the one in your reference and note the validity range.
2. **Typical values**: 50 to 80% for hydrocarbon distillation on sieve or valve trays; absorbers and strippers often 10 to 50%; very viscous or foaming service lower (rules of thumb (gated: unconfirmed, source is paywalled or blocked)).
3. **Vendor or published data** for the system, or pilot data, override correlations.

## Procedure
1. Compute theoretical stages with the shortcut and rigorous models.
2. Estimate efficiency in each section (top and bottom efficiencies can differ).
3. N_actual = N_theoretical / E_o, round up, add a margin (about 10% (gated: unconfirmed, source is paywalled or blocked)) or a spare tray or two for design uncertainty.
4. Choose feed tray and side-draw trays; allow multiple feed nozzles for flexibility.
5. Record the efficiency basis in the data sheet.

## Gotchas
- Tray efficiency decreases at low rates (weeping) and near flood (entrainment).
- Reboilers count as stages; do not double count.

## Verify
- [ ] Purity target met in the rigorous model with the estimated efficiency and with 10% lower.
- [ ] Alpha and viscosity average temperatures noted.
