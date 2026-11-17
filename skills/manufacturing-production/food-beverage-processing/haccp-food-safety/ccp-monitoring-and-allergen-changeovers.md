---
id: manufacturing-production.food-beverage-processing.haccp-food-safety.ccp-monitoring-and-allergen-changeovers
name: ccp-monitoring-and-allergen-changeovers
category: manufacturing-production
field: food-beverage-processing
product: haccp-food-safety
tags: [haccp-food-safety, haccp, ccp, critical-control-point, critical-limits, monitoring, corrective-action, verification, prerequisite-programmes, prps, oprp, allergen-control, allergen-changeover, allergen-validation, atp-swab, allergen-swab, elisa, lateral-flow, hygiene-zoning, high-risk, high-care, low-risk, metal-detector, x-ray, foreign-body, brcgs, sqf, fssc-22000, iso-22000, fsma, preventive-controls, food-safety, food-processing]
level: practitioner
status: gated
description: "Run a food line inside its HACCP plan: monitor CCPs to critical limits, act and hold product when one drifts, run allergen changeovers that pass verification, and respect hygiene zoning."
sources: ["21 CFR 1240.61 (eCFR)", "Codex General Principles of Food Hygiene and HACCP Annex"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CCP monitoring and allergen changeovers

**Goal:** you know which steps on your line are CCPs, you check them as specified, and
when one is outside its critical limit you stop, hold and record — not adjust and carry
on. Inspector-side view: law-government.regulatory-inspection-and-certification.food-safety-inspection.food-hygiene-inspection-and-rating.

## 1. Know your CCPs
Typical CCPs on a line (your plan will differ):
| CCP | Critical limit example | Monitoring |
|---|---|---|
| Cooking | Core ≥75 °C (UK guidance) (gated: unconfirmed, source is paywalled or blocked) or a time/temperature equivalent; US often ≥165 °F (74 °C) for poultry (gated: unconfirmed, source is paywalled or blocked) | Probe thermometer, per batch or frequency |
| Pasteurisation | e.g. milk 72 °C / 15 s (HTST; matches 21 CFR 1240.61 for US milk) | Continuous chart + flow diversion |
| Chilling | Core temperature within set time | Probe + time log |
| Metal detection / X-ray | Detects Fe/non-Fe/SS test pieces of stated size (e.g. 2.0/2.5/3.0 mm — product-specific (gated: unconfirmed, source is paywalled or blocked)) | Test pieces at start, hourly (common), changeover, end |
| Sieve/magnet integrity | Intact, no damage | Check per shift |
The critical limit is a **pass/fail line**, not a target. Operating limits sit inside it
so you can correct before breaching.

## 2. Monitoring done right
- Calibrated probe (ice-point check daily is common: 0 °C ±1 °C in iced water (gated: unconfirmed, source is paywalled or blocked)).
- Probe the **thickest part / coldest point** of the largest item, not the convenient one.
- Record the actual reading, time and initials at the time. "✔" or "OK" isn't a record.
- **Metal detector test:** pass each test piece through the **centre of the aperture**
  (hardest to detect), inside or on the product, and confirm **reject to the locked bin**
  — not just the alarm. A detector that alarms but whose reject fails is a failed CCP.

## 3. When a CCP fails
1. Stop or divert the product.
2. **Hold everything since the last good check** — that's why check frequency matters.
3. Tell the supervisor/technical team; record the failure and the time.
4. Fix the cause (e.g. oven temperature, belt speed, detector sensitivity).
5. Product disposition is decided by technical/QA: re-process, re-check, or destroy.
6. Corrective action record completed and signed off.

## 4. Allergen changeovers
Sequence products from no/low allergen to allergen-containing where possible; a
changeover from allergen to non-allergen product requires a validated clean:
1. Remove all allergen-containing ingredients, WIP and packaging from the area.
2. **Dismantle** to the level in the SOP — allergen powders hide in seals, hoppers, scraper blades.
3. Wet or dry clean per the validated method (dry plants: vacuum, not compressed air,
   which spreads dust).
4. **Visual inspection** by a second person, using torch on hidden areas.
5. **Verification:** allergen-specific swab (lateral-flow, ELISA) on the validated
   locations where required; **ATP swab** proves cleanliness generally but **does not detect allergens** specifically.
6. Change packaging and labels — the wrong label (missing allergen declaration) is the top cause of food recalls in several markets.
7. Sign off before restart.

## 5. Hygiene zoning
- Respect the boundary between low-risk (raw) and high-risk/high-care (ready-to-eat)
  areas: separate PPE colour, footwear change or boot wash, handwash and sanitise at entry.
- Equipment, utensils and cleaning tools are **colour-coded** per zone and never cross.
- Forklifts and maintenance tools crossing zones follow the sanitation procedure.

## Gotchas
- Probing the item nearest the oven door.
- Test pieces placed on the edge of the belt (easy detection) instead of the centre.
- Assuming an ATP pass means allergen-free.
- Moving a line over to the next product while QA hasn't released the changeover.
- Rework containing allergens added to a non-allergen batch.

## Verify
- [ ] You can name every CCP on your line, its limit and its check frequency.
- [ ] All CCP records today have actual values, times and initials.
- [ ] Metal detector tests confirmed physical rejection of every test piece.
- [ ] Any failure: product held back to last good check, corrective action recorded.
- [ ] Allergen changeover visually checked, verified by swab where required, labels changed.
