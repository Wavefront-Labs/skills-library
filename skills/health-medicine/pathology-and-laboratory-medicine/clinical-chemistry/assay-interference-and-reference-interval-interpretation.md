---
id: health-medicine.pathology-and-laboratory-medicine.clinical-chemistry.assay-interference-and-reference-interval-interpretation
name: assay-interference-and-reference-interval-interpretation
category: health-medicine
field: pathology-and-laboratory-medicine
product: clinical-chemistry
tags: [clinical-chemistry, clinical-biochemistry, pathology-and-laboratory-medicine, laboratory-medicine, assay-interference, hil-indices, haemolysis, icterus, lipaemia, pseudohyperkalaemia, edta-contamination, heterophile-antibodies, hama, biotin-interference, macroprolactin, hook-effect, reference-interval, clsi-ep28, reference-change-value, biological-variation, method-validation, clsi-ep15, verification, linearity, imprecision, bias, troponin-99th-percentile, dilution-studies]
level: practitioner
status: draft
description: "Interpret chemistry results critically: pre-analytic artefacts, HIL indices, immunoassay interference (heterophile, biotin, hook effect), reference intervals and method verification."
sources:
  - "Rifai N, Chiu RWK, Young I et al. (eds). Tietz Textbook of Laboratory Medicine, 7th ed. Elsevier 2022"
  - "CLSI EP28-A3c Defining, Establishing, and Verifying Reference Intervals in the Clinical Laboratory"
  - "CLSI EP15-A3 User Verification of Precision and Estimation of Bias; CLSI EP07 Interference Testing in Clinical Chemistry"
  - "Ismail AAA. Interference from endogenous antibodies in automated immunoassays: what laboratorians need to know. J Clin Pathol 2009"
  - "US FDA Safety Communication on biotin interference with laboratory tests (2017, updated 2019)"
  - "EFLM Biological Variation Database (biologicalvariation.eu)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Assay interference and reference-interval interpretation

*General professional reference. Analyser-specific interference limits, reference intervals and validation criteria come from your manufacturer's instructions, accreditation standard and local SOPs.*

**Goal:** know when a number is wrong before it harms someone: spot results that do not
fit the patient, identify the artefact or interference, and judge whether a value or a
change is truly abnormal.

## 1. "Does this result fit the patient?"
Triggers to investigate: physiologically implausible values, a big change from the
patient's previous result (delta check failure), discordance between related analytes
(e.g. high TSH with high free T4 without explanation), or a result discordant with the clinical picture.

## 2. Pre-analytic artefacts (the commonest cause)
| Pattern | Likely cause |
|---|---|
| High K⁺, high LDH/AST, haemolysis index raised | In-vitro haemolysis |
| High K⁺, very low Ca²⁺ and ALP | **EDTA contamination** (wrong tube order/decanting) |
| High K⁺ without haemolysis, high WCC/platelets, or sample left cold/delayed | Pseudohyperkalaemia |
| Low glucose in delayed unspun sample | Glycolysis (use fluoride tube or prompt separation) |
| Drip-arm pattern: high glucose/Na⁺ or Cl⁻, diluted everything else | IV fluid contamination |
| Low Na⁺ with severe lipaemia or paraproteinaemia (indirect ISE) | Pseudohyponatraemia — check direct ISE/blood gas |
- Use the analyser's **haemolysis, icterus, lipaemia (HIL) indices** with method-specific
  cut-offs to suppress or comment on affected results, rather than eyeballing.
- Order of draw and correct tubes matter; educate sample-takers when patterns recur.

## 3. Immunoassay interferences
- **Heterophile antibodies / human anti-animal antibodies (HAMA):** usually falsely raise
  sandwich-assay results (e.g. hCG, troponin, TSH, tumour markers). Clues: result
  discordant with clinical picture or with another platform. Investigate with **re-analysis
  on a different platform**, **heterophile blocking tubes**, **serial dilution** (non-linear
  recovery suggests interference), or polyethylene glycol precipitation.
- **Biotin** (high-dose supplements): interferes with streptavidin-biotin assays —
  falsely low in sandwich assays (e.g. troponin, TSH) and falsely high in competitive assays
  (e.g. free T4, T3), mimicking hyperthyroidism. Ask about supplements; check manufacturer data.
- **Hook (prozone) effect:** extremely high analyte concentration saturates a one-step
  sandwich assay and gives a falsely low/normal result (e.g. prolactin in macroadenoma,
  hCG in molar pregnancy). Re-test on dilution when the clinical picture suggests very high levels.
- **Macro-forms:** macroprolactin, macro-CK, macro-AST give high results with no clinical
  significance; PEG precipitation for macroprolactin.
- **Cross-reactivity:** structurally similar drugs/metabolites (e.g. digoxin-like substances, some steroid assays).

## 4. Reference intervals and decision limits
- A reference interval is usually the central 95% of a healthy reference population — so
  ~5% of healthy people fall outside it. Multiple tests mean more chance "abnormals".
- Must suit the population (age, sex, pregnancy, ethnicity where relevant) and the method.
  Establish (≥ 120 reference individuals per partition per CLSI EP28) or **verify a transferred
  interval** (commonly 20 subjects, accept if ≤ 2 fall outside).
- **Decision limits** differ from reference intervals: e.g. HbA1c diagnostic cut-off, lipid
  targets, troponin 99th percentile upper reference limit (sex-specific for high-sensitivity assays).

## 5. Is the change significant?
**Reference change value (RCV)** combines analytical imprecision (CVa) and within-subject biological variation (CVi):
RCV ≈ √2 × Z × √(CVa² + CVi²) (Z = 1.96 for 95%, two-sided). Changes smaller than RCV may be noise.
Use biological variation data from the EFLM database.

## 6. Method verification/validation (new assay)
Imprecision (repeatability and within-lab, CLSI EP15), bias/trueness (comparison with
current method or reference materials; Bland-Altman/Deming/Passing-Bablok regression),
linearity/reportable range, limits of detection/quantitation, interference, carry-over,
reference interval verification. Set acceptance criteria **before** you start (e.g. from biological variation-based specifications).

## Gotchas
- Haemolysed samples taken from a cannula are common; hyperkalaemia from them is not real — but recollect rather than ignore.
- A different platform does not always remove interference; combine methods.
- Never report a result you suspect is interfered without a comment.

## Verify
- [ ] Implausible or discordant results investigated before release.
- [ ] HIL indices applied with method-specific thresholds.
- [ ] Immunoassay interference checked by dilution, blocking agents or alternate platform.
- [ ] Reference intervals verified for population and method; decision limits labelled.
- [ ] Significant change judged against RCV.
- [ ] Verification plan with predefined acceptance criteria documented.
