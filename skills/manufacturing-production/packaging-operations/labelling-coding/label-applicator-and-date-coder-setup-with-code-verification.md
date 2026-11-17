---
id: manufacturing-production.packaging-operations.labelling-coding.label-applicator-and-date-coder-setup-with-code-verification
name: label-applicator-and-date-coder-setup-with-code-verification
category: manufacturing-production
field: packaging-operations
product: labelling-coding
tags: [labelling-coding, packaging-operations, labelling, labeling, label-applicator, pressure-sensitive-labels, wrap-around-labeller, print-and-apply, pa, thermal-transfer-overprinter, tto, cij, continuous-inkjet, tij, thermal-inkjet, laser-coder, date-code, best-before, use-by, lot-code, batch-code, barcode, gs1, ean-13, gs1-128, sscc, barcode-verification, iso-15416, ocr, ocv, vision-system, wrong-label, recall]
level: practitioner
status: draft
description: "Set up label applicators and date coders (CIJ, TTO, laser, print-and-apply) and prove every pack carries the right label and a legible, correct code using start checks, vision and barcode grading."
sources: ["GS1 General Specifications", "ISO/IEC 15416 (linear barcode print quality)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Label applicator and date coder setup with code verification

**Goal:** the right label, in the right place, with the right date/lot code, legible and
scannable, on every pack. Wrong labels and wrong dates are among the commonest causes of
product recalls (allergen labels especially) — this station is a food-safety and legal
control point, not cosmetic.

## 1. Pressure-sensitive label applicators
- **Web path:** thread the label reel per the diagram, through the peel (dispensing)
  plate and onto the rewind for backing liner. Liner breaks usually come from too much
  rewind tension or a nicked peel edge.
- **Label sensor:** gap sensor (light through liner between labels) for most labels;
  clear labels need a capacitive or ultrasonic sensor. Teach it on each new label
  stock.
- **Product sensor and offset:** a photo-eye detects the product; a delay/offset sets
  where the label lands. Set it at production speed — at low speed it may look right
  and then drift when speed changes (unless the applicator is speed-compensated with an
  encoder, which it should be).
- **Speed match:** label dispensing speed equals conveyor speed, or labels wrinkle
  (too fast) or stretch/flag (too slow).
- Wipe-down brushes/rollers press the label on; wraparound labellers need the product
  spun evenly.

## 2. Coders — pick the technology, know its quirks
- **CIJ (continuous inkjet):** prints on almost anything at speed. Needs ink and
  make-up (solvent) topped up, nozzle cleaned on shutdown (follow the shutdown
  routine), and a print distance usually only a few mm. Solvent-based: ventilation
  and fire precautions.
- **TIJ (thermal inkjet):** cartridge-based, sharp, low maintenance, best on porous or
  coated surfaces; ink dries out if the cartridge is left uncapped.
- **TTO (thermal transfer overprinter):** prints onto flexible film by melting ribbon
  ink; the print head pressure, temperature/darkness and ribbon type must suit the
  film.
- **Laser:** marks the surface or coating, no consumables; requires the right substrate,
  and fume extraction and laser safety guarding.
- **Print-and-apply:** prints a label (often GS1-128/SSCC on cases or pallets) then
  applies it by tamp or blow. Tamp distance and timing matter.

## 3. Getting the code right
- Codes should be built by **date rules in the coder/line software** (offset from
  production date, e.g. +180 days) and the **recipe**, not typed by hand each shift.
  Hand entry is the classic root cause of wrong dates.
- Watch midnight rollovers, Julian dates, and shift/line codes.
- Check the printer clock against the real time at startup.

## 4. Start-of-run and in-run checks
- **Line clearance:** remove every label and pack material from the previous run before
  the new one starts. A single stray reel causes the mix-up.
- **First-pack check** with a second person (signed): label artwork and version, product,
  allergen statement, code content, position, legibility. Retain the signed sample.
- Repeat at set intervals, at every reel/ribbon change and after every restart.
- **Vision systems:** OCR/OCV reads the printed code; label-verification cameras or
  barcode scanners confirm the right label is on. They must reject to a locked bin, and
  must be **challenge-tested** (run a known bad pack) at start-up.

## 5. Barcodes
- GS1 barcodes (EAN-13/UPC-A on retail units, ITF-14 or GS1-128 on cases, SSCC on
  pallets) must **scan** and meet print quality. A **verifier** grades to ISO/IEC
  15416 (A–F, or 0–4); retailers commonly require grade C (1.5) or better — check your
  customer's spec.
- A scanner reading it is not the same as a passing verifier grade.
- Common faults: bars printed in the wrong direction on a TTO (ladder vs picket-fence
  orientation matters), low contrast (red bars do not scan), too-small quiet zones.

## Verify
- [ ] Line clearance done and signed; only current labels on the line.
- [ ] First pack checked by two people for artwork, allergens and code content.
- [ ] Code generated from rules/recipe; printer clock correct.
- [ ] Vision/scanner rejects challenge-tested at start and after changes.
- [ ] Barcode verified to the required grade.

*Uncertain: required verifier grade and code formats vary by retailer and region.*
