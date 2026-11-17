---
id: creative-arts.fashion-design.collection-design.construction-callouts-and-stitch-types
name: construction-callouts-and-stitch-types
category: creative-arts
field: fashion-design
product: collection-design
tags: [fashion-design, collection-design, tech-pack, construction-callouts, stitch-types-iso-4915, seam-types, iso-4916, spi, stitch-class, seam-finish]
level: practitioner
status: draft
description: "Specify garment construction in a tech pack: ISO 4915 stitch classes (301, 401, 504, 514, 602), ISO 4916 seam types, stitches per inch, finishes and allowances."
sources:
  - https://www.iso.org/standard/10932.html
  - https://www.iso.org/standard/10933.html
  - https://www.astm.org/d6193-16r20.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Construction details, stitch and seam callouts

**Goal:** tell the factory exactly how each seam is built so samples come back as
designed, not as the factory's default.

## Stitch types (ISO 4915 / ASTM D6193)
| Code | Name | Use |
|---|---|---|
| 301 | Lockstitch | Most woven seams, topstitching |
| 401 | Chainstitch | Long seams in jeans, can unravel |
| 406 | Two-needle coverstitch | Knit hems |
| 504 | 3-thread overlock | Edge neatening |
| 514 | 4-thread overlock | Seaming knits |
| 516 | 5-thread safety stitch (401+504) | Woven seams in casualwear |
| 602/605 | Cover/flatlock stitches | Sportswear, knit seams |
| 101 | Single-thread chainstitch | Basting, buttons |

## Seam types (ISO 4916 classes)
Class 1 superimposed (plain seam), 2 lapped (felled seams in jeans/shirts), 3 bound,
4 flat (butted, flatlock), 5 decorative, 6 edge neatening, 7 attached parts, 8 single ply
(belt loops).

## What to call out per seam
- Seam/stitch type and **SPI** (stitches per inch; e.g. 10-12 for woven topstitch,
  12-14 for fine shirting) or stitches per cm.
- Seam allowance (e.g. 1 cm, 1.5 cm on side seams for alteration).
- Finish: overlocked, French seam, Hong Kong (bound), pinked, flat-felled.
- Topstitch distance from edge and number of rows (e.g. 0.6 cm twin needle).
- Press direction; interfacing/fusing areas; bartacks (position, length).

## Format
Callout arrows on flats with a code (S1, S2...), plus a construction table: code,
location, stitch type, SPI, thread, allowance, finish.

## Gotchas
- "Neaten seams" is ambiguous; name the stitch.
- Chainstitch hems unravel when caught; use lockstitch where stress matters.
- Too high SPI on heavy fabric perforates and weakens the seam.

## Verify
- [ ] Every seam on the flats has a callout code.
- [ ] Stitch type, SPI, allowance and finish given per code.
- [ ] Sample inspected seam by seam against the table.
