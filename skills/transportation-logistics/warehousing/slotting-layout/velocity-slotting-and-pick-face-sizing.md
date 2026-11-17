---
id: transportation-logistics.warehousing.slotting-layout.velocity-slotting-and-pick-face-sizing
name: velocity-slotting-and-pick-face-sizing
category: transportation-logistics
field: warehousing
product: slotting-layout
tags: [slotting, re-slotting, velocity-slotting, abc-analysis, cube-movement, cube-per-order-index, coi, golden-zone, pick-face, forward-pick-area, replenishment, days-of-supply, warehouse-layout, u-flow, through-flow, aisle-width, ergonomics, affinity, family-grouping, heavy-low, slotting-software, travel-time]
level: practitioner
status: draft
description: "Placing products for throughput: velocity and cube analysis, golden-zone placement, sizing pick faces from demand and replenishment, re-slotting programmes, and layout flow choices."
sources: ["Frazelle, World-Class Warehousing and Material Handling (slotting and COI)", "Bartholdi & Hackman, Warehouse & Distribution Science (free online text)", "NIOSH lifting guidance (ergonomic zone)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Velocity slotting and pick-face sizing

**Goal:** put the most-picked items where picking them is quickest and least strenuous,
with faces big enough that replenishment doesn't interrupt picking — and keep it that
way as demand shifts.

## 1. Get the data (last 8–13 weeks, adjust for seasonality)
Per SKU: **pick lines (hits)**, units shipped, unit and case dimensions and weight,
units per case, lines per order, and which SKUs are ordered together.

## 2. Rank and classify
- **Velocity by hits** (pick lines, not units) drives travel: A ≈ top 15–20 % of SKUs
  that make up ~70–80 % of picks.
- **Cube movement** = units shipped × unit cube — drives how much space the face needs.
- **Cube-per-order index (COI)** = storage space required ÷ picks; low COI items
  (small, many picks) go closest to the start/end of the pick path.

## 3. Placement rules
- **Golden zone**: waist to shoulder height (~0.7–1.5 m) for A items — fastest and
  least strain; heavy items at waist height or below, never overhead.
- A items near the pick-path start/pack area or main aisle; C items at the back/high.
- **Families/affinity**: items often ordered together near each other (kits, matched
  sizes) — but separate **look-alikes** that cause mispicks.
- Heavy and crushable: heavy first in pick sequence and low; fragile later.
- Hazmat, temperature and security classes in their segregated zones first; velocity
  within each zone.

## 4. Size the pick face
Face capacity should cover **days of supply** that matches the replenishment cycle:
- Capacity ≥ max daily demand × target days (e.g. 1–5 days for fast movers) and
  ≥ one full case (or one pallet for pallet-flow) so a replenishment fits when it's
  triggered.
- **Min/max replenishment:** min (trigger) ≥ demand during replenishment lead time +
  safety; max = face capacity.
- Example: 120 units/day, case of 24, replen lead time 2 h in a 16 h day: min ≥
  120 × 2/16 = 15 + safety → 24 (one case); target 2 days → 240 → face of 10 cases.
- Choose the face type by cube movement: shelving/carton flow for small and medium,
  pallet flow or floor pallet for very high cube movement.

## 5. Re-slotting programme
- Re-run analysis monthly or seasonally; move only SKUs with the biggest benefit
  (travel saved vs. move labour) — e.g. top 50 swaps per week.
- Schedule moves in quiet shifts; update WMS locations and pick-path sequence at the
  same time; label the new slots before moving.
- Slot new SKUs with forecast-based assumptions, then correct after 4 weeks of data.

## 6. Layout notes
- **U-flow** (receiving and shipping on the same side): shares docks, puts fast movers
  near both — common default. **Through-flow** (opposite sides) suits cross-dock-heavy
  operations.
- Aisle widths set by the truck type (wide aisle ~3.5–4 m for counterbalance, ~2.7–3 m
  reach truck, ~1.6–1.9 m VNA) — *check truck specs*.
- Separate pedestrian picking zones from heavy MHE traffic.

## Gotchas
- Slotting by units shipped rather than hits puts bulk-but-rarely-ordered SKUs in prime
  spots.
- Undersized faces create replenishment storms and short picks during peaks.
- Moving SKUs without updating the pick sequence makes travel worse, not better.

## Verify
- [ ] Hits, cube movement and dimensions extracted per SKU for a representative period.
- [ ] A items in the golden zone near the path start; look-alikes separated.
- [ ] Each face holds ≥ one case and the target days of supply.
- [ ] Min/max replenishment set from lead time; replenishment count per shift monitored.
- [ ] Re-slot moves reflected in WMS locations and pick sequence the same day.
