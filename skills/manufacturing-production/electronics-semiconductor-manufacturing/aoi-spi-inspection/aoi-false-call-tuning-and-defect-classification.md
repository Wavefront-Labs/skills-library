---
id: manufacturing-production.electronics-semiconductor-manufacturing.aoi-spi-inspection.aoi-false-call-tuning-and-defect-classification
name: aoi-false-call-tuning-and-defect-classification
category: manufacturing-production
field: electronics-semiconductor-manufacturing
product: aoi-spi-inspection
tags: [aoi-spi-inspection, aoi, spi, automated-optical-inspection, solder-paste-inspection, 3d-aoi, koh-young, cyberoptics, omron, viscom, mirtec, saki, false-call, false-call-rate, escape, ppm, defect-classification, ipc-a-610, review-station, library-tuning, package-library, thresholds, closed-loop, spi-volume, cpk, pcba, smt, quality]
level: practitioner
status: draft
description: "Tune AOI and SPI programs to cut false calls without creating escapes: golden-board debugging, threshold discipline, review-station classification to IPC-A-610 and escape tracking."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# AOI false-call tuning and defect classification

**Goal:** an inspection program operators trust — few enough false calls that they
look at every one properly, and no loosened threshold that lets real defects through.
The hidden failure mode of AOI is not missed defects at launch; it is operators
clicking "pass" on a review station that calls 40 false alarms a board.

## 1. Two numbers, always together
- **False-call rate** (calls per board or ppm of inspected locations).
- **Escape rate** (defects found downstream — ICT, functional test, customer — that
  AOI/SPI should have caught).
Tuning that lowers the first while raising the second is not tuning. Track both per
program, per week.

## 2. SPI: tune on data, not feel
- SPI measures volume, area, height and offset per pad. Typical starting limits are
  something like 50–150 % (or tighter) of nominal volume — *use your site/customer
  spec*; these vary widely.
- Watch **Cpk per pad group**, not just pass/fail. A drifting volume trend on fine-pitch
  pads warns of stencil clogging before failures start.
- Closed-loop (SPI → printer offset feedback) is common on modern lines; check it is
  correcting, not oscillating.
- Fix the **zero reference** first: warped panels or wrong board-height reference
  cause whole-board false volume errors.

## 3. AOI program debug workflow
1. Build the program from CAD/centroid data and the **package library**. Most false
   calls come from a library entry that doesn't match the real part (different
   vendor body colour, lead shape, marking).
2. Run a **golden board** (verified good) several times — any call is a false call by
   definition. Then run a deliberately defective set (missing, shifted, rotated,
   bridged, wrong polarity) — every one must be caught.
3. Fix false calls in this order:
   - wrong/variant package model → add a variant (alternate-part library entry);
   - region of interest picking up silkscreen, vias or a neighbour's fillet → adjust ROI;
   - lighting/colour issue (board finish change, ENIG vs HASL, mask colour) → re-teach;
   - only then widen a threshold, and only on that component/algorithm.
4. Re-run the golden and the defect set after every change. Keep a change log of
   who changed what threshold and why.

## 4. Classifying at the review station
Operators classify each call as **false call** or a defect type. Classify against
**IPC-A-610** for the product class (1, 2 or 3): e.g. a side overhang that is a
defect for Class 3 may be acceptable for Class 2. Use the site's visual aids.
- "Process indicator" (acceptable but not ideal) ≠ defect — record it differently
  so process engineers see trends without scrapping boards.
- When unsure, escalate to a certified IPC-A-610 inspector rather than pass.
- Clean reject codes matter: "other" as a defect category makes Pareto analysis useless.

## 5. Escapes
For every downstream escape: was the location inspected? Did it call and get passed
at review (operator issue) or not call at all (program issue)? Tighten the specific
algorithm, then rerun the defect set to check you didn't spike false calls elsewhere.

## Gotchas
- 2D AOI cannot reliably see lifted leads or coplanarity — 3D AOI or X-ray covers that.
- BGA and bottom-terminated parts (QFN) joints are not visible to AOI; inspect with
  X-ray on a sampling plan.
- A new board-shop lot (mask colour shade) can spike false calls overnight.

## Verify
- [ ] Golden board: zero calls across repeated runs.
- [ ] Defect sample set: 100 % caught.
- [ ] False-call and escape rates trended weekly per program.
- [ ] Threshold changes logged with reason and approver.

*Draft: thresholds and workflow names vary by vendor (Koh Young, Omron, Viscom etc.);
not validated on a specific platform.*
