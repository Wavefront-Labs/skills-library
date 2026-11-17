---
id: engineering-technology.nuclear-engineering.radiation-shielding.point-kernel-shield-sizing
name: point-kernel-shield-sizing
category: engineering-technology
field: nuclear-engineering
product: radiation-shielding
tags: [radiation-shielding, point-kernel, gamma-shielding, attenuation-coefficient, buildup-factor, geometric-progression-buildup, ansi-ans-6-4-3, hvl, tvl, half-value-layer, microshield, qad, dose-rate, flux-to-dose-conversion, icrp-74, gamma-constant, streaming, skyshine, alara, concrete, lead, shield-design]
level: practitioner
status: gated
description: "Size gamma shields with point-kernel methods: attenuation, buildup factors (G-P fits), HVL/TVL, flux-to-dose conversion, MicroShield setup, plus streaming and skyshine checks for ALARA design."
sources:
  - "ANSI/ANS-6.4.3-1991, Gamma-Ray Attenuation Coefficients and Buildup Factors for Engineering Materials"
  - "Shultis & Faw, Radiation Shielding"
  - "NCRP Report No. 151, Structural Shielding Design for Megavoltage X- and Gamma-Ray Radiotherapy Facilities"
  - "ICRP Publication 74, Conversion Coefficients for use in Radiological Protection"
  - "NIST XCOM photon cross-section database"
  - "MicroShield User's Manual (Grove Software)"
  - "10 CFR Part 20, Standards for Protection Against Radiation"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Point-kernel shield sizing — how thick, and is it enough

**Goal:** size a gamma shield (concrete, steel, lead, water) to meet a dose-rate target, with a defensible point-kernel calculation and the checks that catch streaming and skyshine.

Engineering guidance only; shield designs for licensed facilities need review by a qualified health physicist/shielding engineer against the governing regulation.

## 1. Set the target

Start from the area classification and occupancy. In the US, 10 CFR 20 limits occupational whole-body dose to 0.05 Sv (5 rem)/yr (20.1201) and members of the public to 1 mSv (0.1 rem)/yr, with ≤0.02 mSv (0.002 rem) in any one hour in unrestricted areas (20.1301; confirmed in the eCFR). Design targets are set well below limits (ALARA) — commonly a fraction of the limit with an occupancy factor applied. Write the target as a dose rate at a stated point (e.g. 10 µSv/h at 30 cm from the shield face).

## 2. Source term

Photon emission rate S (photons/s) per energy group, from the activity and yields (or from ORIGEN for spent fuel / activation, see engineering-technology.nuclear-engineering.fuel-cycle-engineering.spent-fuel-dry-cask-storage-checks). Quick check with gamma constants (unshielded, approximate): Co-60 ≈ 1.3 R/h at 1 m per Ci (about 0.35 mSv/h at 1 m per GBq, taking 1 R as about 0.01 Sv) (gated: unconfirmed, source is paywalled or blocked); Cs-137 ≈ 0.33 R/h at 1 m per Ci (gated: unconfirmed, source is paywalled or blocked). Gamma constants are quoted in several units and dose quantities — confirm which before using one.

## 3. Point-kernel equation

For an isotropic point source of energy E behind a slab:

φ = S · B(E, μx) · exp(−μx) / (4π r²)

- μ = (μ/ρ)·ρ from XCOM or ANSI/ANS-6.4.3. At 1 MeV: lead μ/ρ = 0.07102 cm²/g (NIST XCOM table) → μ ≈ 0.81 /cm at 11.35 g/cm³; ordinary concrete (2.3 g/cm³) μ/ρ = 0.06495 cm²/g (NIST) → μ ≈ 0.149 /cm.
- r = total source-to-detector distance; x = slant path through the shield (x = t / cos θ).
- **Buildup factor B** accounts for scattered photons. Use the geometric-progression (G-P) fit from ANSI/ANS-6.4.3 (valid to ~40 mfp) for the material and response (exposure/dose). B is large: for concrete at 1 MeV and 10 mfp, B is of order 20-40 (gated: unconfirmed, source is paywalled or blocked) — ignoring it under-predicts dose by more than an order of magnitude.
- Volume sources: integrate kernels over the source (MicroShield, QAD-CGGP, or numeric integration) and include self-shielding in the source material.

Convert flux to dose with ICRP-74 H*(10) or ANSI/ANS-6.1.1 coefficients. Rule of thumb: at 1 MeV, ~1.9 µrem/h (0.019 µSv/h) per photon/(cm²·s) (gated: unconfirmed, source is paywalled or blocked).

## 4. Quick sizing with HVL/TVL

Broad-beam TVLs (approximate, check the reference for your energy and geometry):

| Source | Lead TVL | Concrete TVL |
|---|---|---|
| Cs-137 (0.662 MeV) | ~2.2 cm (gated: unconfirmed, source is paywalled or blocked) | ~16 cm (gated: unconfirmed, source is paywalled or blocked) |
| Co-60 (1.17/1.33 MeV) | ~4-4.6 cm (gated: unconfirmed, source is paywalled or blocked) | ~21 cm (gated: unconfirmed, source is paywalled or blocked) |

Thickness ≈ TVL · log10(unshielded / target dose rate). Use for first sizing only; first TVL is often larger than the equilibrium TVL.

## 5. MicroShield / point-kernel code setup

- Choose geometry matching the source (cylinder, rectangular volume, disk).
- Energy grouping: let the code group the nuclide library, but check high-energy lines (e.g. Co-60, N-16 at 6.1 MeV) are not diluted into a lower group.
- **Buildup material:** for multilayer shields pick the material that dominates the attenuation, usually the outermost thick layer; run sensitivities with each candidate and take the bounding one.
- Report the response (deep dose equivalent vs. exposure) consistent with the target.

## 6. Streaming and skyshine

- **Penetrations:** ducts, cable trays, door gaps and pipe sleeves bypass the slab. Use dog-leg (offset) paths with at least one bend, step-plug gaps and stagger joints; shadow shields behind penetrations. Point kernel cannot model streaming — use Monte Carlo (engineering-technology.nuclear-engineering.mcnp.building-an-mcnp-input-deck) or albedo methods.
- **Skyshine:** radiation going up through a thin roof scatters in air back to ground at distance. If the roof is thinner than the walls, compute skyshine (empirical NCRP 151 / SKYSHINE-type codes or MCNP) at the site boundary.
- Neutron sources (fuel, accelerators) need hydrogenous material and capture-gamma accounting; point kernel with removal cross-sections is only a scoping tool.

## Gotchas

- Using narrow-beam μ without buildup is the most common gross under-design.
- Slant-path thickness grows with angle; but so does r — check the off-normal dose point.
- Concrete density and moisture vary (2.2-2.4 g/cm³); specify and verify the as-built density.
- G-P buildup fits degrade beyond ~40 mfp and in multilayer geometries; add margin or confirm with Monte Carlo.
- Daughter photons (e.g. Ba-137m for Cs-137) must be in the source.

## Verify

- [ ] Source spectrum includes all significant lines and daughters, with activity date stated.
- [ ] Buildup factors used, with material choice justified for each layer.
- [ ] Hand point-kernel and code results agree within ~20-30% for a simple configuration.
- [ ] All penetrations, gaps and doors reviewed for streaming; roof checked for skyshine.
- [ ] Calculated dose rate at each target point below the ALARA design target with stated margin and occupancy.
- [ ] Post-installation survey plan defined to confirm the as-built shield.
