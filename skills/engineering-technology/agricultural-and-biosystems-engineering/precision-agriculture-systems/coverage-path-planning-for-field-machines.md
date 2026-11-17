---
id: engineering-technology.agricultural-and-biosystems-engineering.precision-agriculture-systems.coverage-path-planning-for-field-machines
name: coverage-path-planning-for-field-machines
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: precision-agriculture-systems
tags: [agricultural-and-biosystems-engineering, precision-agriculture-systems, coverage-path-planning, boustrophedon, headland-turns, dubins-path, turning-radius, field-coverage, fields2cover, agricultural-robotics]
level: advanced
status: draft
description: "Plan coverage paths for field robots and guided machines: swath width, headland passes, turn types, minimum radius, obstacles and metrics for non-working travel."
sources:
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
  - "Hunt & Wilson, Farm Power and Machinery Management"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Coverage path planning

**Goal:** a path that covers the field with minimal overlap, skips and non-working travel, and that the machine can actually drive.

## Elements
- Field geometry: boundary polygon, obstacles (poles, wet spots, trees) and the working direction; swath width equal to the implement effective width, with an overlap percentage if needed.
- Decomposition: simple convex fields are covered by parallel swaths (boustrophedon or back-and-forth); complex fields are split into convex cells to avoid short rows; choose the direction of travel to minimise the number of turns, which relates to the field's longest dimension, the slope (across the contour for erosion or along it for drainage), and soil traffic constraints (`controlled-traffic-farming-layout`).
- Headlands: one or more passes around the boundary give room to turn, and the finished swaths end at the headland edge. Turn inside the headland.
- Turns: the machine's minimum turning radius (and the implement trail) determines the turn type: a U-turn (loop) requires a row spacing at least two radii, a bulb or omega (fishtail) turn for narrower spacings, and skip-row patterns (sequences like 1 to 3, 5 and so on) to avoid reversing. Dubins curves are minimum-length paths for a vehicle that cannot reverse and has a bounded curvature.
- Sequencing: order the swaths to cut the total non-working distance and time; headland and turn time are costs in field efficiency (`field-efficiency-and-effective-capacity`).

## Implementation
Open-source tools exist (for example the Fields2Cover library) that generate swaths, headlands and turn connections for given vehicle parameters; the results are exported as guidance lines or tracks to the machine via the formats the controller supports (`shapefile-isoxml-and-geotiff-handling`, `ab-line-and-curved-guidance-patterns`).

## Metrics
Field coverage (percent of the area covered), overlap percent, non-working distance, number of turns, and total time; compare candidate directions and orders by simulation.

## Verify
- [ ] Simulate the path with the real turning radius and implement trail.
- [ ] Compare the planned and logged coverage after the first run.
- Unconfirmed: library features and versions; check the project.
