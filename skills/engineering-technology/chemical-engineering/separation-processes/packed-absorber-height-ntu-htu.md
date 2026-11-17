---
id: engineering-technology.chemical-engineering.separation-processes.packed-absorber-height-ntu-htu
name: packed-absorber-height-ntu-htu
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-absorption-and-stripping, packed-absorber-height-ntu-htu, ntu, htu, transfer-units, packed-absorber, height-of-packing, hog, nog, mass-transfer-coefficient, gas-absorption-column]
level: practitioner
status: verified
description: "Compute packed absorber height from transfer units: H_OG, N_OG for dilute linear equilibrium, mass-transfer coefficient sources and checks on wetting and flooding."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Packed absorber height with NTU and HTU

**Goal:** the packed height Z = H_OG N_OG.

## Equations
- Z = H_OG x N_OG, where H_OG = G_m/(K_y a) is the height of an overall gas-phase transfer unit and N_OG the number of transfer units.
- For dilute solute, linear equilibrium y = m x, and A = L/(m V):
N_OG = [1/(1 - 1/A)] ln{ [(y_in - m x_in)/(y_out - m x_in)] (1 - 1/A) + 1/A }.
- Check (computed): m = 1, A = 1.4, clean solvent, 95% removal gives N_OG = 6.5126 from the closed form and 6.5126 by numerical integration of dy/(y - y*) along the operating line; the A -> 1 limit of the closed form tends to (y_in - y_out)/(y_out - m x_in) = 19 exactly (18.98 at A = 1.0001).
- Film resistances add: H_OG = H_G + (m V/L) H_L.

## Procedure
1. Fix equilibrium, flows and terminal compositions as in the Kremser skill.
2. Compute N_OG from the equation.
3. Obtain H_G and H_L (or K_y a) from the packing supplier's correlations (Onda or Billet-Schultes are widely used correlations; check the validity range in the original papers) or from pilot data.
4. Z = H_OG N_OG; add 10 to 20% margin (gated: unconfirmed, source is paywalled or blocked); check the packing height per bed and redistribution.
5. Confirm flooding and wetting rate; confirm pressure drop (see `engineering-technology.chemical-engineering.separation-processes.packed-column-hetp-and-pressure-drop`).
6. For reactive absorption (CO2 into amines), the enhancement factor changes H_L drastically; use a rate-based model.

## Gotchas
- Gas-film-controlled systems (ammonia into water) versus liquid-film-controlled (CO2 into water): the dominant film decides.
- At low liquid rates the interfacial area can be well below the packing surface area.

## Verify
- [ ] N_OG test: A = 1 limit gives N_OG = (y_in - y_out)/(y_out - m x_in) approx; check.
- [ ] Z against a rigorous or vendor calculation within 15% (gated: unconfirmed, source is paywalled or blocked).
