---
id: engineering-technology.structural-engineering.seismic-design.equivalent-lateral-force-method
name: equivalent-lateral-force-method
category: engineering-technology
field: structural-engineering
product: seismic-design
tags: [seismic-design, earthquake-engineering, elf, equivalent-lateral-force, equivalent-static, base-shear, seismic-response-coefficient, cs, sds, sd1, site-class, seismic-design-category, response-modification-factor, r-factor, cd, overstrength, omega0, fundamental-period, story-drift, accidental-torsion, redundancy, p-delta, asce-7, ibc, eurocode-8, nzs-1170-5]
level: advanced
status: verified
description: "Apply the ASCE 7 equivalent lateral force procedure: site class, SDS/SD1, R/Cd/Omega0, period limits, base shear, vertical distribution, drift and irregularity checks."
sources:
  - "ASCE/SEI 7 Minimum Design Loads and Associated Criteria for Buildings and Other Structures (Chapters 11 and 12)"
  - "FEMA P-2082 NEHRP Recommended Seismic Provisions"
  - "FEMA P-2192 2020 NEHRP Recommended Seismic Provisions: Design Examples (Volume I, NIBS)"
  - "EN 1998-1 Eurocode 8 - Design of structures for earthquake resistance"
  - "Chopra, Dynamics of Structures"
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Equivalent lateral force (ELF) — seismic base shear, done in the right order

**Goal:** compute and distribute the ASCE 7 design base shear for a building. Then
apply the drift, torsion, redundancy and stability checks that make the number
meaningful, and confirm ELF is permitted at all.

Values are ASCE 7-16, with the ASCE 7-22 differences flagged. US units, with heights
in feet. The engineer of record must confirm the adopted edition (via the IBC or the
local code). ASCE 7 is paywalled and the free FEMA PDFs were not reachable, so every table value and clause number below is unconfirmed against the text (gated: unconfirmed, source is paywalled or blocked). Verified this session: FEMA P-2082-1 is "2020 NEHRP Recommended Seismic Provisions for New Buildings and Other Structures, Volume I" (BSSC/NIBS, improvements to ASCE 7-16), and the 2020 design examples are FEMA P-2192 (NIBS).

## 1. Hazard and category
1. **Risk Category** (Table 1.5-1) gives the importance factor Ie: 1.0 for I/II, 1.25
   for III, 1.5 for IV.
2. **Site class** from the geotechnical report (vs30, N or su).
3. **Spectral values:**
   - ASCE 7-16: SMS = Fa·SS, SM1 = Fv·S1, SDS = (2/3)SMS and SD1 = (2/3)SM1.
     Site class D with S1 ≥ 0.2 requires a site-specific analysis unless you use the
     11.4.8 exception, which raises Cs in the long-period range.
   - ASCE 7-22: use the multi-period spectra and the SDS/SD1 values returned directly
     by the ASCE Hazard Tool (USGS data). It adds the intermediate site classes BC, CD
     and DE, and drops the Fa/Fv tables. How 7-22 words the ELF
     Cs equations against the multi-period spectrum is unconfirmed (gated: unconfirmed, source is paywalled or blocked); read 12.8.1 in that edition.
4. **Seismic Design Category** (Tables 11.6-1 and 11.6-2) is the worse of the SDS and
   SD1 results. It controls permitted systems, height limits, detailing and analysis.

## 2. System and coefficients (Table 12.2-1)
Typical values (check the row, the height limits and the detailing standard):

| System | R | Ω0 | Cd |
|---|---|---|---|
| Special steel moment frame | 8 | 3 | 5.5 |
| Special RC moment frame | 8 | 3 | 5.5 |
| Special concentrically braced frame (SCBF) | 6 | 2 | 5 |
| BRBF (non-moment beam-column connections) | 8 | 2.5 | 5 |
| Special RC shear wall (bearing wall) | 5 | 2.5 | 5 |

Vertical combinations of systems follow 12.2.3.

