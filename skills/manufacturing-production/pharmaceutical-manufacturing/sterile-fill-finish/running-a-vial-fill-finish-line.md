---
id: manufacturing-production.pharmaceutical-manufacturing.sterile-fill-finish.running-a-vial-fill-finish-line
name: running-a-vial-fill-finish-line
category: manufacturing-production
field: pharmaceutical-manufacturing
product: sterile-fill-finish
tags: [sterile-fill-finish, fill-finish, vial-filling, syringe-filling, prefilled-syringes, depyrogenation-tunnel, filling-needles, fill-weight, in-process-weight-check, stoppering, capping, crimping, seal-integrity, ccit, container-closure-integrity, lyophilisation, lyophilization, freeze-drying, lyophiliser-loading, partial-stoppering, visual-inspection, 100-percent-inspection, aql, particulates, bausch-strobel, groninger, optima, syntegon, pharmaceutical-manufacturing]
level: practitioner
status: draft
description: "Run a sterile vial line: depyrogenation, filling with fill-weight checks, stoppering, lyophiliser loading, capping/crimping, and 100% visual inspection with AQL follow-up — and what goes wrong."
sources:
  - "https://health.ec.europa.eu/medicinal-products/eudralex/eudralex-volume-4_en"
  - "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/sterile-drug-products-produced-aseptic-processing-current-good-manufacturing-practice"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running a vial fill-finish line

**Goal:** fill the right dose into every vial, close it so it stays sterile, and
remove defective units — without breaking the aseptic conditions the line was qualified
under. Aseptic behaviour itself is in
manufacturing-production.pharmaceutical-manufacturing.sterile-aseptic-processing.aseptic-technique-and-cleanroom-behaviour.

## 1. Line flow (typical liquid vial line)
Washer → **depyrogenation tunnel** (dry heat; validated for endotoxin reduction) → Grade A filling (isolator or RABS) → **stoppering** → (lyo: partial stoppering
and loading) → **capping/crimping** (often outside Grade A; confirm the air-supply requirement in Annex 1) → **100% visual inspection** → labelling/packaging.

## 2. Setup checks
- Sterilised product path (filter, tubing, needles, pumps) installed per the aseptic
  assembly procedure; **filter integrity test** results acceptable (pre-use post-sterilisation
  testing where required, post-use always — confirm site requirement).
- Stopper bowl and track loaded with sterile stoppers from the correct lot.
- Tunnel at temperature and belt speed with charts running before the first vial enters.
- Fill-weight target, limits and check frequency from the batch record entered on the HMI.

## 3. Filling and fill weight
- Pump types: peristaltic, rotary piston (ceramic), time-pressure. Each drifts differently:
  peristaltic tubing wears and softens; pistons are sensitive to viscosity and temperature.
- **Fill weight checks** — gross minus tare, at the batch record frequency, often across
  all needles. Many lines have in-line check-weighing (100% or statistical).
- Adjust within the allowed step size, re-check, and document the adjustment.
- Watch for **dripping or foaming** at the needle (wrong suck-back setting, needle height,
  speed) — product on the vial neck can stop stoppers seating and compromise crimp seal.

## 4. Stoppering and capping
- Missing or high stoppers must be rejected automatically before capping; verify the
  sensor reject works at startup with challenge vials (site practice).
- **Crimping:** residual seal force and visual crimp quality (no wrinkling, cap not
  loose or spinning). Over-crimping cracks vial necks; under-crimping fails CCI.
- **CCI (container closure integrity):** deterministic methods (vacuum decay, headspace
  gas analysis, high-voltage leak detection) are generally preferred over dye ingress; see the pharmacopoeial chapters for method details.

## 5. Lyophilised products
- Vials leave the filler **partially stoppered** (vent slots open) and must reach the
  lyophiliser shelves without being knocked closed or exposed — loading is an aseptic
  operation (automatic loading systems or trays, per site).
- Shelf temperature at loading, loading time and order are recorded.
- At cycle end, shelves press stoppers home under vacuum or nitrogen backfill, then vials
  go to capping. A lyo cycle alarm (vacuum, shelf temperature excursion) is a deviation;
  don't restart a cycle without QA.
- Cake appearance (collapse, meltback, shrinkage) is checked at inspection.

## 6. Visual inspection
- **100% inspection** (manual booths, semi-automatic or automated) against a defect
  library: particles (visible), cracks, fill level, cake defects, stopper/crimp faults.
- Manual inspectors are qualified with seeded defect kits and follow defined timing
  (follow your qualified inspection method and the pharmacopoeial chapters).
- After 100% inspection an **AQL** sample re-inspection confirms performance; failure
  generally means re-inspection of the lot and an investigation.

## Gotchas
- Fill weight drifting with product temperature over a long run.
- Stopper jams leading to repeated interventions — fix root cause, don't keep reaching in.
- Glass breakage in the line: stop and follow the glass-breakage clearance SOP; nearby vials are rejected.
- Line speed pushed above validated maximum to recover time.
- Forgetting reconciliation: vials filled vs inspected vs rejected vs samples must add up.

## Verify
- [ ] Filter integrity, tunnel charts and sterilisation records reviewed before first fill.
- [ ] All fill-weight checks in limits and adjustments documented.
- [ ] Stopper/cap reject function challenged at start.
- [ ] Lyo loading and cycle parameters within limits, alarms deviated.
- [ ] 100% inspection plus AQL passed; vial reconciliation balances.

## Checked

Date: 2026-10-25. Jurisdictions: European Union (Annex 1) and United States (FDA aseptic processing guidance, October 2004).

Removed as unconfirmed: the 3-log depyrogenation figure, the Annex 1 capping air-supply statement and the USP chapter numbers and inspection timing (paywalled). The remaining content is line-operation craft that was not tied to a primary source, so the skill stays draft.

Method: documentation only; no commands were run.
