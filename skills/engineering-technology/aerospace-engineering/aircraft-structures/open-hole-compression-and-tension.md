---
id: engineering-technology.aerospace-engineering.aircraft-structures.open-hole-compression-and-tension
name: open-hole-compression-and-tension
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [open-hole, open-hole-compression, ohc, oht, notched-strength, composite-structures]
level: practitioner
status: draft
description: "Use open-hole compression and tension strength for composite laminate design allowables, including test methods, layup dependence and notch-strength models."
sources:
  - "ASTM D6484 (OHC)"
  - "ASTM D5766 (OHT)"
  - "CMH-17 (Composite Materials Handbook)"
  - "Daniel and Ishai, Engineering Mechanics of Composite Materials"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Open-hole strength

**Goal:** strength of a laminate with a fastener hole or cut-out.

## Why it matters
Holes are everywhere in airframes, and tension and compression strength with a hole is a standard design-critical allowable for composites, often more limiting than pristine strength.

## Test methods
- ASTM D6484 for open-hole compression (OHC) and ASTM D5766 for open-hole tension (OHT). Check current revisions and fixture dimensions (hole diameter to width ratio, usually 1:6) before use.
- Test across hot-wet conditions as well as room temperature dry; the environmental knockdown is typically larger in compression.
- Reported strengths are gross-section stress at failure.

## Using the data
1. Nominal layup families (for example 25/50/25 for 0 degree, plus or minus 45, and 90 degree plies) give results that scale to similar layups; use a normalised-strength approach in CMH-17-style procedures.
2. Strain-based allowables are often derived so the same value can be used across layups of the same family.
3. Notch-strength models (point-stress and average-stress methods of Whitney and Nuismer) predict strength from unnotched strength and characteristic distances fitted to test data. They extrapolate poorly in hole diameter without verification.
4. Combine with the bearing-bypass check at the joint (see bolted-joint-bearing-bypass).

## Gotchas
- Layups with many 0 degree plies are notch-sensitive in compression.
- Edge distance and width effects change the result; follow the specimen geometry.
- Do not reuse allowables from a different material system or process.

## Verify
- [ ] The allowable cites specimen geometry, layup, condition and basis (A, B or mean).
