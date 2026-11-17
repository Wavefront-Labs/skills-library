---
id: natural-sciences.chemistry.computational-chemistry.dft-functional-and-basis-set-selection
name: dft-functional-and-basis-set-selection
category: natural-sciences
field: chemistry
product: computational-chemistry
tags: [computational-chemistry, dft, density-functional-theory, functional-choice, basis-set, b3lyp, pbe0, wb97x-d, wb97m-v, m06-2x, r2scan-3c, dispersion-correction, d3bj, d4, def2-svp, def2-tzvp, pople-basis, 6-31g-star, diffuse-functions, effective-core-potential, ecp, solvation-model, smd, cpcm, gmtkn55, benchmark, orca, gaussian, q-chem, thermochemistry, barrier-heights]
level: advanced
status: draft
description: "Choose a DFT functional, dispersion correction, basis set and solvent model for organic and organometallic problems, and check the choice against benchmarks."
sources: ["L. Goerigk et al., GMTKN55 benchmark, Phys. Chem. Chem. Phys. 19 (2017) 32184", "M. Bursch, J.-M. Mewes, A. Hansen, S. Grimme, Best-practice DFT protocols, Angew. Chem. Int. Ed. 61 (2022) e202205735", "F. Weigend & R. Ahlrichs, def2 basis sets, Phys. Chem. Chem. Phys. 7 (2005) 3297"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing a DFT functional and basis set

**Goal:** a level of theory that gets relative energies (reaction energies,
barriers, conformer ordering) right to ~1–3 kcal/mol for your system, chosen
for reasons you can defend in a methods section — not "B3LYP/6-31G* because
everyone does".

## 1. Default protocol (molecular, closed-shell, main-group / light organometallic)
A widely used composite approach (see Bursch et al. 2022):
1. **Conformer search** cheaply (CREST/GFN2-xTB, or force field), keep low-energy
   conformers within a few kcal/mol.
2. **Geometry + frequencies:** a robust hybrid or composite method with
   dispersion and a double/triple-ζ basis, e.g. r²SCAN-3c, PBE0-D3(BJ)/def2-SVP, or
   B3LYP-D3(BJ)/def2-SVP. Frequencies give ZPE and thermal corrections and confirm
   minima (0 imaginary) or TSs (exactly 1).
3. **Single-point energies** at a higher level on those geometries: a modern
   hybrid/range-separated or double-hybrid functional with dispersion
   (ωB97X-D/V, ωB97M-V, PW6B95-D3, DSD-type double hybrids) and def2-TZVP or larger.
4. **Solvation** with an implicit model (SMD or CPCM) for the solvent used; include it at least in the single points.

## 2. Rules behind the choices
- **Always add dispersion** (D3(BJ) or D4, or a functional with built-in VV10).
  Uncorrected B3LYP gets non-covalent interactions and many conformer and
  barrier energies badly wrong.
- **Hybrid vs GGA:** hybrids (20–25% HF exchange) are usually better for barriers and
  thermochemistry; range-separated hybrids help charge-transfer and anions. GGAs (PBE,
  BP86) are cheaper and often fine for transition-metal geometries.
- **Basis set:** double-ζ (def2-SVP, 6-31G*) is acceptable for geometries; energies
  need triple-ζ (def2-TZVP(P)). **Diffuse functions** (def2-SVPD, 6-31+G*) for anions,
  weak interactions, excited states. Prefer the def2 family across the periodic table.
- **Heavy elements:** def2 basis sets include ECPs beyond Kr automatically; Pople
  sets don't cover them — mixing basis families by hand is error-prone.
- **Spin states / transition metals:** relative spin-state energies depend strongly
  on % HF exchange. Compare several functionals and, if it matters, benchmark against
  higher-level (DLPNO-CCSD(T)) or experiment.

## 3. Benchmark your own system when it matters
- Check how your functional performs on GMTKN55 subsets relevant to you (barriers,
  isomerisations, non-covalent).
- For a key reaction, compute a few points with DLPNO-CCSD(T)/def2-TZVP (or CBS
  extrapolation) and compare.
- Report the spread across 2–3 reasonable functionals; if conclusions flip, they
  aren't robust.

## Gotchas
- Mixing levels: free energies must use frequencies computed at the geometry's level.
- Low-frequency modes (< ~100 cm⁻¹) inflate entropy in the harmonic approximation;
  use quasi-harmonic corrections (Grimme/Truhlar; e.g. GoodVibes) for flexible molecules.
- Standard-state correction (1 atm → 1 M, +1.89 kcal/mol at 298 K per species) for
  solution free energies of associative/dissociative steps.
- Integration grids: Minnesota functionals (M06-2X) need fine grids or give noisy
  energies and spurious imaginary frequencies.
- *Uncertainty note:* functional rankings evolve with new benchmarks; the named
  functionals reflect consensus as of the cited reviews, not a final word.

## Verify
- [ ] Dispersion correction included; basis set at least triple-ζ for final energies.
- [ ] Every stationary point checked by frequencies (0 or 1 imaginary).
- [ ] Solvent model matches the experiment; standard-state correction applied.
- [ ] Key conclusions hold across ≥ 2 functionals or are benchmarked.
- [ ] Methods section states functional, dispersion, basis, solvent model, grid and software version.
