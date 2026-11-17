---
id: natural-sciences.chemistry.structure-elucidation.proton-nmr-interpretation-workflow
name: proton-nmr-interpretation-workflow
category: natural-sciences
field: chemistry
product: structure-elucidation
tags: [structure-elucidation, nmr, 1h-nmr, proton-nmr, nmr-interpretation, chemical-shift, integration, multiplicity, j-coupling, coupling-constant, n-plus-one-rule, diastereotopic, exchangeable-protons, d2o-shake, residual-solvent-peak, cdcl3, dmso-d6, tms, degree-of-unsaturation, cosy, hsqc, hmbc, 13c-nmr, mestrenova, topspin, spectroscopy, organic-chemistry]
level: practitioner
status: draft
description: "Interpret a 1H NMR spectrum systematically: referencing, solvent and impurity peaks, integration, chemical shift regions, multiplicity and J-coupling, then assemble fragments."
sources: ["H. E. Gottlieb, V. Kotlyar, A. Nudelman, J. Org. Chem. 62 (1997) 7512 (impurity shifts); G. R. Fulmer et al., Organometallics 29 (2010) 2176", "R. M. Silverstein et al., Spectrometric Identification of Organic Compounds", "T. D. W. Claridge, High-Resolution NMR Techniques in Organic Chemistry (3rd ed.)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ¹H NMR interpretation workflow

**Goal:** go from a proton spectrum (plus formula or expected structure) to a
confident assignment — or to the specific evidence that the structure is not what
you thought — without fitting the spectrum to your hopes.

## 0. Know what you have
Molecular formula (HRMS) → **degrees of unsaturation** = C − H/2 − X/2 + N/2 + 1.
Each ring or π bond = 1; a benzene ring = 4. This bounds every later guess.

## 1. Housekeeping before chemistry
- **Phase and baseline** properly (MestReNova, TopSpin, etc.); bad phasing ruins integrals.
- **Reference** to residual solvent: CDCl₃ 7.26, DMSO-d₆ 2.50, CD₃OD 3.31, D₂O 4.79,
  acetone-d₆ 2.05, C₆D₆ 7.16 ppm (or TMS 0.00).
- **Strike out known impurities** using the Gottlieb/Fulmer tables: water (CDCl₃ ~1.56,
  DMSO ~3.33), EtOAc (2.05, 4.12, 1.26 in CDCl₃), DCM (5.30), acetone (2.17),
  hexane/grease (0.88, 1.26), plus ¹³C satellites (±~55–85 Hz around big peaks)
  and spinning sidebands.

## 2. Integrate
Set one clean, unambiguous signal (e.g. a CH₃ singlet = 3H) and normalise. Sum
should match the formula's H count (minus exchangeable protons that may be missing).
Non-integer ratios that don't fit → mixture, overlapping peaks, or slow relaxation
(quaternary-adjacent or aromatic H under-integrate if the delay d1 is short; use
d1 ≥ 5×T₁ for quantitative work).

## 3. Chemical shift map (approximate, CDCl₃)
| δ (ppm) | Typical |
|---|---|
| 0.8–1.0 | CH₃ alkyl |
| 1.2–1.7 | CH₂/CH alkyl |
| 2.0–2.7 | CH next to C=O, aryl, alkyne C≡C–H (~2–3) |
| 3.3–4.5 | CH–O, CH–N, CH–halogen; OCH₃ ~3.3–3.9 |
| 4.5–6.5 | alkene C=C–H |
| 6.5–8.5 | aromatic / heteroaromatic |
| 9.5–10.5 | aldehyde CHO |
| 10–13 | carboxylic acid OH (broad) |
| variable | OH, NH (broad; shift with concentration, temperature, solvent) |

## 4. Multiplicity and coupling
- n+1 rule for first-order spectra (Δν ≫ J): d, t, q, etc.; dd, dt for unequal neighbours.
- Measure J in Hz (not ppm). Partners share the same J — use it to link signals:
  - vicinal alkyl ~6–8 Hz; trans alkene 12–18 Hz; cis alkene 6–12 Hz; geminal sp³ 10–16 Hz;
  - aromatic ortho 7–9, meta 1–3 Hz;
  - cyclohexane axial–axial 8–13 Hz vs axial–equatorial 2–5 Hz (stereochemistry!).
- **Diastereotopic** CH₂ next to a stereocentre gives two separate signals (often an
  "ABX" pattern), not a clean doublet — common confusion.
- Roofing (leaning) multiplets point toward their coupling partner.

## 5. Assemble
Write fragments (e.g. CH₃CH₂O–, para-disubstituted ring = two 2H doublets ~8 Hz),
connect them consistently with DoU and formula, then **test** against ¹³C (+DEPT),
and 2D: COSY (H–H neighbours), HSQC (H on which C), HMBC (2–3 bond H–C, links across
heteroatoms and quaternary C), NOESY/ROESY for spatial relationships.

## Gotchas
- Exchangeable OH/NH: confirm by D₂O shake (signal disappears).
- Rotamers (amides, carbamates) double peaks at room temperature; heat the sample to coalesce.
- Second-order effects (Δν/J < ~5) distort intensities and patterns — higher field helps.
- *Uncertainty note:* shift ranges are approximate and solvent-dependent; use them to
  narrow possibilities, not to assign alone.

## Verify
- [ ] Spectrum referenced; solvent and impurity peaks identified and excluded.
- [ ] Integrals sum to the expected proton count (or the discrepancy explained).
- [ ] Every coupling constant is found in both partners.
- [ ] Proposed structure is consistent with DoU, ¹³C count and 2D correlations.
- [ ] Alternative isomers considered and ruled out with specific evidence.
