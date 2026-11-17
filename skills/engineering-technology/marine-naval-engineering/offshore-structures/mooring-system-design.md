---
id: engineering-technology.marine-naval-engineering.offshore-structures.mooring-system-design
name: mooring-system-design
category: engineering-technology
field: marine-naval-engineering
product: offshore-structures
tags: [offshore-structures, mooring, spread-mooring, catenary, taut-leg, chain, polyester, wire-rope, anchor, drag-anchor, suction-anchor, dnv-os-e301, api-rp-2sk, iso-19901-7, uls, als, fls, partial-safety-factor, metocean, offset, slow-drift, fpso, semi-submersible, floating-wind, orcaflex]
level: advanced
status: gated
description: "Spread-mooring design for a floater: catenary line tensions, metocean load cases, intact/damaged checks to DNV-OS-E301 partial factors or API RP 2SK safety factors."
sources:
  - "DNV-OS-E301 Position mooring (current edition)"
  - "API RP 2SK Design and Analysis of Stationkeeping Systems for Floating Structures"
  - "ISO 19901-7 Stationkeeping systems for floating offshore structures and mobile offshore units"
  - "Faltinsen, Sea Loads on Ships and Offshore Structures (Cambridge University Press)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Mooring system design (spread mooring)

**Goal:** select line make-up, pattern and pretension so the floater stays within its
offset limits (risers, gangway) and every line and anchor passes intact and one-line-
damaged checks under the design storm.

## 1. Basis of design
1. **Metocean:** the governing combinations for ULS typically use a 100-year
   return period (e.g. 100-yr waves with 10-yr wind and current, and the permutations
   the standard lists); confirm the combinations in your standard and site study.
   Include directions: collinear and non-collinear.
2. **Offset limits** from riser/umbilical analysis (project specific, set by riser analysis; no typical value claimed).
3. **Consequence class** (DNV): CC1 if failure is unlikely to cause loss of life,
   collision or pollution; CC2 otherwise.

## 2. Static line design (catenary)
For a chain segment resting on the seabed, with submerged weight per metre w, water
depth h and horizontal tension H:
- Suspended length s = sqrt(h (h + 2H/w)).
- Fairlead (top) tension T = H + w h.
- Horizontal span of the suspended part x = (H/w) asinh(s w / H).
Typical make-up: chain-polyester-chain for deep water (polyester must never touch the
seabed), all-chain in shallow water. Pretension is a design choice (the example below gives 16 % of MBS).

## 3. Loads and response
1. Mean: wind, current, mean wave drift.
2. Low-frequency (slow-drift) motion near the mooring's natural period (minutes),
   driven by second-order difference-frequency forces; damping is critical and
   uncertain.
3. Wave-frequency motion from RAOs.
4. Run quasi-static (simple screening only), frequency-domain, or coupled
   time-domain analysis (e.g. OrcaFlex-type tools). DNV expects dynamic analysis for
   line tensions; use enough 3-hour seeds (number per the standard, gated: unconfirmed) and take the
   most-probable maximum.

## 4. Checks (DNV-OS-E301 style, ULS)
Form note: the 2018-era DNV-OS-E301 check (after the NorMoor project) is written as u = (T_pre x gamma_pret + T_C,env x gamma_env) / S_C < 1 (pretension and characteristic environmental tension; SINTEF SIMA documentation). The mean/dynamic split and consequence classes below follow the older Posmoor-style text; the factor values are gated and must be replaced by the values in the edition you design to.
Design tension Td = gamma_mean x T_c,mean + gamma_dyn x T_c,dyn <= S_C,
with S_C = 0.95 x MBS for chain (gated: unconfirmed) (other components per the standard).
- ULS CC1: gamma_mean = 1.10, gamma_dyn = 1.50 (gated: unconfirmed, source is paywalled or blocked).
- ULS CC2: gamma_mean = 1.40, gamma_dyn = 2.10 (gated: unconfirmed, source is paywalled or blocked).
- ALS (one line broken): 1.00 / 1.00 for CC1, 1.00 / 1.25 for CC2 (gated: unconfirmed, source is paywalled or blocked).
Confirm in the edition you design to (DNV-OS-E301 or ISO 19901-7 Annex B.2).

API RP 2SK alternative (safety factor on MBS): intact dynamic analysis 1.67, one line damaged 1.25, transient 1.05; quasi-static 2.00 intact, 1.43 damaged (gated: unconfirmed, source is paywalled or blocked).

Also check FLS (fatigue with T-N or S-N curves), anchor holding capacity and
**no uplift at a drag anchor** in intact and damaged cases.

## Worked mini-example
(Recomputed: w 2.446 kN/m, MBS 13,573 kN, s 676.7 m, T 2,234 kN, Td 6,958 kN, utilisation 0.54; catenary relations are standard statics.)
h = 300 m, studless R4 chain 120 mm.
- Mass about 0.0199 d^2 = 287 kg/m; submerged about 0.87 x that: w = 2.45 kN/m.
- MBS (R4) about 0.0274 d^2 (44 - 0.08 d) = 13 600 kN.
- At H = 1500 kN: s = sqrt(300 x (300 + 2 x 1500/2.45)) = 676 m; T = 1500 + 2.45 x 300
  = 2235 kN (16 % MBS pretension).
- Storm: T_mean = 2235 kN, T_dyn = 3000 kN, CC1:
  Td = 1.1 x 2235 + 1.5 x 3000 = 6960 kN; S_C = 0.95 x 13 600 = 12 920 kN:
  utilisation 0.54, pass. Check that the ground length still exceeds the touchdown
  excursion so the anchor sees no uplift.

## Gotchas
- **Corrosion and wear:** reduce chain diameter for corrosion over the design life
  (splash and touchdown zones worst; rates per the standard or field data), and check
  ULS with the corroded diameter.
- Polyester stiffness is load- and time-dependent; run offsets with lower (post-
  installation) and tensions with upper (storm) stiffness.
- One-line-damaged transient: the floater can overshoot; check offsets and riser
  clearances in the transient, not only the new equilibrium.
- Chain catalogue weights and MBS formulas vary slightly by grade and maker; use
  the certified values.

## Verify
- [ ] Metocean combinations and directions match the standard and site data.
- [ ] Intact and one-line-damaged offsets within riser limits.
- [ ] Design tensions use the right consequence-class factors (or API SFs).
- [ ] Corroded-diameter ULS check done; FLS life >= design life x factor.
- [ ] No drag-anchor uplift; polyester clear of seabed in all cases.
