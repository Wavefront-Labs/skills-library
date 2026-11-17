---
id: natural-sciences.chemistry.electrochemistry.cyclic-voltammetry-setup-and-interpretation
name: cyclic-voltammetry-setup-and-interpretation
category: natural-sciences
field: chemistry
product: electrochemistry
tags: [electrochemistry, cyclic-voltammetry, cv, voltammetry, potentiostat, three-electrode-cell, working-electrode, glassy-carbon, platinum-electrode, counter-electrode, reference-electrode, ag-agcl, sce, pseudo-reference, ferrocene, fc-fc-plus, supporting-electrolyte, tbapf6, ir-drop, ir-compensation, randles-sevcik, peak-separation, reversibility, scan-rate, diffusion-coefficient, electrode-polishing, alumina, degassing, gamry, biologic]
level: practitioner
status: gated
description: "Run and read a cyclic voltammogram: three-electrode cell, electrode polishing, supporting electrolyte, iR compensation, ferrocene referencing, reversibility and scan-rate tests."
sources: ["N. Elgrishi et al., A Practical Beginner's Guide to Cyclic Voltammetry, J. Chem. Educ. 95 (2018) 197", "A. J. Bard & L. R. Faulkner, Electrochemical Methods (2nd ed.)", "G. Gritzner & J. Kůta, IUPAC recommendation on ferrocene reference, Pure Appl. Chem. 56 (1984) 461"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cyclic voltammetry: setup and interpretation

**Goal:** a clean CV of your compound from which you can quote formal potentials
(E½ vs Fc⁺/Fc), judge reversibility, and say whether the process is diffusion-
controlled — and recognise artefacts before you publish them.

## 1. The cell
- **Working electrode (WE):** glassy carbon (3 mm) is the general default; Pt or Au
  for some potentials/chemistries. **Polish before every experiment**: alumina slurry
  (e.g. 0.05 µm (gated: unconfirmed, source is paywalled or blocked)) on a pad in figure-8s, rinse, sonicate briefly, rinse, dry.
- **Counter electrode (CE):** Pt wire/mesh, larger area than the WE.
- **Reference electrode (RE):** aqueous Ag/AgCl or SCE in water; in organic solvents a
  non-aqueous Ag/Ag⁺ or a Ag-wire pseudo-reference, **always calibrated with an
  internal standard** (ferrocene) at the end of the experiment.
- Electrolyte: 0.1 M supporting electrolyte (e.g. [nBu₄N][PF₆] in MeCN or DCM; KCl
  or buffer in water); analyte ~1 mM.
- **Degas** with N₂/Ar for ~10 min (O₂ reduces near −0.8 to −1.2 V vs Fc in organic
  solvents and around −0.3 V and below vs Ag/AgCl in water (gated: unconfirmed, source is paywalled or blocked)), and keep a gas blanket over the solution while measuring.

## 2. Running
1. Record a **blank CV** (electrolyte only) over your window; this is your background
   and solvent window.
2. Add analyte; start at the open-circuit potential, scan toward the first process.
   Typical first scan rate 100 mV/s (gated: unconfirmed, source is paywalled or blocked).
3. Repeat at several scan rates (e.g. 25, 50, 100, 200, 500, 1000 mV/s).
4. At the end, add ferrocene (or decamethylferrocene if Fc overlaps your peaks) and
   record; quote potentials vs Fc⁺/Fc.

## 3. Reading a reversible couple
- E½ ≈ (E_pa + E_pc)/2.
- **ΔE_p = E_pa − E_pc ≈ 59/n mV** at 25 °C (RT ln10/F = 59.16 mV from CODATA R and F via scipy.constants) for an ideal reversible one-electron
  process; ~60–90 mV is common in practice due to uncompensated resistance (gated: unconfirmed, source is paywalled or blocked).
  Compare with ferrocene measured in the *same* cell: if Fc also shows 90 mV, your
  compound's 90 mV is iR, not slow kinetics.
- i_pa/i_pc ≈ 1 (measure each peak from its proper extrapolated baseline, not zero current).
- **Randles–Ševčík:** i_p ∝ √v for a freely diffusing species. Plot i_p vs √v: linear
  through the origin = diffusion control; i_p ∝ v = surface-adsorbed species.
  Gives the diffusion coefficient if area and concentration are known.

## 4. When it isn't reversible
- ΔE_p grows with scan rate → slow electron transfer (quasi-reversible).
- Return peak missing or smaller, recovering at fast scan rates → a chemical step
  follows electron transfer (EC mechanism). Its rate can be estimated from the scan rate
  where reversibility returns.
- New peaks on the second cycle → products formed at the electrode.

## Gotchas
- **iR drop** in low-conductivity organic solutions: keep the RE tip close to the WE
  (Luggin capillary), use positive-feedback iR compensation (~80–90% of measured R_u;
  100% causes oscillation (gated: unconfirmed, source is paywalled or blocked)).
- Pseudo-reference drift: never report potentials vs a bare Ag wire.
- Current sign conventions differ (IUPAC vs US, anodic positive or negative) — state which.
- Electrode fouling: peaks shrink scan to scan; repolish.
- *Uncertainty note:* the O₂ reduction potentials quoted are approximate and solvent-
  and reference-dependent.

## Verify
- [ ] Blank CV recorded; analyte peaks absent from the blank.
- [ ] Ferrocene added and potentials referenced to Fc⁺/Fc.
- [ ] ΔE_p of analyte compared with ΔE_p of ferrocene in the same cell.
- [ ] i_p vs √v plotted; diffusion vs adsorption decided.
- [ ] Scan direction, scan rate, electrolyte, concentration and current convention reported.