## 3. Period
- Ta = Ct·hn^x:

  | System | Ct | x |
  |---|---|---|
  | Steel moment frame | 0.028 | 0.8 |
  | Concrete moment frame | 0.016 | 0.9 |
  | Eccentrically braced frame and BRBF | 0.03 | 0.75 |
  | All others | 0.02 | 0.75 |

- The analytical T may be used for **forces** only up to Cu·Ta. Cu = 1.4 when
  SD1 ≥ 0.3, rising to 1.7 when SD1 ≤ 0.1.

## 4. Base shear: V = Cs·W
- Cs = SDS/(R/Ie), but not more than SD1/(T·R/Ie) for T ≤ TL.
- Cs is at least 0.044·SDS·Ie and at least 0.01.
- Where S1 ≥ 0.6, Cs is also at least 0.5·S1/(R/Ie).
- **W** is dead load plus:
  - 25% of storage live;
  - partitions at the greater of the actual load or 10 psf;
  - operating equipment;
  - 20% of flat roof snow where it exceeds 30 psf.

## 5. Vertical distribution and torsion
- Fx = Cvx·V, with Cvx = wx·hx^k / Σ(wi·hi^k).
- k = 1 for T ≤ 0.5 s and 2 for T ≥ 2.5 s, linear in between.
- Apply a **5% accidental eccentricity** of the plan dimension at each level.
- In SDC C–F with torsional irregularity (Type 1a/1b), amplify it by
  Ax = (δmax / 1.2δavg)², limited to 1 ≤ Ax ≤ 3.

## 6. Is ELF allowed? (Table 12.6-1)
- In SDC D–F, ELF is not permitted when T ≥ 3.5Ts (Ts = SD1/SDS).
- It is also not permitted with certain horizontal irregularities (1a, 1b) or
  vertical irregularities (1a, 1b, 2, 3). In those cases use modal response spectrum
  analysis.

## 7. Redundancy, drift, stability
- **Redundancy:** ρ = 1.0 or 1.3 (12.3.4). Removing a single brace or wall must not
  cut strength by more than 33% or create an extreme torsional irregularity.
- **Drift:** δx = Cd·δxe/Ie, at the edges of the plan when torsion is present.
  - Drift calculations may use the computed T without the Cu·Ta cap (12.8.6.2).
  - Limits (Table 12.12-1), for Risk Category I/II, III and IV respectively: "all
    other structures" 0.020, 0.015 and 0.010 hsx; buildings of 4 stories or fewer
    with drift-tolerant interior walls 0.025, 0.020 and 0.015 hsx.
  - In SDC D–F, moment-frame limits are divided by ρ.
- **Stability coefficient:** θ = Px·Δ·Ie / (Vx·hsx·Cd).
  - θ ≤ 0.10: P-delta may be ignored.
  - Otherwise θ must not exceed θmax = 0.5/(β·Cd) ≤ 0.25. Check whether your
    edition revised this (gated: unconfirmed, source is paywalled or blocked).

## 8. Load combination
Eh = ρ·QE and Ev = 0.2·SDS·D enter the strength combinations (see `load-combinations`).
Collectors, discontinuous-element supports and some connections need Ω0·QE.

## 9. Eurocode 8, briefly
The EC8 lateral force method uses Fb = Sd(T1)·m·λ, with λ = 0.85 when T1 ≤ 2Tc and
more than two storeys. The behaviour factor q replaces R.

## Verify
- [ ] Risk Category, Ie, site class and SDS/SD1 come from the governing edition's data source.
- [ ] The system row in Table 12.2-1 is allowed for the SDC and height. R, Ω0 and Cd are recorded.
- [ ] T for forces ≤ Cu·Ta, and every Cs minimum and maximum is checked.
- [ ] Irregularities are evaluated and ELF is permitted (otherwise use RSA).
- [ ] Accidental torsion, Ax and ρ are applied.
- [ ] Amplified drift is within limits and θ is checked at every story.
