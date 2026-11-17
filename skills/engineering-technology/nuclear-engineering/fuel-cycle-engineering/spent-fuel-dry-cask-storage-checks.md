---
id: engineering-technology.nuclear-engineering.fuel-cycle-engineering.spent-fuel-dry-cask-storage-checks
name: spent-fuel-dry-cask-storage-checks
category: engineering-technology
field: nuclear-engineering
product: fuel-cycle-engineering
tags: [fuel-cycle-engineering, spent-fuel, dry-cask-storage, isfsi, decay-heat, ans-5-1, origen, scale, cladding-temperature, isg-11, burnup-credit, isg-8, criticality-safety, keno, dose-rate, 10-cfr-72, nureg-2215, nureg-2224, high-burnup-fuel, vacuum-drying, canister-loading, fuel-qualification]
level: advanced
status: gated
description: "Check a spent-fuel dry storage loading: decay heat (ANS-5.1/ORIGEN), 400 C cladding limit per ISG-11, burnup-credit criticality, and dose rates against 10 CFR 72 and NUREG-2215."
sources:
  - "ANSI/ANS-5.1-2014, Decay Heat Power in Light Water Reactors"
  - "SCALE Code System manual (ORIGEN, ORIGAMI, KENO, MAVRIC)"
  - "NUREG-2215, Standard Review Plan for Spent Fuel Dry Storage Systems and Facilities"
  - "NUREG-2224, Dry Storage and Transportation of High Burnup Spent Nuclear Fuel"
  - "US NRC Interim Staff Guidance ISG-11 Rev 3, Cladding Considerations for the Transportation and Storage of Spent Fuel"
  - "US NRC ISG-8 Rev 3, Burnup Credit in the Criticality Safety Analyses of PWR Spent Fuel"
  - "US NRC Regulatory Guide 3.54, Spent Fuel Heat Generation in an ISFSI"
  - "10 CFR Part 72, Licensing Requirements for Independent Storage of Spent Nuclear Fuel"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Spent-fuel dry cask storage checks — will this loading fit the licence

**Goal:** confirm that a proposed set of assemblies can be loaded into a licensed dry storage canister: within heat-load limits so cladding stays below its temperature limit, subcritical with credited burnup, and within dose limits at the site boundary.

Engineering guidance only. Every loading must comply with the specific Certificate of Compliance (CoC) or site licence and its Technical Specifications; this checklist does not replace the licensed analyses or a qualified reviewer.

## 1. Characterise each assembly

For every assembly record: type, initial enrichment, assembly-average burnup (with measurement uncertainty), cooling time, irradiated hardware/inserts (BPRAs, thimble plugs, control components), and condition (intact, damaged, failed). Damaged fuel goes into damaged-fuel cans per the CoC. High burnup fuel (> 45 GWd/MTU) triggers the extra cladding considerations of NUREG-2224 (gated: unconfirmed, source is paywalled or blocked).

## 2. Decay heat

- Compute with ORIGEN (SCALE ORIGEN/ORIGAMI) using the actual power history, or with ANSI/ANS-5.1-2014 for fission-product heat plus actinides and activation. RG 3.54 gives an accepted method and safety factors (gated: unconfirmed, source is paywalled or blocked).
- Order of magnitude: a PWR assembly at ~45 GWd/MTU and ~5 years cooling produces roughly 1 kW; typical canister limits are ~20-45 kW total (gated: unconfirmed, source is paywalled or blocked). Treat these as scoping values only.
- Compare per-assembly heat to the CoC's **zone loading** map (hotter assemblies often allowed only in specific basket cells) and to the total canister limit.
- Include inserts' heat and gamma source where the CoC requires.

## 3. Cladding temperature (thermal)

