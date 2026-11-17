---
id: manufacturing-production.printing-production.label-packaging-printing.inline-converting-barcode-grading-and-brand-colour
name: inline-converting-barcode-grading-and-brand-colour
category: manufacturing-production
field: printing-production
product: label-packaging-printing
tags: [label-packaging-printing, label-printing, packaging-printing, pressure-sensitive-labels, self-adhesive-labels, folding-cartons, flexible-packaging, inline-converting, rotary-die-cutting, magnetic-cylinder, flexible-die, matrix-stripping, slitting, rewinding, core-size, unwind-direction, lamination, cold-foil, barcode-verification, iso-15416, iso-15415, ean-13, upc-a, gs1-128, qr-code, data-matrix, barcode-grade, brand-colour, pantone, spot-colour-matching, delta-e, 100-percent-inspection, avt, bst]
level: practitioner
status: draft
description: "Make labels and packaging that pass: inline die-cut and matrix strip, slit and rewind to spec, verify barcodes to ISO 15416/15415 grades, match brand spot colours by measurement."
sources: ["ISO/IEC 15416 and 15415 barcode print quality (general reference)", "GS1 General Specifications (general reference)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Labels and packaging: inline converting, barcodes and brand colour

**Goal:** deliver rolls or cartons that run on the customer's packing line, scan at
the till, and match the brand — the three ways label and packaging jobs get rejected.

## 1. Inline die-cutting and matrix stripping (pressure-sensitive labels)
- **Die choice:** flexible dies on a magnetic cylinder for most label work (fast
  changeover); solid rotary dies for long runs/abrasive materials.
- **Cut depth / anvil gap:** cut through face stock and adhesive, **kiss** the
  liner — never cut it. Liner cut-through causes web breaks on the customer's
  applicator. Check by peeling a label and flexing the liner; look for scoring.
  Adjust with shims/gap-adjustable anvils, and match die to liner caliper
  (e.g. PET vs glassine liners differ).
- **Matrix stripping:** waste matrix peeled off right after the die. Breaks come from
  small gaps between labels, sharp internal corners, low matrix tension, or
  adhesive "oozing" at warm temperatures. Strip angle and tension are the levers.

## 2. Slitting and rewinding to the customer's spec
Every customer applicator needs exactly:
- **Core size** (e.g. 76 mm / 3 in), **max roll diameter** or labels per roll.
- **Unwind/winding direction** — the "wind position" diagram (positions 1–8 in common
  charts: copy outside/inside, head/foot/left/right off first). Getting this wrong
  makes the whole order unusable on the line.
- **Splices:** allowed or not, how many per roll, how marked.
- **Missing labels:** tolerance (often zero for automatic application); use a
  label-gap detector or inspection system and a rewinder with stop-on-missing.
Label the roll with job, quantity and wind position.

## 3. Barcode verification
- **Scan is not verify.** A barcode that scans on a phone can still fail at retail.
  Use an **ISO-conformant verifier** (calibrated with its conformance card).
- **Linear (EAN-13, UPC-A, GS1-128):** ISO/IEC 15416 grades (A–F, or 4.0–0.0) on
  parameters like symbol contrast, edge contrast, modulation, defects, decodability.
  **Matrix (QR, Data Matrix):** ISO/IEC 15415.
- Typical retail requirement: **grade C (1.5) or better** at the specified aperture and
  wavelength (often 660 nm red light) — check the brand/GS1 spec for the application.
- Common faults and fixes:
  - **Bar width growth** (dot gain in print direction) — barcodes oriented with bars
    in the machine direction ("picket fence") are more tolerant; apply **bar width
    reduction (BWR)** in prepress for the process.
  - **Low contrast** — red, orange or yellow bars, or dark backgrounds, look like
    "no bars" under red light; insist on dark bars (black/blue/dark green) on light
    backgrounds.
  - **Quiet zone** cut by die-line or trim — keep it clear.
  - **Size below minimum magnification** for the symbology.
- Verify at the start, after any change, and at intervals; keep the reports.

## 4. Brand colour matching
- Work to the brand owner's **standard** (a physical drawdown or Lab target with a
  tolerance, often ΔE00 ≤ ~2 for primaries — whatever the spec says), not "PANTONE
  number on the screen".
- Spot inks: mixed by the ink supplier/ink kitchen from a formulation for **your
  substrate and anilox/cylinder**; drawdowns on the actual substrate before the run.
- Opaque white underlay on films/metallised: its opacity changes every colour printed
  over it — control white density.
- Measure on press (spectro, ΔE to standard) at start, intervals and end; record.

## 5. Inspection
100% inspection systems (camera vs approved master — e.g. AVT/BST-style) catch
missing print, spots, misregister and label count. Set sensitivity to defect specs,
review flagged events, and remove/flag defective labels on the rewinder.

## Verify
- [ ] Liner not cut; matrix strips cleanly at running speed.
- [ ] Core, roll size and wind position match the spec and are on the roll label.
- [ ] Barcodes graded with a calibrated verifier to required grade; reports saved.
- [ ] Brand colours measured within tolerance against the approved standard.
- [ ] Inspection events reviewed; defective labels removed or flagged.

*Draft note:* grade and ΔE tolerances vary by retailer/brand; use the customer spec.
