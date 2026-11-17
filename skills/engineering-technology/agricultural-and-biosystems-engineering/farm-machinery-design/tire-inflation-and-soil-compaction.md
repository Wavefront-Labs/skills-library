---
id: engineering-technology.agricultural-and-biosystems-engineering.farm-machinery-design.tire-inflation-and-soil-compaction
name: tire-inflation-and-soil-compaction
category: engineering-technology
field: agricultural-and-biosystems-engineering
product: farm-machinery-design
tags: [agricultural-and-biosystems-engineering, farm-machinery-design, tire-inflation, tractor-performance, soil-compaction, contact-pressure, cone-index, radial-tires, tire-load]
level: practitioner
status: draft
description: "Choose tractor tyre inflation from axle load and soil conditions to cut slip, rolling resistance and subsoil compaction, using load-inflation tables and cone index."
sources:
  - "Srivastava, Goering, Rohrbach & Buckmaster, Engineering Principles of Agricultural Machines (ASABE)"
  - "ASABE Standards, Engineering Practices and Data (https://www.asabe.org)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Tyre inflation and soil compaction

**Goal:** lowest practical inflation for the load, since a larger footprint improves traction and lowers surface pressure.

## Procedure
1. Get true axle loads (see ballasting skill) and divide by tyre count for the load per tyre.
2. Use the tyre manufacturer's load-inflation table for the size and type (radials permit lower pressure than bias tyres for the same load, and typically have higher load capacity at a given pressure). Read the table at the working speed (field versus road).
3. Choose the lowest inflation that still carries the load at the table's allowed minimum; do not go below it. Raise it for road transport per the table's speed-adjustment guidance.
4. Estimate ground contact pressure: it is roughly tyre inflation pressure plus a carcass-stiffness effect; contact pressure under the tyre is what damages topsoil, while total axle load drives subsoil compaction depth.
5. Measure soil strength with a cone penetrometer (cone index, kPa) at the time of work; wet soil has low strength, so reduce load, use duals/tracks, or delay.
6. Controlled traffic and fewer passes reduce the area compacted regardless of tyre choice.

## Gotchas
- Axle load, not tyre pressure, determines deep compaction; low pressure helps topsoil.
- Under-inflation beyond table limits overheats and damages sidewalls.
- Central tyre inflation systems help but need sized compressors and rim compatibility.

## Verify
- [ ] Pressure within the table range for the measured load and speed.
- [ ] Footprint length/width increased after reducing pressure; slip dropped.
