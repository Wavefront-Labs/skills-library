---
id: engineering-technology.industrial-manufacturing-systems-engineering.facility-layout-design.material-flow-analysis-and-block-layout
name: material-flow-analysis-and-block-layout
category: engineering-technology
field: industrial-manufacturing-systems-engineering
product: facility-layout-design
tags: [facility-layout, plant-layout, block-layout, material-flow, from-to-chart, flow-matrix, systematic-layout-planning, slp, muther, rel-chart, closeness-rating, aeiou, craft-algorithm, process-layout, product-layout, cellular-layout, pq-analysis, spaghetti-diagram, distance-cost, department-sizing, aisle-allowance, factory-planning, industrial-engineering]
level: practitioner
status: draft
description: "Turn routings and volumes into a block layout: from-to charts, flow-distance scoring, SLP closeness ratings, department sizing and aisle/expansion allowances."
sources:
  - "Muther, Systematic Layout Planning (SLP)"
  - "Tompkins et al., Facilities Planning"
  - "Heragu, Facilities Design"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Material-flow analysis and block layout

**Goal:** place departments so that the heaviest material flows travel the shortest
distances, with space sized from capacity rather than guessed, and a layout score you
can defend against the alternatives.

## 1. Classify the product mix first (P-Q analysis)
Rank products by annual quantity (Pareto). The shape picks the layout type:
- A few products carry ~70-80% of volume → **product (line) layout** or dedicated cells
  for those, and a process layout for the long tail.
- Flat curve, many low-volume parts → **process (functional) layout**, with
  **cells** for part families found by grouping routings (production-flow analysis).
Do not force a single layout type on a bimodal mix; most real plants are hybrids.

## 2. Build the flow matrix (from-to chart)
For each part family: routing × annual volume ÷ unit-load size = **moves per year**
between department pairs. Use *moves* (forklift trips, totes), not pieces: 10,000
pieces in 50-piece totes is 200 moves. Weight by handling difficulty if loads differ
wildly (a pallet vs a tote), and say what weighting you used.

Worked mini-example: Saw → Mill carries 1,200 moves/yr, Mill → Deburr 1,100,
Saw → Weld 150. Saw-Mill-Deburr must be a tight chain; Weld can sit further away.

## 3. Add non-flow relationships (SLP REL chart)
Flow is not everything. Rate each pair A/E/I/O/U/X (absolutely necessary → undesirable):
shared utilities, supervision, noise, contamination (paint vs clean assembly = X),
fire separation. Convert to numbers for scoring (a common scheme: A=4, E=3, I=2, O=1,
U=0, X=-4 or a large negative; any consistent scale works, state it).

## 4. Size each department from capacity
Machines needed = (annual demand × standard time) ÷ (available hours × OEE).
Example: 180,000 parts × 2.4 min = 7,200 h; 2 shifts × 7.5 h × 240 days = 3,600 h;
at 80% OEE → 2,880 effective h → 7,200 ÷ 2,880 = 2.5 → **3 machines**.
Area per machine = footprint + operator zone + WIP/staging + maintenance access.
Then add aisle allowance (typically 10-30% of floor area depending on truck type;
forklift aisles roughly 3.5-4 m vs ~1 m pedestrian — check the truck's right-angle
stacking aisle spec) and an **expansion allowance** of 15-25% for growth.

## 5. Generate alternatives
- Draw a **relationship diagram**: A-pairs and high-flow pairs as short thick lines.
- Fit to the building as **block layouts** (rectangles to scale), honouring fixed
  features: columns, docks, crane bays, floor-load zones, pits, utility mains.
- Produce at least **3 alternatives** (e.g. U-flow, straight-through, L-flow). A U
  puts receiving and shipping on one dock face and shares staff; straight-through
  suits separate docks and clean/dirty segregation.
- Algorithms (CRAFT-style pairwise exchange, or modern solvers) can improve a block
  plan but will happily produce unbuildable shapes; treat them as idea generators.

## 6. Score and choose
Flow score = Σ (moves_ij × distance_ij), distance measured **rectilinear** between
department pick-up/drop-off points (not centroids, if you know them). Add a weighted
qualitative score (REL satisfaction, flexibility, safety, cost of moves). Present the
table; a layout that is 8% better on flow but blocks future expansion often loses.

## Gotchas
- Volumes used for layout must be **forecast** volumes for the layout's life, not
  last year's. Run the score at low and high demand scenarios.
- Monuments (heat-treat, paint, presses with pits) are expensive to move: place them
  first and design around them.
- Overhead conveyors, floor drains and compressed-air drops are layout constraints too.
- Walk the **spaghetti diagram** of the current state; the data often misses rework
  loops and trips to the quality lab.
- Check emergency egress, fire-code travel distances and aisle widths against your
  local code (they vary by jurisdiction; check the current edition).

## Verify
- [ ] Layout type is justified by the P-Q curve, not habit.
- [ ] From-to matrix is in moves/year with the unit-load assumption stated.
- [ ] Every department size traces to a capacity calculation including OEE.
- [ ] At least three alternatives scored on Σ flow × distance plus qualitative factors.
- [ ] X-relationships are separated; fixed features and expansion space are respected.
- [ ] Score rechecked at a high-demand scenario.
