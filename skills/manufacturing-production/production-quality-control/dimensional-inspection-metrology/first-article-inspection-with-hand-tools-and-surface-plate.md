---
id: manufacturing-production.production-quality-control.dimensional-inspection-metrology.first-article-inspection-with-hand-tools-and-surface-plate
name: first-article-inspection-with-hand-tools-and-surface-plate
category: manufacturing-production
field: production-quality-control
product: dimensional-inspection-metrology
tags: [dimensional-inspection-metrology, dimensional-inspection, metrology, first-article-inspection, fai, as9102, ballooned-drawing, ballooning, calipers, micrometers, bore-gauge, height-gauge, dial-indicator, surface-plate, gauge-blocks, pin-gauges, thread-gauges, go-no-go, gd-t, flatness, perpendicularity, position, profile, runout, optical-comparator, vision-system, measurement-uncertainty, temperature-20c, inspection-report, production-quality-control]
level: practitioner
status: draft
description: "Inspect parts against the drawing with hand tools and a surface plate: balloon the drawing, pick the right gauge, measure GD&T features without a CMM, and complete a first-article report."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# First-article inspection with hand tools and a surface plate

**Goal:** confirm that the first part off a new or changed process meets every
requirement on the drawing, using the shop's manual metrology, and document it so the
evidence stands. For CMM programs see
manufacturing-production.production-quality-control.cmm-programming.writing-and-running-a-cmm-part-program;
deep GD&T theory in engineering-technology.technical-drawing-cad.gd-t.position-tolerancing-with-datums.

## 1. Prepare
- **Balloon** the drawing: number every characteristic — dimensions, GD&T frames,
  notes (material, finish, marking, deburr), general tolerances that apply to untoleranced
  dimensions. The FAI report has one line per balloon. Aerospace uses **AS9102** forms
  (Form 1 part accountability, Form 2 materials/specials, Form 3 characteristics).
- Confirm drawing and part revision match.
- Clean, deburr-free part, soaked to room temperature (reference 20 °C).

## 2. Pick the gauge (10:1 rule)
Gauge resolution/uncertainty should be about one tenth of the tolerance (4:1 minimum in many shops).
| Tolerance | Typical tool |
|---|---|
| ±0.1 mm and wider | Calipers (0.01 mm reading, but realistic ±0.02–0.03) |
| ±0.01–0.05 mm | Micrometer (0.001 mm), bore gauge, height gauge |
| Hole size go/no-go | Pin gauges (plus and minus pins), plug gauges |
| Threads | Go/no-go thread plug/ring gauges for the class (e.g. 6H/6g, 2B/2A) |
| Small features, profiles | Optical comparator, vision system |
Check zero/master before use; use the ratchet/friction thimble on micrometers for consistent force.

## 3. Surface plate techniques
- Plate clean (wipe; no paper towels leaving fibres), part on precision parallels or
  directly on the datum face as the drawing implies.
- **Height gauge** with a dial/test indicator for heights from datum A; zero on gauge blocks.
- **Flatness**: indicate across the surface with the part on three adjustable supports
  levelled to minimise reading (simple method), or on the plate with a test indicator through a hole; true flatness needs plane-based evaluation.
- **Perpendicularity**: square or cylinder square against datum, sweep indicator along the feature.
- **Parallelism**: datum face on plate, sweep indicator across the opposite face — full indicator movement = parallelism.
- **Runout**: part in V-blocks or between centres on the datum axis, indicator on the
  feature, rotate one turn; FIM is the runout.
- **Position of holes**: measure X/Y from datums (height gauge, or pins in holes and measure over pins),
  compute actual position as **2 × √(dx² + dy²)** for a diameter tolerance zone, add MMC bonus if specified.

## 4. Record
For each balloon: nominal, tolerance, actual reading (actual numbers, not "OK"),
gauge ID, pass/fail. Note the method where it's non-obvious (e.g. "position via pins
and height gauge"). Attach material certs, process certs (heat treat, plating) and
special process approvals for notes.

## 5. When something fails
- Re-measure with a second method or second person before declaring a failure.
- Record the actual, mark the nonconformance, and raise an NCR (see
  manufacturing-production.production-quality-control.nonconformance-root-cause.containment-and-8d-problem-solving).
- A failed FAI means the process isn't released; partial re-FAI covers only the
  changed characteristics after a fix if the customer allows.

## Gotchas
- Calipers on tight tolerances because "they read to 0.01".
- Measuring a warm part from the machine.
- Missing the notes and general tolerances — the most common FAI omissions.
- Using the jaws' tips on calipers (they flex) instead of the full jaw.
- Position computed as radial deviation and compared with a diametral tolerance (factor of 2).

## Verify
- [ ] Every drawing characteristic, note and general tolerance has a balloon and a report line.
- [ ] Each gauge has adequate resolution and is in calibration; IDs recorded.
- [ ] GD&T measured relative to the specified datums.
- [ ] Actual values recorded; failures double-checked and NCR raised.
- [ ] Certificates for materials and special processes attached.
