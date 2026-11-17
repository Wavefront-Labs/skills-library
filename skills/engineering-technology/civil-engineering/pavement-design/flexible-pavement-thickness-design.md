---
id: engineering-technology.civil-engineering.pavement-design.flexible-pavement-thickness-design
name: flexible-pavement-thickness-design
category: engineering-technology
field: civil-engineering
product: pavement-design
tags: [pavement-design, flexible-pavement, asphalt-pavement, granular-pavement, esal, esa, design-traffic, fourth-power-law, structural-number, aashto-93, aashto-guide-1993, mepdg, pavement-me, austroads, agpt02, circly, mechanistic-empirical, cbr, resilient-modulus, subgrade, layer-coefficients, reliability, asphalt-fatigue, subgrade-strain, sprayed-seal]
level: practitioner
status: verified
description: "Design a new flexible pavement: traffic as ESALs/ESAs, subgrade CBR or resilient modulus, layer thickness via AASHTO 93 SN or Austroads mechanistic method, and checks."
sources: ["AASHTO Guide for Design of Pavement Structures (1993)", "AASHTO Mechanistic-Empirical Pavement Design Guide: A Manual of Practice", "Austroads Guide to Pavement Technology Part 2: Pavement Structural Design (AGPT02)", "Huang, Pavement Analysis and Design", "Yoder & Witczak, Principles of Pavement Design"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Flexible pavement thickness design — traffic, subgrade, then layers

**Goal:** a new asphalt or granular pavement whose layer thicknesses carry the design
traffic over the design period on the actual subgrade, with the method your road
authority adopts (AASHTO 93 empirical, AASHTO MEPDG, or Austroads mechanistic-empirical).

## 1. Design traffic
1. Start from AADT, % heavy vehicles, growth rate and design period (commonly 20 years
   for flexible pavements; 30–40 for heavy-duty asphalt — authority-specific) (gated: unconfirmed, source is paywalled or blocked).
2. Convert heavies to standard axles. **US:** ESAL = 18-kip (80 kN) single axle.
   **Australia:** ESA = 80 kN single axle with dual tyres (SADT); Austroads design
   traffic is DESA, with load damage exponents per distress mode (4 for granular/
   subgrade, 5 for asphalt fatigue, 12 for cemented layers) (gated: unconfirmed, source is paywalled or blocked).
3. Apply directional and lane distribution factors (design lane only).
4. Cumulative growth factor: [(1 + r)^n − 1] / r.
**Fourth-power law:** doubling an axle load does ~16 times the damage (2^4 = 16). One overloaded
truck can do the work of thousands of cars; car traffic is negligible structurally.

## 2. Subgrade
- Design CBR from soaked laboratory CBR (or DCP correlations) at the expected moisture
  and density, taken as a low percentile (e.g. 10th) of tested values, not the mean.
- **Resilient modulus:** AASHTO 93 often uses M_R (psi) ≈ 1500 × CBR (Heukelom &
  Klomp), valid only for fine-grained soils at low CBR (≤ ~10) (gated: unconfirmed, source is paywalled or blocked); NCDOT converts CBR with M_R = 2555 CBR^0.64. Austroads presumes
  E ≈ 10 × CBR (MPa) for the subgrade, capped at a maximum (gated: unconfirmed, source is paywalled or blocked).
- CBR < 3: treat the subgrade (lime/cement stabilisation, select fill capping layer)
  before thickness design; the design methods assume a working platform.

## 3a. AASHTO 1993 (US empirical)
log₁₀W₁₈ = Z_R·S₀ + 9.36·log₁₀(SN+1) − 0.20 + log₁₀[ΔPSI/(4.2−1.5)] / [0.40 + 1094/(SN+1)^5.19] + 2.32·log₁₀M_R − 8.07

- Equation matches FHWA NHI-05-037 Appendix C (fetched). Z_R ≈ −1.037 for 85% and −1.645 for 95% (computed from the normal distribution); S₀ typically 0.35 to 0.50, 0.45 commonly used (FHWA).
- ΔPSI = p₀ − p_t, e.g. 4.2 − 2.5 = 1.7.
- Solve for the required SN, then choose layers: SN = a₁D₁ + a₂D₂m₂ + a₃D₃m₃.
  Typical layer coefficients: dense HMA a₁ ≈ 0.4 to 0.44 (FHWA); crushed-stone base a₂ ≈ 0.14 (NCDOT aggregate base course 0.14);
  granular subbase a₃ ≈ 0.11 (gated: unconfirmed, source is paywalled or blocked) (per inch). Drainage coefficients m ≈ 0.8–1.2 (gated: unconfirmed, source is paywalled or blocked).
- Design **top-down**: required SN above the base (using base modulus) sets the
  asphalt thickness, then above subbase, then above subgrade.
- Apply minimum thicknesses by traffic level (e.g. 3–4 in asphalt for heavy traffic (gated: unconfirmed, source is paywalled or blocked)).
- Many US states now use **AASHTOWare Pavement ME** (MEPDG) instead: it predicts
  rutting, cracking and IRI against thresholds rather than solving for SN.

## 3b. Austroads AGPT02 (Australia/NZ)
- **Granular pavement with thin bituminous surfacing:** use the empirical design chart
  (thickness of granular cover over subgrade vs DESA and subgrade CBR).
- **Asphalt or cemented layers:** mechanistic-empirical — model the layers as linear
  elastic (CIRCLY), compute the critical strains under the standard axle, and check:
  - horizontal tensile strain at the bottom of asphalt → asphalt fatigue life;
  - vertical compressive strain at top of subgrade → permanent deformation life;
  - cemented layers: tensile strain → fatigue.
  Allowable repetitions ≥ design traffic for each mode.
- Granular layers are sublayered with modulus limited by the support beneath (Austroads
  sublayering rules); don't assign a high modulus to a thick granular layer on soft
  subgrade.

## 4. Practical checks
- Drainage: subsurface drains and a crossfall of ~3% on granular surfaces (gated: unconfirmed, source is paywalled or blocked); moisture
  entry is the commonest cause of early failure of granular pavements.
- Frost (US/Europe north): check frost-protection depth independently of structural SN.
- Constructability: minimum compacted lift (asphalt layer ≥ ~2.5–3 × nominal maximum
  aggregate size; granular 100–200 mm per lift) (gated: unconfirmed, source is paywalled or blocked).

## Gotchas
- Using the mean subgrade CBR, or soaked vs unsoaked mix-ups, changes thickness a lot.
- Mixing AASHTO SN with Austroads traffic (ESA vs ESAL definitions and damage exponents)
  gives meaningless results; stay within one method.
- The 1500 × CBR rule is widely criticised; use measured M_R if available.

## Verify
- [ ] Design traffic in standard axles, design lane only, with growth and design period stated.
- [ ] Subgrade design value is a conservative percentile under realistic moisture.
- [ ] One method used consistently (AASHTO 93, Pavement ME, or Austroads) with its own inputs.
- [ ] Each distress criterion (SN, or fatigue and subgrade strain) is satisfied for design traffic.
- [ ] Minimum thicknesses, lift thicknesses and drainage provisions met.
