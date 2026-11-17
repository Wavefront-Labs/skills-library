---
id: transportation-logistics.maritime-navigation-seamanship.cargo-operations-stability.loading-plan-stability-and-draught-survey
name: loading-plan-stability-and-draught-survey
category: transportation-logistics
field: maritime-navigation-seamanship
product: cargo-operations-stability
tags: [cargo-operations-stability, ship-stability, maritime-navigation-seamanship, stowage-plan, loading-computer, loadicator, gm, metacentric-height, kg, free-surface-effect, gz-curve, intact-stability, is-code, shear-force, bending-moment, trim, list, draught-survey, draft-survey, displacement, deadweight, hydrostatic-tables, loading-sequence, cargo-securing-manual, bulk-carrier, container-ship]
level: advanced
status: draft
description: "Plan and run cargo ops on a ship: stowage and loading sequence in the loading computer, GM/GZ and free-surface checks, shear/bending limits, trim and list control, and a draught survey."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Loading plan, stability and draught survey — load it, keep it upright, prove the quantity

**Goal:** load or discharge cargo so the ship stays within stability criteria and hull
strength limits at every stage (not just the final condition), sails at the right
trim and draught, and the quantity is verified.

## 1. Plan the stow
- Cargo list: weights, stowage factors (m³/t), special cargo (DG, heavy lifts, reefer).
- Allocate to holds/bays respecting: port rotation (discharge order), tank top /
  hatch cover / stack weight limits, DG segregation, lashing/securing per the
  **Cargo Securing Manual**, visibility line (containers), load line draught.
- Enter the plan into the approved **loading computer (loadicator)** — it computes
  displacement, draughts, trim, GM, GZ curve, shear forces (SF) and bending moments (BM).

## 2. Stability checks (intact)
- **GM (corrected for free surface)** = KM − KG − FSC. Must meet the minimum from
  the stability booklet / IS Code criteria (e.g. GM₀ ≥ 0.15 m, plus GZ area and max GZ
  requirements — the loadicator checks all criteria).
- **Free surface:** each slack tank reduces effective GM; keep tanks pressed up or
  empty where possible, especially large wide tanks.
- Too low GM → tender ship, large heel in turns and wind; too high GM → stiff ship,
  violent rolling, cargo securing loads high (container ships aim for moderate GM).
- Grain cargoes: grain heeling moment check (SOLAS VI / Grain Code).

## 3. Strength — every stage
- SF and BM must stay within **harbour limits** during cargo ops and **sea limits** at
  sailing. Check intermediate stages: loading one end first can exceed limits even
  if the final condition is fine.
- Bulk carriers: agree a **loading/unloading sequence** with the terminal (BLU Code),
  pour by pour, with ballast operations matched to cargo rate. Fast loaders can put
  thousands of tonnes in a hold in an hour — ballast pumps must keep pace.

## 4. Running cargo ops
- Read draughts (fore, aft, midships both sides) regularly; compare with the plan.
- Correct list early with ballast; unexplained list = possible wrong weight, tank
  leak or cargo misplacement — stop and find out.
- Hold cargo for the final trimming pours; finish at planned trim.
- Keep a deck log of hold quantities, ballast operations and draught readings.

## 5. Draught survey (quantity check)
Displacement before and after minus changes in non-cargo weights = cargo.
1. Read six draughts (F, M, A port and starboard) in calm conditions; note water density
   with a hydrometer at several depths.
2. Correct to perpendiculars (marks aren't at the perpendiculars); compute mean of
   means (quarter-mean: (F + 6M + A)/8 accounts for hog/sag).
3. Enter hydrostatics for displacement at that draught; apply **trim corrections**
   (first and second, using LCF and MTC) and **density correction**
   (displacement × measured density / table density, typically 1.025).
4. Subtract **deductibles**: ballast (sound every tank, correct for trim/list),
   fresh water, fuel, lube oil, and the constant.
5. Final minus initial net displacement = cargo loaded (or reverse for discharge).
Accuracy of a careful survey is often quoted around ±0.5%; poor ballast soundings are
the usual error.

## Gotchas
- Using approximate weights for heavy containers — misdeclared weights cause stack
  collapses; VGM exists for this.
- Slack ballast tanks overlooked in GM calculations.
- Sea state making draught readings guesses; use a draught tube or average over swells.
- Loadicator not validated: run the class test conditions periodically.

## Verify
- [ ] Every stage of the loading sequence within harbour SF/BM limits.
- [ ] Departure condition meets all intact stability criteria with free surface.
- [ ] Draughts read and logged; list explained and corrected.
- [ ] Draught survey with density and trim corrections, deductibles sounded.
- [ ] Cargo secured per Cargo Securing Manual before sailing.

*Uncertainty:* criteria quoted are IS Code general minima; ship-type rules and the approved stability booklet govern.