- ISG-11 Rev 3 criterion: peak cladding temperature ≤ **400 °C** for normal storage and short-term loading operations (vacuum drying, backfill, transfer) (gated: unconfirmed, source is paywalled or blocked). A higher limit may be justified for low-burnup fuel if hoop stress is shown to stay below ~90 MPa (gated: unconfirmed, source is paywalled or blocked). Off-normal and accident limit: **570 °C** (gated: unconfirmed, source is paywalled or blocked). (The NRC document host blocked automated fetching; confirm in the current ISG.)
- During drying, limit repeated thermal cycling (ISG-11: ≤10 cycles, each < 65 °C swing (gated: unconfirmed, source is paywalled or blocked)) to avoid hydride reorientation.
- Licensed thermal models (ANSYS Fluent, STAR-CCM+, COBRA-SFS) bound the heat-load pattern; a loading within the CoC map inherits that result. Watch time limits for vacuum drying and transfer cask operations (time-to-boil, time-to-limit), especially for high heat loads where forced helium dehydration may be required.

## 4. Criticality and burnup credit

- Criterion: k-eff + biases + uncertainties ≤ 0.95 (gated: unconfirmed, source is paywalled or blocked) (upper subcritical limit from code validation) under the most reactive credible conditions — for wet loading this means the canister flooded with pool water (PWR canisters may credit soluble boron per the CoC).
- **Burnup credit** (ISG-8 Rev 3): actinide-only or actinide-plus-fission-product credit with validated isotopic depletion (ORIGEN/TRITON) and criticality code (KENO, MCNP), bounding axial burnup profiles (end effect), horizontal profiles, depletion parameters (high fuel/moderator temperature, burnable absorbers present) and burnup uncertainty.
- Each assembly must satisfy the **loading curve**: minimum burnup as a function of initial enrichment and cooling time. Verify burnup by records plus a misload check (some designs require measurement or a misload analysis).
- Cross-reference engineering-technology.nuclear-engineering.reactor-physics.core-criticality-and-reactivity-coefficients for k-eff fundamentals and engineering-technology.nuclear-engineering.mcnp.building-an-mcnp-input-deck for Monte Carlo practice.

## 5. Dose rates

- Source terms (neutron and gamma, including Co-60 activation in end fittings) from ORIGEN; transport with MCNP or SCALE/MAVRIC to cask surface, vents and the site boundary (including skyshine for arrays).
- 10 CFR 72.104 (eCFR, confirmed): ≤ 0.25 mSv (25 mrem)/yr whole body (0.75 mSv thyroid, 0.25 mSv any other critical organ) to a real individual at or beyond the controlled-area boundary from normal operations and anticipated occurrences; 72.106 (confirmed): design-basis accident dose ≤ 0.05 Sv (5 rem) TEDE at the controlled-area boundary, which must be at least 100 m from the spent fuel.
- Measure as-loaded dose rates at the CoC-specified points and compare to the Tech Spec limits; deviations point to misload or unexpected source.
- ALARA during loading: transfer cask, lid welding and drying are the dose-intensive steps — see engineering-technology.nuclear-engineering.radiation-shielding.point-kernel-shield-sizing.

## Gotchas

- Assembly-average burnup overstates credit at the low-burnup ends; that is why bounding axial profiles exist.
- Short cooling times raise neutron and gamma sources faster than the heat load suggests (Cm-244 dominates neutrons and grows strongly with burnup).
- Non-fuel hardware can push heat or dose over a zone limit on its own.
- Reconstituted or rods-removed assemblies may not be covered by the CoC; check before planning.
- CoC amendments change loading maps — use the amendment the cask was actually loaded under.

## Verify

- [ ] Every assembly's enrichment, burnup, cooling time and condition verified against plant records and CoC contents.
- [ ] Per-cell and total decay heat within the zone-loading and canister limits.
- [ ] Drying and transfer plans keep peak cladding ≤ 400 °C with thermal-cycling limits respected.
- [ ] Every assembly meets the burnup-credit loading curve; misload check documented.
- [ ] Measured cask dose rates within Tech Spec limits; site-boundary dose meets 10 CFR 72.104 with the new casks.
- [ ] Independent second check of the loading plan signed off before fuel movement.
