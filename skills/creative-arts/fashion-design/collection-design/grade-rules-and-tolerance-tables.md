---
id: creative-arts.fashion-design.collection-design.grade-rules-and-tolerance-tables
name: grade-rules-and-tolerance-tables
category: creative-arts
field: fashion-design
product: collection-design
tags: [fashion-design, collection-design, size-chart, grade-rules, measurement-tolerance, grading-spec, size-spec, graded-specs]
level: practitioner
status: draft
description: "Write grade rules and tolerance tables for a spec sheet: increments per POM between sizes, break points, and allowed deviations for sample and bulk inspection."
sources:
  - https://www.astm.org/d5585-21.html
  - https://en.wikipedia.org/wiki/Grading_(tailoring)
  - https://www.iso.org/standard/61686.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Grade rules and tolerance tables for the spec

**Goal:** a graded measurement table and tolerances in the tech pack so every size is
produced consistently; production grading of patterns itself is a pattern-drafting task.

## Grade rules
- From the brand size chart, take the body interval per size (e.g. bust +4 cm, waist
  +4 cm, hip +4 cm in mid sizes).
- Apply to each POM proportionally:
  - Chest width (half) = +2 cm per size,
  - Body length = +0.5-1 cm per size,
  - Across shoulder = +1 cm,
  - Sleeve length = +0.5 cm,
  - Neck width = +0.5 cm.
- **Break points**: larger intervals at the extremes (plus or petite) where bodies
  change differently; split grade tables if needed.
- Keep small details constant (pocket size, placket width) or step them every 2 sizes.

## Tolerances (indicative)
| POM type | Tolerance |
|---|---|
| Lengths over 50 cm | +/-1-1.5 cm |
| Widths (chest, hip half) | +/-1 cm |
| Small details (neck, cuff, pocket) | +/-0.3-0.5 cm |
| Knits | wider than wovens |
State whether tolerance is plus/minus or one-sided (e.g. waist must not be smaller).

## Format
Spec table: POM code, description, tolerance, then columns per size; base size marked.
Grade column shows the increment for checking.

## Gotchas
- Grading length the same as width makes large sizes too long; lengths grade less.
- Tolerances wider than the grade increment allow one size to measure as the next.
- Changing the base sample after grading requires re-grading the whole table.

## Verify
- [ ] Every POM has a grade increment and tolerance.
- [ ] Tolerances smaller than grade increments.
- [ ] Size set samples measured against the table.
