---
id: manufacturing-production.packaging-operations.packaging-line-changeover.format-change-across-a-packaging-line-with-first-pack-release
name: format-change-across-a-packaging-line-with-first-pack-release
category: manufacturing-production
field: packaging-operations
product: packaging-line-changeover
tags: [packaging-line-changeover, packaging-operations, format-change, size-change, changeover, change-parts, format-parts, colour-coding, change-part-trolley, recipe, recipe-recall, servo, line-retiming, line-clearance, first-pack-check, first-off, allergen-changeover, wet-clean, label-reconciliation, smed, changeover-matrix, pack-material-staging]
level: practitioner
status: draft
description: "Change a whole packaging line between formats: changeover matrix, change-part control, recipe recall on every machine, re-timing, line clearance and a signed first-pack check before release."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Format change across a packaging line with first-pack release

**Goal:** move a multi-machine packaging line (filler → capper → labeller → coder →
checkweigher → case packer → palletiser) from format A to format B so that every machine
is set for B, nothing from A remains, and the first packs released are proven right.
For cutting the time itself, use the SMED method in
manufacturing-production.production-line-operations.line-changeover-smed.running-a-smed-changeover-study;
this skill is about doing the *whole line* correctly.

## 1. Know what kind of change it is — the changeover matrix
Build a matrix of from/to products showing for each pair what is needed:
- **Format change** (size/shape): change parts and settings.
- **Label/artwork change only:** label reels, coder message, line clearance.
- **Product change** with allergen or recipe difference: may need **full wet clean**
  and validation (e.g. allergen swab/ELISA or ATP), not just a dry clean.
- **Sequence** production to minimise big changes (e.g. allergen-free before
  allergen-containing, light colours before dark).

## 2. Before the line stops (external work)
- Change parts for B pulled from storage on a dedicated **trolley**, checked complete
  against a parts list (photo of the full set helps).
- Pack materials for B (film, labels, cases, caps) staged nearby, *not* on the line.
- Recipes ready, check gauges and samples available, QC informed of the time.

## 3. Change parts control
- **Colour-code** or **number** change parts by format (e.g. all 500 ml parts blue),
  stamped with the format ID so a 330 ml star wheel can't go on a 500 ml change.
- Store each set on its own shadow board or trolley; a missing piece is obvious.
- Damaged parts are tagged and replaced, never "made to fit".

## 4. Run the change, machine by machine
- Assign each person a machine and a sequence; work in parallel where LOTO allows.
- Swap parts, then **recall the recipe** for B on every machine HMI: filler, capper
  (torque), labeller (label length, offset), coder (message, date rule), checkweigher
  (limits), metal detector (product learn), case packer, palletiser (pattern),
  stretch wrapper. A forgotten checkweigher recipe is a classic miss.
- Many servo-driven lines store everything in recipes; mechanical lines rely on
  scale/counter positions recorded per format — set to the recorded numbers, don't
  eyeball.

## 5. Re-timing the line
- Run each machine in jog, then the line slowly: transfer points (star wheels, screws,
  guides) must hand product over cleanly.
- Machine-to-machine timing on mechanically linked or servo-synchronised sections
  must be reset to the format's values.
- Bring the line up in steps to rated speed; watch transfers at full speed, where
  misalignments show.

## 6. Line clearance (the safety-critical step)
Walk the whole line, top to tail, and remove **every** item of format A: product, packs,
labels, sleeves, leaflets, cases, printed film, coded cases in the reject bin. Check under
and behind conveyors and in reject bins. Second-person check and signature. **Label
reconciliation** (labels issued − used − returned − wasted = 0) is used where the risk
justifies it (pharma, allergens).

## 7. First-pack release
Before running at rate, a signed check of the first packs from the end of the line:
- Product, pack size, fill weight.
- Closure and seal.
- Label artwork/version, allergen panel, code and date correct and legible.
- Barcodes scan; case and pallet labels right.
- Inspection systems challenged (checkweigher, metal detector, vision).
Keep the retained sample with the signed sheet.

## Gotchas
- The changeover isn't over at "line running" — first-hour monitoring catches settings
  that drift once everything warms up.
- Partial changes (only the labeller changed) still need full line clearance for the
  changed materials.
- Record actual changeover time and issues per machine; the worst machine is the next
  SMED target.

## Verify
- [ ] Changeover type identified from the matrix (clean level included).
- [ ] Right colour-coded change parts fitted; recipes recalled on every machine.
- [ ] Line clearance signed by two people.
- [ ] First pack checked and signed before release at rate.
