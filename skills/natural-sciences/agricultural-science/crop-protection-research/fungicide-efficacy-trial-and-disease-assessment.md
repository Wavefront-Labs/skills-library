---
id: natural-sciences.agricultural-science.crop-protection-research.fungicide-efficacy-trial-and-disease-assessment
name: fungicide-efficacy-trial-and-disease-assessment
category: natural-sciences
field: agricultural-science
product: crop-protection-research
tags: [agricultural-science, crop-protection-research, plant-pathology, efficacy-trial, fungicide-trial, pesticide-efficacy, eppo-standards, gep, good-experimental-practice, disease-severity, disease-incidence, standard-area-diagrams, sad, visual-assessment, rater-calibration, audpc, abbott-formula, percent-control, untreated-control, reference-product, inoculation, disease-pressure, crop-safety, phytotoxicity, yield-response, ipm-research, resistance-screening]
level: practitioner
status: draft
description: "Run a fungicide (or other crop-protection) efficacy trial: EPPO-style design with untreated and reference controls, calibrated severity scoring, AUDPC, percent control, and phytotoxicity."
sources: [EPPO Standards PP 1/152 (design and analysis of efficacy trials), PP 1/181 (conduct and reporting), and crop-specific PP 1 standards; Madden, Hughes & van den Bosch 2007 The Study of Plant Disease Epidemics; Bock et al. 2010/2020 reviews on visual disease assessment]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Fungicide efficacy trial and disease assessment

**Goal:** measure how well a crop-protection product or programme controls a disease
(the same structure applies to insecticide and herbicide trials) with data that are
comparable across sites and acceptable for publication or registration dossiers.

## 1. Design
- Follow the **EPPO PP 1 standards** (general PP 1/152, PP 1/181, plus the crop-disease
  specific standard) or national equivalents; registration trials usually need
  certified **GEP** (Good Experimental Practice) facilities.
- Treatments: **untreated control** (essential — efficacy is relative to it), a
  **reference product** (current standard), test product at proposed rate, and often
  half and double rate (double rate for crop-safety/phytotoxicity).
- RCBD with ≥4 replicates; plot size large enough to harvest yield (e.g. ≥10–20 m²
  for cereals). Guard plots or spreader rows (susceptible variety) promote even
  disease pressure.
- **Disease pressure** is the point: choose a susceptible variety and a site/season
  with history. Artificial inoculation (spore suspension, infected debris) when natural
  pressure is unreliable. A trial with <~5–10% severity in the control usually can't
  discriminate products — report it as low pressure, don't claim equivalence.

## 2. Application
Calibrated plot sprayer (e.g. CO2 backpack with boom), stated water volume, nozzle and
pressure; record crop growth stage (BBCH), weather, and time to rain. Timing relative to
infection (protectant vs curative) is often the main finding.

## 3. Assessing disease
- **Incidence** = % plants or leaves with any symptom; **severity** = % area diseased.
  Severity on specified leaves (e.g. flag leaf, F-1, F-2 in cereals) is standard.
- Use **standard area diagrams (SADs)** and calibrate raters before each assessment
  session (e.g. software training sets); raters overestimate low severities strongly.
  Same rater per trial where possible, or include rater as a factor.
- Assess at several dates from onset to late epidemic, plus **before the first
  application** (baseline) for curative claims.
- Image-based or sensor scoring is increasingly used; validate against visual scores.

## 4. Analysis
- **AUDPC** (area under disease progress curve) integrates severity over time:
  `AUDPC = Σ ((y_i + y_{i+1})/2 × (t_{i+1} − t_i))`. Standardise by duration (sAUDPC) if
  intervals differ across trials. R: `agricolae::audpc()`.
- **Percent control (Abbott's formula):** `efficacy % = (C − T)/C × 100`, with C and T
  the untreated and treated severity. Analyse severity (transformed if needed, or with a
  beta/binomial GLMM), then compute efficacy from model means; don't run ANOVA on
  efficacy percentages directly.
- Yield and quality (thousand-grain weight, specific weight) responses, and
  economic return per application.
- Multi-site analysis with site × treatment interaction; regional efficacy claims need
  several sites and seasons.

## 5. Phytotoxicity and resistance
- Score phytotoxicity (chlorosis, necrosis, stunting, % scale) at each assessment,
  especially at double rate.
- Collect samples for **fungicide sensitivity monitoring** (EC50 shifts, target-site
  mutations, e.g. SDHI or QoI resistance) when control is unexpectedly poor; follow
  FRAC guidance on mode-of-action rotation in recommendations.

## Gotchas
- Disease misidentified at scoring (similar leaf spots) ruins a dataset — confirm the
  pathogen by microscopy, culture or qPCR at least once per trial.
- Spray drift into untreated plots shrinks apparent efficacy; keep buffers.
- Assessing too early (low disease) or too late (senescence) compresses differences.

## Verify
- [ ] Untreated control, reference product and adequate replication present.
- [ ] Control-plot severity high enough to discriminate; pathogen confirmed.
- [ ] Raters calibrated with SADs; leaf layers and dates specified.
- [ ] AUDPC and efficacy derived from modelled severity; phytotoxicity and yield reported.
