---
id: natural-sciences.chemistry.polymer-chemistry.gpc-sec-molecular-weight-analysis
name: gpc-sec-molecular-weight-analysis
category: natural-sciences
field: chemistry
product: polymer-chemistry
tags: [polymer-chemistry, gpc, sec, gel-permeation-chromatography, size-exclusion-chromatography, molecular-weight, molar-mass, mn, mw, dispersity, polydispersity-index, pdi, conventional-calibration, polystyrene-standards, pmma-standards, universal-calibration, mark-houwink, viscometry-detector, mals, multi-angle-light-scattering, dn-dc, refractive-index-detector, thf, dmf-licl, hfip, raft, atrp, controlled-polymerisation]
level: practitioner
status: draft
description: "Get trustworthy polymer molecular weights from GPC/SEC: conventional vs universal vs light-scattering calibration, sample prep, Mn/Mw/dispersity, and reading the trace."
sources: ["S. Mori & H. G. Barth, Size Exclusion Chromatography (Springer, 1999)", "IUPAC recommendations on dispersity (Pure Appl. Chem. 81 (2009) 351)", "Wyatt Technology and Agilent application notes on SEC-MALS and calibration"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# GPC/SEC molecular-weight analysis

**Goal:** Mn, Mw and dispersity (Đ = Mw/Mn) for a polymer sample with a clear statement
of *how* they were obtained — because the same sample can give numbers differing by
×2 depending on calibration.

## 1. What the column does
SEC separates by **hydrodynamic volume**, not mass: big coils elute first. Converting
elution volume to molar mass needs a calibration, and that's where most errors live.

## 2. Calibration options
- **Conventional (relative):** narrow standards (polystyrene, PMMA, PEG) → log M vs
  elution volume. Results are "PS-equivalent" molar masses. Fine for comparing samples
  of the same polymer (kinetics, batch-to-batch). Wrong in absolute terms for
  chemically different polymers — say "relative to PS standards".
- **Universal calibration:** [η]·M is the same at a given elution volume for all
  polymers (Benoit). With a viscometer detector, or known Mark–Houwink K and a for
  both polymers in that solvent at that temperature, you get absolute M. Needs
  trustworthy K/a values — literature sets vary.
- **Light scattering (SEC-MALS):** absolute M at each slice, independent of elution
  volume. Requires accurate **dn/dc** of the polymer in the eluent (measure it, or
  use a reliable value; an error in dn/dc propagates directly into M) and good
  inter-detector alignment and band-broadening corrections.

## 3. Sample and system prep
- Choose eluent that dissolves the polymer and suppresses column interactions: THF for
  many vinyl polymers; DMF or DMAc with ~0.05–0.1 M LiBr/LiCl for polar polymers (salt
  suppresses aggregation and polyelectrolyte effects); HFIP for polyesters/polyamides;
  aqueous buffers with salt for water-soluble polymers.
- Typical: 1–3 mg/mL, dissolve fully (hours to overnight for high M; gentle, no sonication
  that can degrade chains), filter 0.2–0.45 µm PTFE.
- Use a **flow marker** (e.g. toluene in THF) to correct small flow-rate drift; a 1%
  flow error is large in log M.
- Column set's exclusion limits should bracket your sample (mixed-bed columns cover a broad range).

## 4. Reading the chromatogram
- Set integration limits consistently; the low-M edge is where solvent/additive peaks
  and baseline drift live — excluding or including it shifts Mn more than Mw.
- RI peaks can be negative for polymers with dn/dc < eluent (e.g. some in THF); check sign.
- **Controlled polymerisation (RAFT, ATRP)**: expect symmetric peaks shifting to lower
  elution volume with conversion and Đ ≈ 1.1–1.3. High-M shoulders → coupling; low-M tailing
  → dead chains or slow initiation.
- Calibrated range: values outside the standards' range are extrapolation.

## Gotchas
- Interaction with the column (amines, charged polymers) delays elution → underestimated M,
  tailing peaks.
- Branched polymers are more compact than linear ones of equal mass; conventional
  calibration underestimates their M.
- Very high M (> several 10⁶) can shear-degrade in columns; lower flow rate.
- *Uncertainty note:* salt concentrations and concentration ranges are common lab
  defaults; consult your column manufacturer's limits.

## Verify
- [ ] Calibration type stated in every reported number ("PS-equivalent", "SEC-MALS, dn/dc = ...").
- [ ] Standards bracket the sample; flow marker used.
- [ ] Sample fully dissolved and filtered; no material retained on the filter (check mass recovery if MALS).
- [ ] Integration limits fixed and applied identically across samples.
- [ ] Peak shape interpreted (shoulders, tailing) before quoting Đ.
