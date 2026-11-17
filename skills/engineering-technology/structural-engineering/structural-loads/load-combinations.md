---
id: engineering-technology.structural-engineering.structural-loads.load-combinations
name: load-combinations
category: engineering-technology
field: structural-engineering
product: structural-loads
tags: [structural-loads, load-combinations, lrfd, asd, ultimate-limit-state, uls, sls, serviceability, load-factors, combination-factors, psi-factors, companion-actions, asce-7, ibc, eurocode-0, en-1990, as-nzs-1170, notional-loads, pattern-loading, envelope, wind, snow, seismic, dead-load, live-load]
level: practitioner
status: verified
description: "Build LRFD/ULS and serviceability load combinations from ASCE 7, Eurocode EN 1990 and AS/NZS 1170.0: factors, companion actions, notional loads and envelope set-up."
sources:
  - "ASCE/SEI 7 Minimum Design Loads and Associated Criteria for Buildings and Other Structures (Chapter 2)"
  - "International Building Code (IBC), Chapter 16"
  - "EN 1990 Eurocode - Basis of structural design (Annex A1) and its National Annexes"
  - "AS/NZS 1170.0 Structural design actions - General principles"
  - "AISC 360 Specification for Structural Steel Buildings (Chapter C, notional loads)"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Load combinations — factored, companion and serviceability sets that actually envelope

**Goal:** a complete, code-correct set of strength and serviceability combinations
for the governing standard, entered so the software envelope captures every
critical case, including uplift, reversal and pattern live load.

The factors below are from ASCE 7-16/22, EN 1990 (first generation) with recommended
values, and AS/NZS 1170.0:2002. National Annexes and editions change values, so the
engineer of record must check the governing document. ASCE 7, EN 1990 and AS/NZS 1170 are paywalled, so all factors below are unconfirmed against the text (gated: unconfirmed, source is paywalled or blocked). A search confirmed only that EN 1990 lets a National Annex choose between 6.10 and the 6.10a/6.10b pair (Croce and Formichi, University of Pisa); a steelconstruction.info fetch returned 404.

## 1. ASCE 7 strength (LRFD), section 2.3
1. 1.4D
2. 1.2D + 1.6L + 0.5(Lr or S or R)
3. 1.2D + 1.6(Lr or S or R) + (L or 0.5W)
4. 1.2D + 1.0W + L + 0.5(Lr or S or R)
5. 0.9D + 1.0W
6. 1.2D + Ev + Eh + L + 0.2S
7. 0.9D − Ev + Eh

Rules and notes:
- W is strength-level, from the ultimate (risk-category) wind maps used since ASCE 7-10.
- Ev = 0.2·SDS·D, and Eh = ρ·QE.
- The L factor in combinations 3, 4 and 6 may be 0.5 where L₀ ≤ 100 psf, except in
  garages and places of public assembly.
- ASCE 7-22 adds tornado loads (Chapter 32), which enter in place of W where they
  apply. Re-read 2.3 for your edition.

**ASD (2.4):** D + L; D + 0.6W; D + 0.7E; D + 0.75L + 0.75(0.6W) + 0.75(Lr or S or R);
0.6D + 0.6W; 0.6D + 0.7E (with the Ev terms included).

## 2. Eurocode EN 1990, persistent and transient ULS (STR/GEO)
- **Eq. 6.10:** 1.35Gk + 1.5Qk,1 + 1.5Σψ0,i·Qk,i
- **Or the pair 6.10a/6.10b**, taking the worse:
  - 6.10a: 1.35Gk + 1.5ψ0·Qk,1 + 1.5Σψ0·Qk,i
  - 6.10b: ξ·1.35Gk + 1.5Qk,1 + 1.5Σψ0·Qk,i, with ξ = 0.85 (so 1.15Gk) as the recommended value. The UK National Annex is usually cited with ξ = 0.925 (so 1.25Gk), not 0.85 (gated: unconfirmed, source is paywalled or blocked); use the value from your National Annex.

  The UK National Annex allows the pair, which is usually more economical (gated: unconfirmed, source is paywalled or blocked).
- Favourable permanent actions take γG = 1.0. EQU checks (overturning, uplift) use
  0.9 favourable and 1.1 unfavourable.
- ψ0 (recommended): offices and residential 0.7; snow 0.5 at sites at or below
  1000 m; wind 0.6. **The UK National Annex uses 0.5 for wind** (gated: unconfirmed, source is paywalled or blocked).
- **SLS:**
  - characteristic: G + Q1 + ψ0Q
  - frequent: G + ψ1Q1 + ψ2Q
  - quasi-permanent: G + ψ2Q (offices ψ1 = 0.5 and ψ2 = 0.3), used for long-term
    deflection and crack width
- Second-generation Eurocodes (EN 1990:2023 onwards) restructure the factor
  presentation. Do not mix generations within one project.

## 3. AS/NZS 1170.0, ULS
1.35G; 1.2G + 1.5Q; 1.2G + 1.5ψl·Q (long-term); 1.2G + Wu + ψc·Q; 0.9G + Wu;
G + Eu + ψE·Q; 1.2G + Su + ψc·Q. For general floors, ψc = 0.4 and ψE = 0.3
(Table 4.1). Check Table 4.1 for storage and roofs.

## 4. Building the set in software
1. Separate load patterns by source: self-weight, SDL, partitions, L, L-reducible,
   Lr, S, W in each direction and sign (including the ASCE torsional cases and EN
   internal-pressure ±), and E in each direction including accidental torsion.
2. **Pattern live load:** where L is significant (ACI 6.4 and EC2 5.1.3), add
   checkerboard and alternate-span patterns. Uniform live load under-predicts
   midspan moments and misses reversal.
3. **Notional loads / imperfections:**
   - AISC direct analysis: 0.002·Yi at every level, in gravity-only combinations
     (and in all combinations when Δ2nd/Δ1st > 1.7 with reduced stiffness) (gated: unconfirmed, source is paywalled or blocked).
   - EC3 5.3.2: a sway imperfection φ = (1/200)·αh·αm.
4. **Each combination** must include wind or seismic in every direction and sign.
   A 0.9D + W uplift case is easy to omit by accident.
5. **Nonlinear analyses** (P-delta, tension-only bracing, gaps) must be run per
   combination. Superposing nonlinear case results is wrong.
6. Live-load reduction (ASCE 7 4.7, EN 1991-1-1 αA/αn) belongs on the L pattern,
   not as a combination factor. Never reduce roof live, storage live or assembly
   live where the code forbids it.

## 5. Gotchas
- Snow drift, rain-on-snow and ponding are separate load derivations, not combination
  factors.
- Transfer girders and columns supporting discontinuous systems may need overstrength
  (Ω0) seismic combinations (ASCE 7 12.4.3).
- Serviceability wind for drift is usually a lower return period. ASCE 7 Appendix C
  commentary suggests about 10-year wind for drift and 0.7W is sometimes used (gated: unconfirmed, source is paywalled or blocked). This is
  a judgement call, not a code mandate in ASCE 7.

## Verify
- [ ] Every code combination is present for every wind and seismic direction and sign.
- [ ] Minimum-dead (0.9D / 1.0G favourable) uplift and overturning cases are included.
- [ ] Pattern live loading is applied where live load is significant.
- [ ] Notional loads or imperfections are included per the stability method used.
- [ ] Nonlinear cases are analysed per combination, not superposed.
- [ ] ψ factors and National Annex values match the project's governing edition.
