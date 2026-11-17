---
id: natural-sciences.applied-industrial-rd.drug-discovery.hit-to-lead-screening-cascade
name: hit-to-lead-screening-cascade
category: natural-sciences
field: applied-industrial-rd
product: drug-discovery
tags: [drug-discovery, applied-industrial-rd, medicinal-chemistry, hit-to-lead, lead-optimisation, screening-cascade, hts, high-throughput-screening, z-prime, assay-development, ic50, dose-response, orthogonal-assay, pains, aggregators, counter-screen, sar, ligand-efficiency, lipophilic-efficiency, adme, dmpk, microsomal-stability, permeability, herg, selectivity, candidate-profile, tpp]
level: advanced
status: draft
description: "Design and run a drug-discovery screening cascade: assay quality (Z′), hit confirmation, triaging artefacts, SAR with efficiency metrics, early ADME/safety and a candidate profile."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Hit-to-lead screening cascade

**Goal:** turn primary screening hits against a validated target into a lead
series with credible potency, selectivity and drug-like properties — and kill false
positives early and cheaply.

## 1. Begin with the target product profile (TPP)
Define the end-point: route (oral, injectable), dosing frequency, indication,
required potency (e.g. cellular IC50 < 100 nM), selectivity over named off-targets,
safety margins, and desired PK. Every assay in the cascade should exist to answer a
TPP question. Without it, teams optimise potency forever.

## 2. Assay development and quality
- Primary assay (biochemical or cell-based) miniaturised for the screening format.
- Quality metric: **Z′-factor** = 1 − 3(σpos + σneg)/|μpos − μneg|. Z′ ≥ 0.5 is the
  common bar for HTS; check across plates and days, not one plate.
- Include reference inhibitor (pharmacological control) dose–response on every run;
  track its IC50 over time on a control chart.
- Watch DMSO tolerance, edge effects (evaporation in outer wells), and reagent stability.

## 3. The cascade (typical order)
1. **Primary screen** at a single concentration (often ~10 µM).
2. **Hit confirmation:** re-test from fresh solid or re-supplied stock, in replicate.
3. **Dose–response** (10-point, half-log dilutions) for IC50/EC50 and Hill slope.
4. **Artefact triage:**
   - **Orthogonal assay** with a different readout (e.g. biophysical: SPR, thermal
     shift, NMR) to show direct binding.
   - **Counter-screens** for the detection technology (luciferase inhibitors,
     fluorescent compounds, quenchers).
   - **Aggregation:** re-test with 0.01% non-ionic detergent; potency loss suggests
     a colloidal aggregator. Steep Hill slopes (>2) are a warning sign.
   - **PAINS** and reactive substructure filters; redox cyclers; metal contamination.
   - Confirm identity and purity (LC-MS) of the tested sample.
5. **Cellular activity** and target engagement in cells.
6. **Selectivity** against related targets and a broad panel for key liabilities.
7. **Early ADME:** solubility, microsomal/hepatocyte stability, permeability
   (PAMPA/Caco-2), plasma protein binding, CYP inhibition.
8. **Early safety:** hERG, cytotoxicity, Ames-type flags where relevant.
9. **In vivo PK** for the best compounds, then efficacy models.

## 4. SAR and efficiency metrics
- Make **analogue series** to show that activity tracks structure (a flat or noisy SAR
  often means an artefact).
- **Ligand efficiency (LE)** ≈ 1.37 × pIC50 / heavy-atom count (kcal/mol per heavy
  atom); ~0.3 or more is a common guide.
- **Lipophilic ligand efficiency (LLE/LipE)** = pIC50 − cLogP (or logD); higher is
  better, values ≥ 5 are often targeted for leads.
- Track molecular weight and lipophilicity creep; potency gains bought with
  lipophilicity usually cost solubility, metabolism and safety.
- Use matched molecular pairs and structure-based design where structures exist.

## 5. Decision-making
- Pre-agree **progression criteria** for each stage (e.g. "IC50 < 1 µM, LLE > 4,
  microsomal clearance below X, >30× selectivity over Y").
- Compare series, not single compounds; a series with a clear SAR and fewer
  liabilities beats one potent outlier.
- Write a **candidate profile** at each milestone against the TPP, noting gaps.

## Gotchas
- Compound degradation in DMSO stocks (water uptake, freeze–thaw) produces false SAR.
- Biochemical potency rarely translates 1:1 into cells (permeability, protein binding, ATP competition for kinases).
- Species differences in metabolism mislead PK-based progression.

## Verify
- [ ] TPP written and each assay mapped to a TPP question.
- [ ] Z′ and reference IC50 tracked across runs.
- [ ] Hits confirmed from fresh material, by an orthogonal assay, and cleared of aggregation/interference.
- [ ] SAR shows coherent trends; LE/LLE tracked.
- [ ] Progression criteria set in advance and applied consistently.

*Draft note:* thresholds (Z′ ≥ 0.5, LE ~0.3, LLE ≥ 5) are widely cited heuristics,
not rules; targets vary by target class and modality.
