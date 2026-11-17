---
id: engineering-technology.aerospace-engineering.aircraft-structures.impact-damage-bvid-cai
name: impact-damage-bvid-cai
category: engineering-technology
field: aerospace-engineering
product: aircraft-structures
tags: [aircraft-structures, composites, composite-laminates, bvid, impact-damage, compression-after-impact, astm-d7136, astm-d7137]
level: advanced
status: draft
description: "Plan composite impact damage tolerance: barely visible impact damage, compression-after-impact testing, and how detectability drives design allowables."
sources:
  - "ASTM D7136 (drop-weight impact) and D7137 (compression after impact)"
  - "FAA advisory circular 20-107 series on composite aircraft structure"
  - "CMH-17 volume 3"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Impact damage and BVID

**Goal:** structure that carries ultimate load with undetected impact damage and limit load with detectable damage.

## Concepts
- **BVID:** barely visible impact damage: below the threshold of reliable detection in routine inspection but large enough to reduce strength (delamination, matrix cracking beneath a small dent).
- **Compression after impact (CAI):** residual compression strength after a standard impact; ASTM D7136 specifies the drop-weight impact, D7137 the CAI test.
- Damage categories in the composite guidance (AC 20-107 series): from barely visible damage requiring ultimate load capability, through visible damage requiring limit load capability until detection, to discrete-source damage with reduced loads. Check the current advisory circular.

## Practice
1. Use CAI strength (basis values from CMH-17 style statistics) to set strain allowables for damaged laminates.
2. Define impact energy by the likely threats (tool drop, hail, runway debris) and the detectability cut-off at which a dent is found by visual inspection (derived from test and inspection capability).
3. Verify with coupon, element and component tests; relate to analysis methods.
4. Design thickness and stiffeners, softening strips and toughened resins to raise CAI.

## Gotchas
- Detectability depends on paint, surface and inspector; programme-specific.
- CAI depends on laminate and thickness; coupons do not scale blindly.

## Verify
- [ ] Allowables used trace to CAI tests with stated conditions.
