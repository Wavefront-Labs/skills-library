---
id: engineering-technology.chemical-engineering.reactor-design.thiele-modulus-and-effectiveness-factor
name: thiele-modulus-and-effectiveness-factor
category: engineering-technology
field: chemical-engineering
product: reactor-design
tags: [chemical-engineering, reactor-design, rx-catalytic-reactors, thiele-modulus-and-effectiveness-factor, thiele-modulus, effectiveness-factor, internal-diffusion, catalyst-pellet, pore-diffusion, intraparticle-diffusion, effective-diffusivity, catalyst-sizing]
level: advanced
status: verified
description: "Compute Thiele modulus and internal effectiveness factor for catalyst pellets of various shapes, correct observed rates, and choose pellet size and shape."
sources:
  - "Fogler Elements of Chemical Reaction Engineering, Levenspiel Chemical Reaction Engineering, Froment Bischoff and De Wilde Chemical Reactor Analysis and Design"
  - "https://www.aiche.org"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Thiele modulus and effectiveness factor

**Goal:** know how much of the catalyst is used and choose pellet size accordingly.

## First-order, isothermal pellet
- Slab (half thickness L): phi = L sqrt(k / D_e); eta = tanh(phi) / phi.
- Sphere (radius R): phi_s = (R/3) sqrt(k / D_e) (generalised modulus); eta = (1/phi_s)[1/tanh(3 phi_s) - 1/(3 phi_s)] (checked by solving the spherical pellet boundary-value problem numerically: eta = 0.950, 0.672, 0.296 at phi_s = 0.3, 1, 3, matching the formula).
- High modulus (phi > about 3): eta approaches 1/phi (tanh(3)/3 = 0.332 against 1/3), so the observed rate varies as the square root of k times D_e; the apparent activation energy is about half the true value.

## Effective diffusivity
D_e = D_pore eps_p / tau, with eps_p the particle porosity and tau tortuosity (often about 2 to 6 (gated: unconfirmed, source is paywalled or blocked)), and D_pore combining molecular and Knudsen diffusion (1/D = 1/D_M + 1/D_K) when pores are small (below about 0.1 micron at low pressure (gated: unconfirmed, source is paywalled or blocked)).

## Procedure
1. Get k per unit particle volume at the reaction temperature from kinetics measured on crushed particles.
2. Estimate D_e (or measure).
3. Compute phi and eta for candidate particle sizes.
4. Choose a size giving eta above about 0.8 to 0.9 (gated: unconfirmed, source is paywalled or blocked) if pressure drop allows; otherwise use shaped pellets (rings, trilobes) or egg-shell catalyst where the active metal sits near the surface.
5. For non-first-order or non-isothermal pellets, solve numerically.

## Gotchas
- Using rate per catalyst mass without converting to per-volume.
- Strongly exothermic reactions can have eta above 1 within the particle (internal temperature rise).

## Verify
- [ ] Observed rates on crushed and whole pellets compared: the ratio gives eta experimentally.
- [ ] Particle size selection documented with both dP and eta.
