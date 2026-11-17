---
id: manufacturing-production.printing-production.prepress-workflow.preflight-imposition-trapping-and-platesetting
name: preflight-imposition-trapping-and-platesetting
category: manufacturing-production
field: printing-production
product: prepress-workflow
tags: [prepress-workflow, prepress, preflight, pdf-x, pdf-x-4, pdf-x-1a, acrobat-preflight, enfocus-pitstop, kodak-prinergy, esko-automation-engine, heidelberg-prinect, agfa-apogee, screen-equios, imposition, signature, creep, bleed, trapping, overprint, rich-black, total-area-coverage, tac, ink-limit, spot-colour, rip, ctp, computer-to-plate, platesetter, plate-curve, soft-proof, hard-proof, contract-proof, jdf, cip3]
level: practitioner
status: draft
description: "Take a customer PDF to plates: preflight to PDF/X rules, fix common faults, impose signatures with creep, trap and overprint correctly, proof, and output plates in a Prinergy/Esko-style workflow."
sources: ["ISO 15930 PDF/X (general reference)", "Ghent Workgroup output suite and specifications (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Prepress: preflight, imposition, trapping and platesetting

**Goal:** catch every file problem before it costs plates and press time, and deliver
correctly imposed, trapped, proofed plates (or digital press output) that match what
the customer approved.

## 1. Receive and preflight
Normalise to a **PDF/X** standard your workflow expects (PDF/X-4 keeps live
transparency and ICC; PDF/X-1a flattens to CMYK/spot). Run preflight (Acrobat
Preflight, Enfocus PitStop, or the workflow's built-in, e.g. Prinergy or Esko
Automation Engine) with a profile built to the job type. Check at least:
- **Page size, trim and bleed** (typically 3 mm / 0.125 in) present and boxes
  (TrimBox/BleedBox) correct.
- **Fonts** embedded.
- **Image resolution** — commonly ≥ 300 ppi effective for offset at 150–175 lpi; flag
  below ~200.
- **Colour:** RGB or unexpected spot colours, spot names consistent (a "PMS 185" and
  "PANTONE 185 C" give two plates).
- **Total area coverage (TAC/ink limit)** — e.g. around 300–320% for coated sheetfed,
  lower for uncoated/newsprint; over-limit shadows set off and dry slowly.
- **Rich black** text and fine lines (4-colour small text misregisters) and
  **registration colour** used for artwork (prints on all plates).
- **White overprint** set on objects (they disappear on output) and unexpected
  overprint/knockout.
Fix what is safe to fix (convert RGB with the agreed profile, map spot names); send
anything that changes appearance back to the customer for approval.

## 2. Imposition
- Choose the **signature/layout** from the binding and press sheet: e.g. 16-page
  signatures for perfect binding, work-and-turn vs sheetwise for small runs,
  gang-up for cards.
- Use the binding team's **folding dummy** to confirm page order and grain direction.
- **Creep (shingling)** for saddle-stitched work: inner pages push out at the fore-edge;
  apply the calculated creep (depends on paper caliper and page count) so margins stay
  even after trimming.
- Add marks: crops, folds, colour bar, registration, collation marks on spines for
  perfect binding, gripper and tail margins per press.

## 3. Trapping and overprint
- **Trapping** adds small overlaps where adjacent colours meet so misregistration
  doesn't show white gaps. Workflow (in-RIP) trapping is normal; typical trap widths
  are small (e.g. ~0.1–0.15 mm for sheetfed; larger for flexo, often 0.2 mm+).
- **Lighter colours spread under darker**; black typically **overprints** rather than
  knocks out (small black type and lines always).
- Don't double-trap: files already trapped by the designer need trapping disabled for
  those objects.

## 4. Proofing
- **Soft proof** on a calibrated monitor or online approval portal for content.
- **Contract proof** (hard proof) printed to a certified condition (e.g. FOGRA51/
  GRACoL) with a measured control strip (e.g. Ugra/FOGRA Media Wedge) that passes — that
  is what the pressroom matches.
- Get signed approval of the **final** version; record the version number.

## 5. Platesetting (CTP)
- Apply the right **plate curve** (calibration) for press/paper condition; output a
  control target and measure a plate with a plate reader periodically.
- Check plates after processing: correct job/colour/version, full image, no scratches,
  punch/bend correct for the press.
- Keep the 1-bit or TIFF output archived for remakes.

## Gotchas
- Replacing a page late: re-run preflight and re-impose; don't patch a single plate
  without checking it against the others (version mismatch across colours).
- Transparency + spot colours + overprint is where unexpected output hides; check
  with Acrobat Output Preview / separation preview before plating.

## Verify
- [ ] Preflight report clean or exceptions approved by customer.
- [ ] Imposition checked against folding dummy; creep applied where needed.
- [ ] Trap/overprint behaviour checked in separation preview.
- [ ] Contract proof's control strip passes; approval signed for this version.
- [ ] Plates checked for job, colour, version and curve before release to press.

*Draft note:* numeric thresholds are typical industry values; customer specs and your
press conditions decide actual values.
