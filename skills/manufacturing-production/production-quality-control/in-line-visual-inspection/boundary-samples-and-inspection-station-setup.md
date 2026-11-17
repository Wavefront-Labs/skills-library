---
id: manufacturing-production.production-quality-control.in-line-visual-inspection.boundary-samples-and-inspection-station-setup
name: boundary-samples-and-inspection-station-setup
category: manufacturing-production
field: production-quality-control
product: in-line-visual-inspection
tags: [in-line-visual-inspection, visual-inspection, cosmetic-inspection, boundary-samples, limit-samples, defect-catalogue, defect-library, appearance-standard, inspection-station, lighting, lux, viewing-distance, viewing-time, inspector-fatigue, inspector-qualification, attribute-agreement, escape-analysis, defect-escape, machine-vision, automated-optical-inspection, aoi, poka-yoke, 100-percent-inspection, sorting, production-quality-control]
level: practitioner
status: draft
description: "Make line-speed visual inspection reliable: defect catalogues and boundary samples, station lighting and viewing conditions, inspector qualification and rotation, and escape analysis."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Boundary samples and inspection station setup

**Goal:** inspectors on every shift make the same accept/reject call on the same part,
and defects that escape are traced to why. Human visual inspection is typically only
around **80–90% effective** at catching defects even under good conditions (a widely
quoted range from inspection studies; actual rates depend heavily on task) — so design
the station and standards to help people, and don't rely on inspection where prevention is possible.

## 1. Defect catalogue
- One page (or screen) per defect type: name, photo, where it typically occurs, cause,
  and **accept/reject criterion** in measurable terms where possible (e.g. "scratch
  > 5 mm long or visible at 600 mm on class A surface = reject").
- Classify surfaces/zones (class A visible, B semi-visible, C hidden) because the same
  mark can be acceptable on one and not another.
- Agree the catalogue with the customer where appearance is a customer requirement; get it signed.

## 2. Boundary (limit) samples
- Physical parts showing the **worst acceptable** and **just rejectable** condition for
  each key defect, labelled, signed and dated, stored at the station (and a master set
  in the quality lab).
- Control them like gauges: ID, review date, replace when worn/damaged.
- Photos help but don't replace physical samples for gloss, colour and texture.

## 3. Station design
- **Lighting**: enough and consistent — e.g. ~1000–2000 lux for fine visual inspection
  is a common guide (higher for very small defects); diffuse light for colour/contamination;
  low-angle (raking) light reveals scratches, dents and sink marks. Colour matching under a
  controlled source (D65 light booth).
- **Viewing distance, angle and time** defined (e.g. 450–600 mm, rotate part through
  defined views, ~X seconds per part) and written on the work instruction.
- Background contrasting with the defects sought; no glare.
- Parts presented at a comfortable height; inspector can stop or slow the line or has an
  accumulation buffer.
- **Reject path** that can't be confused with good: red bin, locked or with a lid,
  physically separated; rejected parts tagged with the defect.

## 4. Inspectors
- Eyesight checks (near acuity, colour vision where colour is inspected) at hire and periodically.
- **Qualification** with a blind test set including borderline parts; attribute
  agreement study (see
  manufacturing-production.production-quality-control.measurement-system-analysis.running-a-gage-rr-and-acting-on-it)
  — target high agreement with the standard and near-zero misses.
- **Rotation/breaks**: vigilance drops after ~20–30 minutes of continuous monotonous
  inspection (vigilance research; set your own rotation by trial). Rotate tasks.
- Keep defect rates visible to the inspector; very low defect rates make detection worse (people stop expecting defects).

## 5. Escape analysis
When a customer finds a defect you should have caught:
1. **Contain**: check stock and WIP, sort with an enhanced (possibly 200%) inspection.
2. Why did it **occur** (process root cause) **and** why did it **escape** (detection root cause)?
   Was it in the catalogue? Was the boundary sample clear? Was lighting/time adequate?
   Was the inspector qualified/rotated? Was the reject bin secure?
3. Fix both, and verify detection with a seeded test (plant known defects; confirm they're caught).
4. Feed back into PFMEA detection ratings and the control plan.

## 6. Machine vision
Automated inspection (AOI, cameras) suits repeatable, well-defined defects. It still needs
boundary samples for setup, daily **challenge parts** to prove detection, and false-reject
monitoring — operators bypassing a "nuisance" camera is a classic escape cause.

## Gotchas
- Verbal standards ("small scratches are OK").
- Mixing reworked parts back without re-inspection.
- Boundary samples that have faded or been handled until the defect changed.
- Adding more inspection instead of fixing the process causing the defect.

## Verify
- [ ] Every defect type has a catalogue entry with measurable criteria and boundary samples in date.
- [ ] Lighting measured at the inspection point and recorded; viewing conditions in the instruction.
- [ ] Inspectors qualified on a blind test set; rotation in place.
- [ ] Reject parts physically segregated and tagged.
- [ ] Each escape has an occurrence and an escape root cause with verified fixes.
