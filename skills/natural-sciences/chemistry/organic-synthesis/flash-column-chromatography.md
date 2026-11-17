---
id: natural-sciences.chemistry.organic-synthesis.flash-column-chromatography
name: flash-column-chromatography
category: natural-sciences
field: chemistry
product: organic-synthesis
tags: [organic-synthesis, flash-chromatography, column-chromatography, purification, silica-gel, tlc, thin-layer-chromatography, rf-value, eluent, mobile-phase, hexane-ethyl-acetate, dcm-methanol, gradient-elution, dry-loading, wet-loading, celite, triethylamine, streaking, co-elution, automated-flash, biotage, combiflash, still-1978, fraction-collection, work-up, organic-chemistry-lab]
level: practitioner
status: draft
description: "Run a flash column that separates: TLC solvent choice (Rf 0.2-0.35), silica loading ratio, dry vs wet loading, column packing, fraction collection and common failures."
sources: ["W. C. Still, M. Kahn, A. Mitra, J. Org. Chem. 43 (1978) 2923", "Not Voodoo X (University of Rochester), chromatography pages", "Biotage application notes on flash method development"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Flash column chromatography

**Goal:** isolate your product pure from a crude mixture in one column, using TLC
to predict the outcome rather than discovering it in 60 test tubes.

## 1. Develop on TLC first
- Find an eluent where the **product Rf ≈ 0.2–0.35** and the nearest impurity is at
  least ΔRf ≈ 0.1 away (closer → bigger column, shallower gradient).
- Start with hexane/EtOAc (or heptane/EtOAc). Polar compounds: DCM/MeOH (keep MeOH
  ≤ ~10%: silica dissolves somewhat above that). Try a different selectivity
  (toluene, ether, acetone, DCM blends) if spots overlap at every polarity.
- **Amines/basic N** streak: add ~1% Et₃N (or NH₃/MeOH) to the eluent and pre-treat
  the silica. **Acids** streak: add ~0.5–1% AcOH.
- Co-spot crude with starting material to know which spot is which; check UV
  (254 nm) *and* a stain (KMnO₄, anisaldehyde, CAM, ninhydrin) — many impurities are UV-silent.
- 2D TLC (run, rotate 90°, rerun) tells you if the compound decomposes on silica.

## 2. Size the column
- Silica mass ≈ **30–50× the crude mass** for an easy separation (ΔRf > 0.2),
  ~100× or more for a hard one.
- Column diameter from the sample size (Still's table): roughly 2 cm for ~100 mg,
  3–4 cm for ~0.5–1 g, 5 cm for ~2–3 g. Silica bed ~15 cm tall.
- Silica: 40–63 µm (230–400 mesh).

## 3. Pack and load
- **Slurry pack** in the starting eluent, tap/pressurise to settle, never let the top
  run dry; add a thin layer of sand on top.
- **Wet loading:** dissolve in the *minimum* volume of eluent (or a little DCM) and
  apply as a thin band. Dissolving in a strong solvent (DCM, MeOH, EtOAc) ruins
  resolution — the compound runs with it.
- **Dry loading** (preferred when solubility is poor or the solvent is strong):
  dissolve crude, add 2–3× its mass of silica or Celite, rotovap to a free-flowing
  powder, pour on top.

## 4. Run it
- Push with air/N₂ at a flow giving ~5 cm/min descent of the solvent front (the "flash").
- Use a **step or gradient**: start ~half the polarity that gave Rf 0.3, increase
  stepwise. Roughly, elution volume ≈ CV/Rf, where CV = column volume.
- Fraction size ≈ 1/4 to 1/2 of a column volume near the product; TLC every few
  fractions (several per plate).
- Automated systems (Biotage, CombiFlash) do the same with pre-packed cartridges and
  UV detection; method development on TLC transfers via the 1/Rf ≈ CV relationship.

## 5. Combine and finish
Combine only fractions that are single-spot by TLC in two different stains/eluents.
Mixed fractions: recolumn or recrystallise. Rotovap, then high vacuum to remove
residual solvent; check by ¹H NMR (residual EtOAc/hexane peaks).

## Gotchas
- Cracks or channels in the bed (from heat of wetting or running dry) smear bands.
- Overloading looks like tailing and co-elution even with a good Rf difference.
- Acid-sensitive compounds (acetals, silyl ethers, some epoxides) can decompose on
  silica; use Et₃N-deactivated silica or neutral alumina.
- *Uncertainty note:* the column-size figures are approximate, adapted from Still's
  original guidance; scale with your separation difficulty.

## Verify
- [ ] TLC showed product Rf 0.2–0.35 with clear separation before packing.
- [ ] Silica:crude ratio and column diameter chosen for the ΔRf.
- [ ] Sample loaded as a narrow band (dry-loaded if solubility was poor).
- [ ] Combined fractions are single-spot in two visualisation methods.
- [ ] Product mass and ¹H NMR confirm purity and recovery.
