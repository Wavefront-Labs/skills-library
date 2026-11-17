---
id: engineering-technology.chemical-engineering.separation-processes.msmpr-crystalliser-design
name: msmpr-crystalliser-design
category: engineering-technology
field: chemical-engineering
product: separation-processes
tags: [chemical-engineering, separation-processes, sep-crystallisation-drying-evaporation, msmpr-crystalliser-design, msmpr, population-balance, crystal-size-distribution, csd, growth-rate, nucleation-rate, magma-density, continuous-crystallizer, dominant-size]
level: advanced
status: draft
description: "Design a continuous MSMPR crystalliser from the population balance: growth rate, residence time, nucleation, dominant size and magma density with a worked relationship."
sources:
  - "Seader Henley and Roper Separation Process Principles, Perry Chemical Engineers Handbook separations sections, Kister Distillation Design, Treybal Mass-Transfer Operations, McCabe Smith and Harriott Unit Operations, Mullin Crystallization"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MSMPR crystalliser design

**Goal:** crystalliser volume and operating conditions to hit a product crystal size.

## Model (mixed-suspension, mixed-product removal, size-independent growth)
Population density n(L) = n0 exp(-L/(G tau)), tau the residence time, G the linear growth rate, n0 = B/G the nuclei population density (B = nucleation rate).
- **Dominant (mode of mass) size**: L_D = 3 G tau.
- **Magma density** (crystal mass per volume of slurry): M_T = 6 rho_c k_v n0 (G tau)^4, with k_v the volume shape factor (pi/6 for spheres).
- Moments give total number, surface area and mass.

## Kinetics
- Growth: G = k_g (DC)^g (often g = 1 to 2).
- Nucleation: B = k_b M_T^j (DC)^b (secondary nucleation), with parameters fitted from MSMPR laboratory data: plot ln n versus L, slope = -1/(G tau), intercept = ln n0.

## Procedure
1. Run lab MSMPR experiments at several residence times; obtain G and B.
2. For the target L_D choose tau = L_D/(3G).
3. Set M_T from the yield target (solute fed minus solubility).
4. Compute volume V = tau x slurry flow.
5. Check heat removal or evaporation duty and mixing (suspension, avoid crystal breakage).
6. Include fines destruction or classified product removal if larger size or narrower distribution is needed.

## Gotchas
- Real crystallisers have size-dependent growth, classification and attrition; MSMPR is a first estimate.
- Scale-up changes secondary nucleation via impeller tip speed.

## Verify
- [ ] ln n versus L is straight for lab data; if not, the MSMPR assumptions fail.
- [ ] Predicted magma density matches the mass balance.
