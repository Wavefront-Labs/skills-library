---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.ab-line-and-curved-guidance-patterns
name: ab-line-and-curved-guidance-patterns
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, ab-line-guidance, autosteer, machine-guidance, guidance-patterns, curved-guidance, headland, swath-width]
level: practitioner
status: draft
description: "Set up guidance patterns: AB lines, A+ heading, adaptive curves, identical curves, pivot and contour guidance, swath width, overlap and headland management."
sources:
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
  - "Zhang, Precision Agriculture Technology for Crop Farming (CRC Press)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# AB line and curved guidance patterns

**Goal:** the pattern that minimises overlap and driver effort for the field shape and operation.

## Patterns
- **Straight AB**: two points mark a line; parallel tracks are generated at the swath width; fast and simple.
- **A+ heading**: one point and a compass heading.
- **Curved (identical curve)**: the recorded curve is repeated for each pass; good for contour fields but errors accumulate across passes.
- **Adaptive curve**: each pass is based on the last pass; follows field boundaries without drift to the original curve; may accumulate odd shapes.
- **Pivot** guidance for centre-pivot fields, **spiral** and **contour** (terrace) patterns.

## Setup
1. Enter the implement working width accurately (and overlap setting if desired for spraying) and check by measuring.
2. Record the AB line at the exact edge of the first pass; choose the datum and keep the line files per field and year.
3. Name and store lines for each operation; use the same line for all operations in controlled traffic.
4. Headland: set the number of headland passes, turn type, and boundary buffer.
5. Transfer lines between machines using the manufacturer's file exchange or USB, or in ISO-XML where supported.

## Gotchas
- Tracks drift on curves if the receiver has poor accuracy (SBAS) - use RTK for repeatability.
- A line recorded with the implement on a slope can carry the offset; see terrain compensation.

## Verify
- [ ] Measure the distance between two adjacent passes in several places and compare with the swath width.
