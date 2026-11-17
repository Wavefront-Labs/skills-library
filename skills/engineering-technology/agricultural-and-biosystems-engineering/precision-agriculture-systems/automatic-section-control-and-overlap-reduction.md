---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.automatic-section-control-and-overlap-reduction
name: automatic-section-control-and-overlap-reduction
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, section-control, isobus, machine-networks, overlap-reduction, boom-sections, coverage-map, latency-compensation]
level: practitioner
status: draft
description: "Configure automatic section control for sprayers, spreaders and planters: boundaries, coverage logic, on/off timing, overlap tolerance and verification of savings."
sources:
  - "ISO standards catalogue (https://www.iso.org)"
  - "Pierce, Precision Agriculture (and related precision agriculture references)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Automatic section control and overlap reduction

**Goal:** switch implement sections off over already treated areas and outside the boundary.

## Set-up
1. **Implement geometry**: enter section widths, number of sections, and the distances from the receiver antenna to the implement (fore-aft and lateral) so that section positions are computed correctly; for towed implements enter the hitch length.
2. **Field boundary**: record the boundary (drive around the field with the correct implement offset) and set the boundary buffer or tolerance (inside or outside).
3. **Coverage logic**: choose the overlap tolerance (percent or distance of a section allowed over previous coverage before it switches off).
4. **Latency compensation**: set the turn-on and turn-off times of each section (valve opening and closing, product travel to the ground) so the coverage edge is correct at speed. Measure by running a test pass at working speed and observing the coverage line against known positions, or by following manufacturer procedures.
5. Use the same coverage map for sequential operations when needed.

## Benefits
Input savings from reduced overlap vary with field shape and operator skill; commonly cited ranges are on the order of 5-15 percent for irregular fields and smaller for rectangular ones, with greater benefit on hand-steered machines. Check against your own as-applied maps.

## Gotchas
- Wrong implement offset gives gaps or overlaps along headlands.
- Section control needs a controller capable of switching sections and flow meters consistent with the new area.
- Do not rely on automation near buffers or sensitive areas without verification.

## Verify
- [ ] As-applied map shows no double application beyond tolerance and no gaps at boundaries.
