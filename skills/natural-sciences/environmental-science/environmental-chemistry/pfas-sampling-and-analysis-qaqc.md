---
id: natural-sciences.environmental-science.environmental-chemistry.pfas-sampling-and-analysis-qaqc
name: pfas-sampling-and-analysis-qaqc
category: natural-sciences
field: environmental-science
product: environmental-chemistry
tags: [environmental-chemistry, pfas, pfoa, pfos, forever-chemicals, epa-1633, epa-537.1, epa-533, lc-ms-ms, isotope-dilution, field-blank, equipment-blank, cross-contamination, groundwater-sampling, surface-water, qa-qc, chain-of-custody, method-detection-limit, contaminant-analysis, trace-analysis]
level: practitioner
status: docs-checked
description: "Sample and report PFAS without contaminating it: choose EPA 1633 vs 537.1/533 by matrix, agree kit, blanks and reporting limits with the lab, and read the QC in the report."
sources: [https://www.epa.gov/water-research/epa-drinking-water-research-methods, https://www.epa.gov/cwa-methods/cwa-analytical-methods-and-polyfluorinated-alkyl-substances-pfas]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# PFAS sampling and analysis QA/QC — trace data you can defend

**Goal:** collect environmental samples for per- and polyfluoroalkyl substances (PFAS)
and get results at very low concentrations where a detection reflects the site,
not your gloves, tubing or bottle.

## 1. Pick the method before you pick the bottles
- **Drinking water:** EPA **537.1** (18 PFAS; solid-phase extraction + LC-MS/MS) or
  **533** (select PFAS; isotope-dilution anion-exchange SPE + LC-MS/MS). Labs certify per method.
- **Other matrices** (surface water, groundwater, wastewater, soil, biosolids, sediment,
  landfill leachate, fish tissue): EPA **1633**, a 40-compound LC-MS/MS method (EPA's current
  version is 1633A, December 2024, proposed for 40 CFR 136.3 and not yet required for CWA
  compliance monitoring until promulgated; check the CWA methods page for status).
- Ask the lab *before mobilising* for its bottle type, volume, preservative, hold time,
  temperature requirement and reporting limits relative to your screening values. A
  reporting limit above the action level makes the whole campaign useless.

## 2. Keep PFAS sources away from the sample
PFAS are in many field materials (fluoropolymer tubing and tape, treated clothing, some
packaging and personal-care products). Take the exact do/don't list for bottles, tubing,
clothing and decon from the lab and the site QAPP rather than from a generic list, and
ask for certified PFAS-free water for rinsing.

## 3. Build the blanks that let you defend a detection
Plan field reagent blanks, equipment rinsate blanks, field duplicates and matrix
spikes at the frequencies the method and your QAPP require. Sample least-contaminated
locations first, highest last, to limit carry-over.

## 4. Read the lab report like a reviewer
- **Isotope-dilution recoveries:** each analyte is corrected by its labelled analogue;
  recoveries outside the method's limits mean the result is estimated or unusable.
- **Blank contamination:** if a blank shows an analyte, qualify sample results near it
  according to your program's data-validation rule.
- **Linear vs branched isomers:** confirm the lab integrated both for PFOS and PFOA.
- **Units and sums:** regulatory sums must use the analyte list the rule specifies.
- **Detection vs reporting limit:** results between MDL and LOQ are estimates;
  don't drop them silently, and don't treat them as precise.

## Gotchas
- New waders and rain gear are a classic source; ask the lab how to screen them.
- Foam and surface microlayers concentrate PFAS — note foam at surface-water sites.
- Precursors aren't captured by target lists; a total oxidisable precursor (TOP) assay
  is a separate request.

## Verify
- [ ] Method matches matrix (537.1/533 drinking water, 1633 others) and reporting limit is below the screening level.
- [ ] Field kit checklist agreed with the lab and QAPP.
- [ ] Blanks and duplicates collected as planned.
- [ ] Recoveries within method limits; blank-associated detections qualified.
- [ ] Chain-of-custody, temperature at receipt and hold times documented.

## Checked
2026-11-01. Confirmed from EPA's drinking water research methods page: 537.1 covers 18 PFAS by SPE and LC-MS/MS; 533 is isotope-dilution anion-exchange SPE and LC-MS/MS; 1633 is a 40-compound method for surface water, groundwater, wastewater, soil, biosolids, sediment, landfill leachate and fish tissue. From EPA's CWA PFAS methods page: 1633A dated December 2024, proposed for 40 CFR 136.3, not yet required for CWA compliance monitoring. Removed (not stated on pages read): 533 analyte count, bottle volumes, hold times, temperatures, material do/don't lists (ITRC), blank frequencies, recovery windows, blank-multiple rule.
Method: documentation only; no commands were run.
