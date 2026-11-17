---
id: natural-sciences.applied-industrial-rd.agrochemical-rd.formulation-type-selection-and-efficacy-trials
name: formulation-type-selection-and-efficacy-trials
category: natural-sciences
field: applied-industrial-rd
product: agrochemical-rd
tags: [agrochemical-rd, applied-industrial-rd, crop-protection, pesticide-formulation, herbicide, fungicide, insecticide, active-ingredient, formulation-types, ec, sc, wg, wp, ew, cs, od, se, croplife-codes, adjuvants, tank-mix, cipac, storage-stability, efficacy-trials, eppo, gep, randomised-complete-block, dose-response, phytotoxicity, glasshouse-screening, field-trials]
level: advanced
status: draft
description: "Pick a formulation type for a new crop-protection active (EC, SC, WG, OD, CS…), test physical stability with CIPAC methods, and run glasshouse and GEP-style field efficacy trials."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Formulation type selection and efficacy trials

**Goal:** turn a promising active ingredient (a.i.) into a formulated product that
is stable, easy for farmers to use, and proven effective and crop-safe in
statistically sound trials.

## 1. Let the active's properties choose the formulation type
Profile the a.i.: water solubility, solubility in solvents/oils, melting point,
hydrolytic and photo-stability, particle hardness, toxicity, and use rate (g a.i./ha).
Common types (CropLife International two-letter codes):
- **EC** (emulsifiable concentrate): a.i. dissolved in solvent + emulsifiers; simple,
  good biological uptake, but solvent toxicity/flammability and regulatory pressure.
- **SC** (suspension concentrate): solid a.i. milled to a few µm in water with
  dispersants and thickener; needs low water solubility and a reasonably high melting
  point (above ~60 °C is a common guide) to avoid crystal growth.
- **WG** (water-dispersible granules): dry, low-dust, good for high-melting solids.
- **EW** (oil-in-water emulsion): liquid a.i. or solution without EC's solvent load.
- **CS** (capsule suspension): microencapsulated — slow release, reduced operator
  toxicity or volatility.
- **OD** (oil dispersion): solids in oil, often with built-in adjuvancy; useful for
  water-sensitive actives.
- **SE** (suspo-emulsion): mixtures of solid and liquid actives.
Built-in vs tank-mix **adjuvants** (wetters, penetrants, oils) can change efficacy more than the a.i. load.

## 2. Physical-chemical testing
- Use **CIPAC** methods where available: suspensibility, emulsion stability,
  wet sieve, persistent foam, pourability, dispersibility, particle size.
- **Accelerated storage:** commonly 14 days at 54 °C as a predictor of 2 years at
  ambient, plus low-temperature storage (e.g. 0 °C for 7 days) for crystallisation
  and phase separation. Check a.i. content before and after.
- **Tank-mix compatibility** with common partners and water hardness levels; jar tests
  for flocculation, separation, nozzle-blocking residues.

## 3. Glasshouse screening
- Dose–response on target pests/weeds/diseases at several rates, with a
  commercial standard and an untreated control.
- Estimate ED50/ED90 from logistic dose–response fits; compare formulations at the
  same a.i. rate.
- Score **phytotoxicity** on the crop (often a 0–100% scale) at 1–2× the intended rate.
Glasshouse results overestimate field efficacy (ideal conditions, young plants).

## 4. Field efficacy trials
- Follow **EPPO** standards (or the national equivalent) and **Good
  Experimental Practice (GEP)** where trials support registration.
- **Randomised complete block design**, typically 4 replicates; plot size suited to the
  sprayer and pest distribution; untreated control and reference product in each block.
- Treatments: proposed rate, half and/or double rate (for margin and crop safety).
- Record application details: sprayer, nozzle, pressure, water volume, weather
  (temperature, humidity, wind, rain-free period), crop stage (BBCH scale), pest pressure.
- Assess at planned intervals with standard scales; record yield where relevant.
- Multiple sites and seasons are needed because pressure and weather vary.
- Analyse with ANOVA (or mixed models across sites) and mean separation; report
  efficacy relative to untreated control (e.g. Abbott's formula for insect mortality).

## 5. Toward handover
Final formulation specification, manufacturing process with critical parameters,
retained samples, analytical methods (a.i. content, impurities), and a summary of
efficacy and crop-safety data for the regulatory dossier.

## Gotchas
- Untreated controls with low pest pressure make every trial "inconclusive" — choose sites with history.
- Crystal growth in SCs appears only after months; temperature cycling reveals it sooner.
- Resistance management (mode-of-action groups: FRAC, IRAC, HRAC) shapes recommended use.

## Verify
- [ ] Formulation type justified by a.i. properties and use pattern.
- [ ] CIPAC physical tests and accelerated/low-temperature storage passed.
- [ ] Glasshouse dose–response done with commercial standard and phyto scoring.
- [ ] Field trials randomised, replicated, multi-site, with full application records.
- [ ] Efficacy reported against untreated control and reference.

*Draft note:* storage conditions and melting-point guide are common industry
heuristics; registration requirements vary by country.
