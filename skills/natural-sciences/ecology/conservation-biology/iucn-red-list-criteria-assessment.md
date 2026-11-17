---
id: natural-sciences.ecology.conservation-biology.iucn-red-list-criteria-assessment
name: iucn-red-list-criteria-assessment
category: natural-sciences
field: ecology
product: conservation-biology
tags: [conservation-biology, iucn-red-list, red-list-assessment, extinction-risk, threatened-species, critically-endangered, endangered, vulnerable, near-threatened, data-deficient, criterion-a, criterion-b, eoo, aoo, extent-of-occurrence, area-of-occupancy, generation-length, population-reduction, number-of-locations, severe-fragmentation, continuing-decline, mature-individuals, geocat, red-list-guidelines, regional-red-list, sis-connect]
level: advanced
status: draft
description: "Assess a species' extinction risk against IUCN Red List criteria A-E: generation length, EOO/AOO, locations, continuing decline, uncertainty handling and documentation."
sources: ["IUCN, Red List Categories and Criteria Version 3.1 (2nd ed., 2012)", "IUCN Standards and Petitions Committee, Guidelines for Using the IUCN Red List Categories and Criteria (current version, iucnredlist.org)", "IUCN, Guidelines for Application of IUCN Red List Criteria at Regional and National Levels v4.0 (2012)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# IUCN Red List criteria assessment

**Goal:** a defensible Red List category for a taxon (global or regional), with every
criterion evaluated, the data and reasoning documented, and uncertainty handled the
way IUCN expects.

## 1. Gather the basics
- Taxonomy (accepted name and concept), global distribution (point records, range map).
- **Generation length** — average age of parents of the current cohort. It sets the
  time windows for criteria A and C (10 years or 3 generations, whichever is longer,
  capped at 100 years for future projections).
- Population size estimates in **mature individuals** (not total counts), trends, threats.

## 2. Work through every criterion (A–E)
A taxon qualifies for the **highest category met by any criterion**.
- **A — Population reduction** over 10 years/3 generations: CR ≥ 90/80%, EN ≥ 70/50%,
  VU ≥ 50/30% (higher thresholds for A1, where causes are reversible, understood and
  ceased; lower for A2–A4). Sub-criteria specify the basis (direct observation, index,
  decline in AOO/EOO/habitat, exploitation, invasives).
- **B — Geographic range** with at least 2 of: (a) severely fragmented or few locations,
  (b) continuing decline, (c) extreme fluctuations.
  - EOO (B1) thresholds: CR < 100 km², EN < 5,000 km², VU < 20,000 km².
  - AOO (B2): CR < 10 km², EN < 500 km², VU < 2,000 km².
  - Locations: CR = 1, EN ≤ 5, VU ≤ 10.
- **C — Small, declining population:** < 250 / 2,500 / 10,000 mature individuals with
  continuing decline (and subpopulation-structure conditions).
- **D — Very small or restricted:** < 50 / 250 / 1,000 mature individuals; VU D2 for
  very restricted AOO (typically < 20 km²) or ≤ 5 locations with a plausible threat.
- **E — Quantitative analysis** (PVA): probability of extinction ≥ 50% in 10 yrs/3 gen
  (CR), ≥ 20% in 20 yrs/5 gen (EN), ≥ 10% in 100 yrs (VU).

## 3. Measure EOO and AOO correctly
- **EOO:** minimum convex polygon around all known/inferred/projected sites of present
  occurrence (excluding vagrants), not clipped to habitat for Red List purposes.
- **AOO:** count of occupied cells on a **2 × 2 km grid** (4 km² cells) — the standard
  scale. AOO from finer or coarser grids is not comparable to thresholds.
- Tools: GeoCAT (web), `red` or `ConR` R packages. Check grid placement sensitivity.
- **Location** = a geographically/ecologically distinct area in which a *single threatening
  event* can rapidly affect all individuals — defined by the threat, not by sites.

## 4. Uncertainty and documentation
- Use best estimates with plausible ranges; IUCN guidance asks assessors to adopt a
  **precautionary but realistic** attitude to uncertainty, and the category can be stated
  with a plausible range.
- **Data Deficient** is for when the range of plausible categories spans LC to CR — not a
  default for "few data". **Near Threatened** when close to VU thresholds.
- Regional assessments: apply the regional guidelines (adjust for immigration from outside).
- Document every criterion's data, inferences, and the justification text in the IUCN
  Species Information Service (SIS) format; assessments are reviewed.

## Gotchas
- Counting total individuals instead of mature individuals overstates population size.
- "Severely fragmented" means most of the population is in small, isolated subpopulations
  — not simply a patchy range.
- Mixing generation-length windows across criteria, or using AOO at 1 km cells.
- *Uncertainty note:* thresholds are from Categories & Criteria v3.1; the Guidelines
  document is updated periodically — use the current version for definitions.

## Verify
- [ ] Generation length estimated and used for A/C time windows.
- [ ] All five criteria evaluated, with "not met" explained.
- [ ] AOO on a 2 × 2 km grid; EOO by minimum convex polygon.
- [ ] Locations defined by the most serious plausible threat.
- [ ] Category, criteria string (e.g. EN B1ab(iii)+2ab(iii)) and rationale documented.
